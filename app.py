from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import json
import os
from datetime import datetime
import random
import re
from sqlalchemy import func
from models import init_db, SessionLocal_FR, SessionLocal_EN, Flashcard_FR, Flashcard_EN

# Global cache for flashcards (server-side)
flashcard_cache = {
    'french': {
        'cards': [],
        'used_indices': set(),
        'total_cards': 0,
        'last_refresh': None,
        'total_cards_used': 0  # Track total cards used across refreshes
    },
    'english': {
        'cards': [],
        'used_indices': set(),
        'total_cards': 0,
        'last_refresh': None,
        'total_cards_used': 0  # Track total cards used across refreshes
    }
}

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
    if 'selected_language' not in session:
        session['selected_language'] = None

def get_flashcards_summary():
    """Get summary data for the selected language"""
    if session.get('selected_language') == 'french':
        db = SessionLocal_FR()
        try:
            # Get categories and counts
            categories = db.query(Flashcard_FR.category, func.count(Flashcard_FR.id))\
                          .group_by(Flashcard_FR.category)\
                          .all()
            
            # Get total count
            total = db.query(Flashcard_FR).count()
            
            return {
                'total_cards': total,
                'categories': [{'name': cat, 'count': count} for cat, count in categories]
            }
        finally:
            db.close()
    elif session.get('selected_language') == 'english':
        db = SessionLocal_EN()
        try:
            # Get categories and counts
            categories = db.query(Flashcard_EN.category, func.count(Flashcard_EN.id))\
                          .group_by(Flashcard_EN.category)\
                          .all()
            
            # Get total count
            total = db.query(Flashcard_EN).count()
            
            return {
                'total_cards': total,
                'categories': [{'name': cat, 'count': count} for cat, count in categories]
            }
        finally:
            db.close()
    else:
        return {'total_cards': 0, 'categories': []}

def refresh_card_cache(language, force=False):
    """Refresh the card cache with a new batch of 50 random cards"""
    global flashcard_cache
    
    cache = flashcard_cache[language]
    current_time = datetime.now()
    
    # Check if we need to refresh (every 5 minutes or if forced)
    if not force and (cache['last_refresh'] and 
                     (current_time - cache['last_refresh']).seconds < 300):
        return
    
    try:
        if language == 'french':
            db = SessionLocal_FR()
            model = Flashcard_FR
        else:
            db = SessionLocal_EN()
            model = Flashcard_EN
        
        # Get total count first
        total_cards = db.query(model).count()
        cache['total_cards'] = total_cards
        
        if total_cards == 0:
            cache['cards'] = []
            cache['used_indices'] = set()
            return
        
        # Get 50 random cards, excluding previously used ones
        used_ids = set()
        if cache['cards']:
            # Get IDs of cards in current cache
            used_ids = {card.id for card in cache['cards']}
        
        # Query for new random cards
        new_cards = db.query(model)\
                      .filter(~model.id.in_(used_ids))\
                      .order_by(func.random())\
                      .limit(50)\
                      .all()
        
        # If we don't have enough new cards, reset and get fresh batch
        if len(new_cards) < 50 and len(used_ids) > 0:
            new_cards = db.query(model)\
                          .order_by(func.random())\
                          .limit(50)\
                          .all()
            cache['used_indices'] = set()
        
        cache['cards'] = new_cards
        cache['used_indices'] = set()
        cache['last_refresh'] = current_time
        # Note: total_cards_used is preserved across refreshes
        
        print(f"🔄 Refreshed {language} cache: {len(new_cards)} cards loaded")
        
    except Exception as e:
        print(f"❌ Error refreshing {language} cache: {e}")
    finally:
        db.close()

def get_random_card():
    """Get a random card from cache, refresh if needed"""
    language = session.get('selected_language')
    if not language:
        return None
    
    # Ensure cache is initialized
    if not flashcard_cache[language]['cards']:
        refresh_card_cache(language, force=True)
    
    cache = flashcard_cache[language]
    
    # If all cards in current batch are used, refresh cache
    if len(cache['used_indices']) >= len(cache['cards']):
        refresh_card_cache(language, force=True)
        cache = flashcard_cache[language]
    
    # Get random unused card from cache
    available_indices = set(range(len(cache['cards']))) - cache['used_indices']
    if not available_indices:
        # Fallback: refresh cache and try again
        refresh_card_cache(language, force=True)
        cache = flashcard_cache[language]
        available_indices = set(range(len(cache['cards']))) - cache['used_indices']
    
    # Check if all cards in database have been used
    if cache['total_cards_used'] >= cache['total_cards']:
        # All cards used - redirect to ending page
        session['current_view'] = 'ending'
        return None
    
    if available_indices:
        # Select random index from available ones
        selected_index = random.choice(list(available_indices))
        cache['used_indices'].add(selected_index)
        
        # Increment total cards used across refreshes
        cache['total_cards_used'] += 1
        
        # Store the card ID in session for compatibility
        selected_card = cache['cards'][selected_index]
        session['current_card_index'] = selected_card.id
        
        return selected_card.id
    
    return None

