from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import json
import os
from datetime import datetime
import random
import re
from sqlalchemy import func
from models import init_db, SessionLocal, Flashcard


app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for sessions

def initialize_session():
    """Initialize session variables"""
    if 'current_view' not in session:
        session['current_view'] = 'start'
    if 'current_card_index' not in session:
        session['current_card_index'] = None
    if 'submitted' not in session:
        session['submitted'] = False
    if 'hint_level' not in session:
        session['hint_level'] = 0
    if 'revealed_letters' not in session:
        session['revealed_letters'] = []
    if 'score' not in session:
        session['score'] = {'correct': 0, 'total': 0}
    if 'used_cards' not in session:
        session['used_cards'] = []

def get_flashcards(page=1, per_page=50, category=None, level=None):
    """Get flashcards with pagination and filtering - optimized for large datasets"""
    db = SessionLocal()
    try:
        query = db.query(Flashcard)
        
        # Add filters
        if category:
            query = query.filter(Flashcard.category == category)
        if level:
            query = query.filter(Flashcard.level == level)
        
        # Get total count for pagination
        total = query.count()
        
        # Paginate results
        flashcards = query.order_by(Flashcard.category, Flashcard.french)\
                         .offset((page - 1) * per_page)\
                         .limit(per_page)\
                         .all()
        
        return {
            'flashcards': flashcards,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'pages': (total + per_page - 1) // per_page
            }
        }
    finally:
        db.close()

def get_flashcards_summary():
    """Get summary data for large datasets"""
    db = SessionLocal()
    try:
        # Get categories and counts
        categories = db.query(Flashcard.category, func.count(Flashcard.id))\
                      .group_by(Flashcard.category)\
                      .all()
        
        # Get total count
        total = db.query(Flashcard).count()
        
        return {
            'total_cards': total,
            'categories': [{'name': cat, 'count': count} for cat, count in categories]
        }
    finally:
        db.close()

def get_random_card():
    """Get a random card that hasn't been used yet - optimized for large datasets"""
    db = SessionLocal()
    try:
        # Get total count
        total_cards = db.query(Flashcard).count()
        
        if total_cards == 0:
            return None
        
        # Use database-level random selection for better performance
        if len(session.get('used_cards', [])) >= total_cards:
            # Reset if all cards used
            session['used_cards'] = []
        
        # Get random card using SQL RANDOM() for better performance
        available_cards = db.query(Flashcard)\
                           .filter(~Flashcard.id.in_(session.get('used_cards', [])))\
                           .order_by(func.random())\
                           .limit(1)\
                           .first()
        
        if available_cards:
            session['used_cards'].append(available_cards.id)
            return available_cards.id
        else:
            # Fallback to Python random if needed
            return get_random_card_fallback()
            
    finally:
        db.close()

def get_random_card_fallback():
    """Fallback random card selection"""
    db = SessionLocal()
    try:
        flashcards = db.query(Flashcard).all()
        available_cards = [i for i in range(len(flashcards)) if i not in session.get('used_cards', [])]
        
        if not available_cards:
            session['used_cards'] = []
            available_cards = list(range(len(flashcards)))
        
        random_index = random.choice(available_cards)
        session['used_cards'].append(random_index)
        return random_index
    finally:
        db.close()

def render_hint_display(french_word, revealed_letters):
    """Render the hint display with underlines and revealed letters"""
    if not revealed_letters and session.get('hint_level', 0) == 0:
        return ""
    
    result = []
    for i, char in enumerate(french_word):
        if not re.match(r'[a-zA-ZàâäéèêëïîôöùûüÿçÀÂÄÉÈÊËÏÎÔÖÙÛÜŸÇ]', char):
            # Show spaces and punctuation as-is
            result.append(f'<span class="mx-1">{char}</span>')
        elif i in revealed_letters:
            # Show revealed letters in green
            result.append(f'<span class="revealed-letter">{char}</span>')
        else:
            # Show underlines for unrevealed letters
            result.append('<span class="letter-placeholder">_</span>')
    
    return ''.join(result)

@app.route('/')
def index():
    initialize_session()
    return render_template('base.html')