def get_random_card_fallback(language):
    """Fallback random card selection"""
    if language == 'french':
        db = SessionLocal_FR()
        try:
            flashcards = db.query(Flashcard_FR).all()
            available_cards = [i for i in range(len(flashcards)) if i not in session.get('used_cards', [])]
            
            if not available_cards:
                session['used_cards'] = []
                available_cards = list(range(len(flashcards)))
            
            random_index = random.choice(available_cards)
            session['used_cards'].append(random_index)
            return random_index
        finally:
            db.close()
    elif language == 'english':
        db = SessionLocal_EN()
        try:
            flashcards = db.query(Flashcard_EN).all()
            available_cards = [i for i in range(len(flashcards)) if i not in session.get('used_cards', [])]
            
            if not available_cards:
                session['used_cards'] = []
                available_cards = list(range(len(flashcards)))
            
            random_index = random.choice(available_cards)
            session['used_cards'].append(random_index)
            return random_index
        finally:
            db.close()
    return None

def render_hint_display(word, revealed_letters, language):
    """Render the hint display with underlines and revealed letters"""
    if not revealed_letters and session.get('hint_level', 0) == 0:
        return ""
    
    result = []
    for i, char in enumerate(word):
        if language == 'french':
            if not re.match(r'[a-zA-ZàâäéèêëïîôöùûüÿçÀÂÄÉÈÊËÏÎÔÖÙÛÜŸÇ]', char):
                # Show spaces and punctuation as-is
                result.append(f'<span class="mx-1">{char}</span>')
            elif i in revealed_letters:
                # Show revealed letters in green
                result.append(f'<span class="revealed-letter">{char}</span>')
            else:
                # Show underlines for unrevealed letters
                result.append('<span class="letter-placeholder">_</span>')
        else:  # english
            if not re.match(r'[a-zA-Z]', char):
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

@app.route('/select_language', methods=['GET', 'POST'])
def select_language():
    if request.method == 'POST':
        session['current_view'] = 'language_selection'
    elif request.method == 'GET':
        # If accessed via GET, redirect to start
        return redirect(url_for('index'))
    return render_template('base.html')

@app.route('/start_study', methods=['POST'])
def start_study():
    session['current_view'] = 'study'
    session['current_card_index'] = get_random_card()
    
    # Check if we've used all cards (get_random_card will set current_view to 'ending' if needed)
    if session['current_card_index'] is None:
        # All cards used - ending page will be shown
        return redirect(url_for('index'))
    
    session['submitted'] = False
    session['hint_level'] = 0
    session['revealed_letters'] = []
    session['score'] = {'correct': 0, 'total': 0}
    session['used_cards'] = [session['current_card_index']]
    session.pop('flip_used', None)  # Reset flip flag
    return redirect(url_for('index'))

@app.route('/select_language_french', methods=['POST'])
def select_language_french():
    session['selected_language'] = 'french'
    # Clear cache for new language session
    global flashcard_cache
    flashcard_cache['french']['cards'] = []
    flashcard_cache['french']['used_indices'] = set()
    flashcard_cache['french']['total_cards_used'] = 0  # Reset counter for new session
    
    session['current_view'] = 'study'
    session['current_card_index'] = get_random_card()
    
    # Check if we've used all cards (get_random_card will set current_view to 'ending' if needed)
    if session['current_card_index'] is None:
        # All cards used - ending page will be shown
        return redirect(url_for('index'))
    
    session['submitted'] = False
    session['hint_level'] = 0
    session['revealed_letters'] = []
    session['score'] = {'correct': 0, 'total': 0}
    session['used_cards'] = [session['current_card_index']]
    session.pop('flip_used', None)  # Reset flip flag
    return redirect(url_for('index'))

@app.route('/select_language_english', methods=['POST'])
def select_language_english():
    session['selected_language'] = 'english'
    # Clear cache for new language session
    global flashcard_cache
    flashcard_cache['english']['cards'] = []
    flashcard_cache['english']['used_indices'] = set()
    flashcard_cache['english']['total_cards_used'] = 0  # Reset counter for new session
    
    session['current_view'] = 'study'
    session['current_card_index'] = get_random_card()
    
    # Check if we've used all cards (get_random_card will set current_view to 'ending' if needed)
    if session['current_card_index'] is None:
        # All cards used - ending page will be shown
        return redirect(url_for('index'))
    
    session['submitted'] = False
    session['hint_level'] = 0
    session['revealed_letters'] = []
    session['score'] = {'correct': 0, 'total': 0}
    session['used_cards'] = [session['current_card_index']]
    session.pop('flip_used', None)  # Reset flip flag
    return redirect(url_for('index'))

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    user_input = request.form.get('user_input', '').lower().strip()
    
    if session.get('selected_language') == 'french':
        db = SessionLocal_FR()
        try:
            current_card = db.query(Flashcard_FR).filter(Flashcard_FR.id == session['current_card_index']).first()
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
    elif session.get('selected_language') == 'english':
        db = SessionLocal_EN()
        try:
            current_card = db.query(Flashcard_EN).filter(Flashcard_EN.id == session['current_card_index']).first()
            if not current_card:
                return redirect(url_for('index'))
                
            correct_answer = current_card.english.lower()
            
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
    
    return redirect(url_for('index'))

@app.route('/next_card', methods=['POST'])
def next_card():
    if session.get('selected_language') == 'french':
        db = SessionLocal_FR()
        try:
            # Check if this was a flip scenario (answer was revealed without submission)
            if not session.get('submitted', False) and session.get('flip_used', False):
                # This was a flip scenario - increment total score but not correct count
                session['score']['total'] += 1
            
            # Get next random card
            session['current_card_index'] = get_random_card()
            
            # Check if we've used all cards (get_random_card will set current_view to 'ending' if needed)
            if session['current_card_index'] is None:
                # All cards used - ending page will be shown
                return redirect(url_for('index'))
            
            session['submitted'] = False
            session['hint_level'] = 0
            session['revealed_letters'] = []
            session.pop('user_input', None)
            session.pop('is_correct', None)
            session.pop('flip_used', None)  # Reset flip flag
            
            return redirect(url_for('index'))
        finally:
            db.close()
    elif session.get('selected_language') == 'english':
        db = SessionLocal_EN()
        try:
            # Check if this was a flip scenario (answer was revealed without submission)
            if not session.get('submitted', False) and session.get('flip_used', False):
                # This was a flip scenario - increment total score but not correct count
                session['score']['total'] += 1
            
            # Get next random card
            session['current_card_index'] = get_random_card()
            
            # Check if we've used all cards (get_random_card will set current_view to 'ending' if needed)
            if session['current_card_index'] is None:
                # All cards used - ending page will be shown
                return redirect(url_for('index'))
            
            session['submitted'] = False
            session['hint_level'] = 0
            session['revealed_letters'] = []
            session.pop('user_input', None)
            session.pop('is_correct', None)
            session.pop('flip_used', None)  # Reset flip flag
            
            return redirect(url_for('index'))
        finally:
            db.close()
    
    return redirect(url_for('index'))

@app.route('/flip_answer', methods=['POST'])
def flip_answer():
    """Handle flip button click - mark that answer was revealed"""
    session['flip_used'] = True
    return jsonify({'success': True})

@app.route('/get_hint', methods=['POST'])
def get_hint():
    if session.get('selected_language') == 'french':
        db = SessionLocal_FR()
        try:
            current_card = db.query(Flashcard_FR).filter(Flashcard_FR.id == session['current_card_index']).first()
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
    elif session.get('selected_language') == 'english':
        db = SessionLocal_EN()
        try:
            current_card = db.query(Flashcard_EN).filter(Flashcard_EN.id == session['current_card_index']).first()
            if not current_card:
                return redirect(url_for('index'))
            
            if session['hint_level'] == 0:
                # First click: show underlines
                session['hint_level'] = 1
            else:
                # Subsequent clicks: reveal random letters
                english_word = current_card.english.lower()
                available_positions = []
                revealed = session.get('revealed_letters', [])
                
                # Find positions that are letters and not already revealed
                for i, char in enumerate(english_word):
                    if re.match(r'[a-z]', char) and i not in revealed:
                        available_positions.append(i)
                
                if available_positions:
                    random_pos = random.choice(available_positions)
                    revealed.append(random_pos)
                    session['revealed_letters'] = revealed
                    session['hint_level'] += 1
            
            return redirect(url_for('index'))
        finally:
            db.close()
    
    return redirect(url_for('index'))