@app.route('/start_study', methods=['POST'])
def start_study():
    session['current_view'] = 'study'
    session['current_card_index'] = get_random_card()
    session['submitted'] = False
    session['hint_level'] = 0
    session['revealed_letters'] = []
    session['score'] = {'correct': 0, 'total': 0}
    session['used_cards'] = [session['current_card_index']]
    return redirect(url_for('index'))

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    user_input = request.form.get('user_input', '').lower().strip()
    db = SessionLocal()
    try:
        current_card = db.query(Flashcard).filter(Flashcard.id == session['current_card_index']).first()
        if not current_card:
            return redirect(url_for('index'))
            
        correct_answer = current_card.french.lower()
        
        is_correct = user_input == correct_answer
        session['submitted'] = True
        session['is_correct'] = is_correct
        session['user_input'] = request.form.get('user_input', '')
        
        # Update score
        session['score']['total'] += 1
        if is_correct:
            session['score']['correct'] += 1
        
        return redirect(url_for('index'))
    finally:
        db.close()

@app.route('/next_card', methods=['POST'])
def next_card():
    db = SessionLocal()
    try:
        total_cards = db.query(Flashcard).count()
        # Check if we've used all cards
        if len(session.get('used_cards', [])) >= total_cards:
            session['current_view'] = 'results'
        else:
            # Get next random card
            session['current_card_index'] = get_random_card()
            session['submitted'] = False
            session['hint_level'] = 0
            session['revealed_letters'] = []
            session.pop('user_input', None)
            session.pop('is_correct', None)
        
        return redirect(url_for('index'))
    finally:
        db.close()

@app.route('/get_hint', methods=['POST'])
def get_hint():
    db = SessionLocal()
    try:
        current_card = db.query(Flashcard).filter(Flashcard.id == session['current_card_index']).first()
        if not current_card:
            return redirect(url_for('index'))
        
        if session['hint_level'] == 0:
            # First click: show underlines
            session['hint_level'] = 1
        else:
            # Subsequent clicks: reveal random letters
            french_word = current_card.french.lower()
            available_positions = []
            revealed = session.get('revealed_letters', [])
            
            # Find positions that are letters and not already revealed
            for i, char in enumerate(french_word):
                if re.match(r'[a-zàâäéèêëïîôöùûüÿç]', char) and i not in revealed:
                    available_positions.append(i)
            
            if available_positions:
                random_pos = random.choice(available_positions)
                revealed.append(random_pos)
                session['revealed_letters'] = revealed
                session['hint_level'] += 1
        
        return redirect(url_for('index'))
    finally:
        db.close()

@app.route('/reset_study', methods=['POST'])
def reset_study():
    session['current_card_index'] = get_random_card()
    session['submitted'] = False
    session['hint_level'] = 0
    session['revealed_letters'] = []
    session['score'] = {'correct': 0, 'total': 0}
    session['current_view'] = 'study'
    session['used_cards'] = [session['current_card_index']]
    session.pop('user_input', None)
    session.pop('is_correct', None)
    return redirect(url_for('index'))

@app.route('/go_to_start', methods=['POST'])
def go_to_start():
    session.clear()
    session['current_view'] = 'start'
    return redirect(url_for('index'))

@app.context_processor
def inject_template_vars():
    """Inject variables available to all templates - optimized for large datasets"""
    db = SessionLocal()
    try:
        # Get summary data instead of all flashcards
        summary = get_flashcards_summary()
        
        current_card = None
        hint_display = ""
        
        if session.get('current_card_index') is not None:
            # Get only the current card instead of loading all
            current_card = db.query(Flashcard)\
                            .filter(Flashcard.id == session['current_card_index'])\
                            .first()
            
            if current_card and session.get('hint_level', 0) > 0:
                hint_display = render_hint_display(
                    current_card.french,
                    session.get('revealed_letters', [])
                )
        
        return {
            'flashcards_summary': summary,
            'current_card': current_card,
            'hint_display': hint_display,
            'total_cards': summary['total_cards']
        }
    finally:
        db.close()

if __name__ == '__main__':
    # Initialize database on first run
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)