@app.route('/reset_study', methods=['POST'])
def reset_study():
    session['current_card_index'] = get_random_card()
    
    # Check if we've used all cards (get_random_card will set current_view to 'ending' if needed)
    if session['current_card_index'] is None:
        # All cards used - ending page will be shown
        return redirect(url_for('index'))
    
    session['submitted'] = False
    session['hint_level'] = 0
    session['revealed_letters'] = []
    session['score'] = {'correct': 0, 'total': 0}
    session['current_view'] = 'study'
    session['used_cards'] = [session['current_card_index']]
    session.pop('user_input', None)
    session.pop('is_correct', None)
    session.pop('flip_used', None)  # Reset flip flag
    return redirect(url_for('index'))

@app.route('/go_to_start', methods=['POST'])
def go_to_start():
    session.clear()
    session['current_view'] = 'start'
    
    # Clear all caches when returning to start
    global flashcard_cache
    for language in flashcard_cache:
        flashcard_cache[language]['cards'] = []
        flashcard_cache[language]['used_indices'] = set()
        flashcard_cache[language]['last_refresh'] = None
        flashcard_cache[language]['total_cards_used'] = 0
    
    return redirect(url_for('index'))

@app.route('/ending')
def ending():
    """Ending page when all cards have been used"""
    session['current_view'] = 'ending'
    return render_template('base.html')

@app.route('/cache_status')
def cache_status():
    """Debug endpoint to check cache status"""
    global flashcard_cache
    status = {}
    for language, cache in flashcard_cache.items():
        status[language] = {
            'cards_loaded': len(cache['cards']),
            'cards_used': len(cache['used_indices']),
            'cards_remaining': len(cache['cards']) - len(cache['used_indices']),
            'total_cards_used': cache['total_cards_used'],
            'last_refresh': str(cache['last_refresh']) if cache['last_refresh'] else 'Never',
            'total_in_db': cache['total_cards']
        }
    return jsonify(status)

@app.context_processor
def inject_template_vars():
    """Inject variables available to all templates - using cache for better performance"""
    summary = get_flashcards_summary()
    
    current_card = None
    hint_display = ""
    
    if session.get('current_card_index') is not None and session.get('selected_language'):
        language = session['selected_language']
        
        # Try to get card from cache first
        if language in flashcard_cache and flashcard_cache[language]['cards']:
            cache = flashcard_cache[language]
            # Find the current card in cache
            for card in cache['cards']:
                if card.id == session['current_card_index']:
                    current_card = card
                    break
        
        # If not found in cache, fallback to database (shouldn't happen with proper cache management)
        if not current_card:
            if language == 'french':
                db = SessionLocal_FR()
                try:
                    current_card = db.query(Flashcard_FR)\
                                    .filter(Flashcard_FR.id == session['current_card_index'])\
                                    .first()
                finally:
                    db.close()
            elif language == 'english':
                db = SessionLocal_EN()
                try:
                    current_card = db.query(Flashcard_EN)\
                                    .filter(Flashcard_EN.id == session['current_card_index'])\
                                    .first()
                finally:
                    db.close()
        
        # Generate hint display if needed
        if current_card and session.get('hint_level', 0) > 0:
            if language == 'french':
                hint_display = render_hint_display(
                    current_card.french,
                    session.get('revealed_letters', []),
                    'french'
                )
            elif language == 'english':
                hint_display = render_hint_display(
                    current_card.english,
                    session.get('revealed_letters', []),
                    'english'
                )
    
    # Get total cards used from cache for progress display
    total_cards_used = 0
    if session.get('selected_language') and session.get('selected_language') in flashcard_cache:
        total_cards_used = flashcard_cache[session['selected_language']]['total_cards_used']
    
    return {
        'flashcards_summary': summary,
        'current_card': current_card,
        'hint_display': hint_display,
        'total_cards': summary['total_cards'],
        'total_cards_used': total_cards_used
    }

if __name__ == '__main__':
    # Initialize database on first run
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)