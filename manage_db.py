#!/usr/bin/env python3
"""
Database management script for FlashCard app
Use this to add, view, and manage flashcards
"""

import pandas as pd
import os
import shutil
from datetime import datetime
from sqlalchemy import func
from models import init_db, SessionLocal, Flashcard

def add_flashcard(french, english, ipa, category="General", wordType="Not specified", level="XX", notes=""):
    """Add a new flashcard to the database"""
    db = SessionLocal()
    try:
        new_card = Flashcard(
            french=french,
            english=english,
            ipa=ipa,
            category=category,
            wordType=wordType,
            level=level,
            notes=notes
        )
        db.add(new_card)
        db.commit()
        print(f"✅ Added: {french} -> {english}")
        return new_card.id
    except Exception as e:
        print(f"❌ Error adding card: {e}")
        db.rollback()
        return None
    finally:
        db.close()

def list_all_cards():
    """List all flashcards in the database"""
    db = SessionLocal()
    try:
        cards = db.query(Flashcard).order_by(Flashcard.category, Flashcard.french).all()
        if not cards:
            print("No flashcards found in database.")
            return
        
        print(f"\n📚 Found {len(cards)} flashcards:\n")
        current_category = None
        
        for card in cards:
            if card.category != current_category:
                current_category = card.category
                print(f"\n🏷️  {current_category}:")
            
            notes_display = f" ({card.notes})" if card.notes else ""
            level_display = f" [{card.level}]" if card.level != "XX" else ""
            wordtype_display = f" <{card.wordType}>" if card.wordType != "Not specified" else ""
            print(f"  • {card.french} → {card.english} [{card.ipa}]{level_display}{wordtype_display}{notes_display}")
        
        print()
    finally:
        db.close()

def search_cards(search_term):
    """Search for flashcards by French or English text"""
    db = SessionLocal()
    try:
        search_pattern = f"%{search_term}%"
        cards = db.query(Flashcard).filter(
            (Flashcard.french.ilike(search_pattern)) |
            (Flashcard.english.ilike(search_pattern))
        ).all()
        
        if not cards:
            print(f"No cards found matching '{search_term}'")
            return
        
        print(f"\n🔍 Found {len(cards)} cards matching '{search_term}':\n")
        for card in cards:
            notes_display = f" [{card.notes}]" if card.notes else ""
            level_display = f" [{card.level}]" if card.level != "XX" else ""
            wordtype_display = f" <{card.wordType}>" if card.wordType != "Not specified" else ""
            print(f"  • {card.french} → {card.english} [{card.ipa}] [{card.category}]{level_display}{wordtype_display}{notes_display}")
        print()
    finally:
        db.close()

def delete_card(card_id):
    """Delete a flashcard by ID"""
    db = SessionLocal()
    try:
        card = db.query(Flashcard).filter(Flashcard.id == card_id).first()
        if card:
            print(f"🗑️  Deleting: {card.french} -> {card.english}")
            db.delete(card)
            db.commit()
            print("✅ Card deleted successfully")
        else:
            print(f"❌ Card with ID {card_id} not found")
    except Exception as e:
        print(f"❌ Error deleting card: {e}")
        db.rollback()
    finally:
        db.close()

def backup_database():
    """Create a backup of the current database"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"flashcards_backup_{timestamp}.db"
    
    if os.path.exists("flashcards.db"):
        shutil.copy2("flashcards.db", backup_filename)
        print(f"✅ Database backed up to: {backup_filename}")
        return backup_filename
    else:
        print("❌ No database file found to backup")
        return None

def restore_database(backup_filename):
    """Restore database from a backup file"""
    if not os.path.exists(backup_filename):
        print(f"❌ Backup file '{backup_filename}' not found")
        return False
    
    try:
        # Create backup of current database before restore
        current_backup = backup_database()
        
        # Restore from backup
        shutil.copy2(backup_filename, "flashcards.db")
        print(f"✅ Database restored from: {backup_filename}")
        
        if current_backup:
            print(f"📁 Previous database backed up to: {current_backup}")
        
        return True
    except Exception as e:
        print(f"❌ Error restoring database: {e}")
        return False

def download_template():
    """Download the CSV template file"""
    template_file = "flashcard_template.csv"
    if os.path.exists(template_file):
        print(f"📥 CSV template available: {template_file}")
        print("📋 Instructions:")
        print("  1. Open this file in Excel or text editor")
        print("  2. Fill in your vocabulary (french and english are required)")
        print("  3. Save the file")
        print("  4. Use option 7 to upload and replace all flashcards")
        print()
        print("📝 CSV Format:")
        print("  french,english,ipa,category,wordType,level,notes")
        print("  Bonjour,Hello,bɔ̃ʒuʁ,Greetings,Interjection,A1,Formal greeting")
        print()
        print("📊 Field Descriptions:")
        print("  • french: French word/phrase (required)")
        print("  • english: English translation (required)")
        print("  • ipa: International Phonetic Alphabet pronunciation")
        print("  • category: Word category (default: General)")
        print("  • wordType: Part of speech (Verb, Noun, Adjective, etc.)")
        print("  • level: CEFR level (A1, A2, B1, B2, C1, C2)")
        print("  • notes: Additional information")
        print()
    else:
        print("❌ Template file not found")

def upload_csv_replace_all(csv_file):
    """Upload CSV file and completely replace all flashcards"""
    if not os.path.exists(csv_file):
        print(f"❌ File '{csv_file}' not found")
        return False
    
    try:
        # Read CSV file
        print(f"📖 Reading CSV file: {csv_file}")
        df = pd.read_csv(csv_file)
        
        # Validate required columns
        required_columns = ['french', 'english']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            print(f"❌ Missing required columns: {missing_columns}")
            return False
        
        # Validate data
        print("🔍 Validating data...")
        df = df.dropna(subset=['french', 'english'])  # Remove rows with missing required fields
        
        if df.empty:
            print("❌ No valid data found in CSV")
            return False
        
        # Create backup before replacement
        backup_file = backup_database()
        if not backup_file:
            print("❌ Failed to create backup. Aborting import.")
            return False
        
        # Clear existing database and import new data
        db = SessionLocal()
        try:
            # Delete all existing cards
            existing_count = db.query(Flashcard).count()
            db.query(Flashcard).delete()
            print(f"🗑️  Deleted {existing_count} existing flashcards")
            
            # Import new cards
            new_cards = []
            for _, row in df.iterrows():
                card = Flashcard(
                    french=str(row['french']).strip(),
                    english=str(row['english']).strip(),
                    ipa=str(row.get('ipa', '')).strip() if pd.notna(row.get('ipa')) else '',
                    category=str(row.get('category', 'General')).strip() if pd.notna(row.get('category')) else 'General',
                    wordType=str(row.get('wordType', 'Not specified')).strip() if pd.notna(row.get('wordType')) else 'Not specified',
                    level=str(row.get('level', 'XX')).strip() if pd.notna(row.get('level')) else 'XX',
                    notes=str(row.get('notes', '')).strip() if pd.notna(row.get('notes')) else ''
                )
                new_cards.append(card)
            
            db.add_all(new_cards)
            db.commit()
            
            print(f"✅ Successfully imported {len(new_cards)} flashcards")
            print(f"📁 Previous database backed up to: {backup_file}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error importing data: {e}")
            db.rollback()
            return False
        finally:
            db.close()
            
    except Exception as e:
        print(f"❌ Error reading CSV file: {e}")
        return False

def export_to_csv(filename="flashcards_export.csv"):
    """Export all flashcards to CSV file"""
    db = SessionLocal()
    try:
        cards = db.query(Flashcard).order_by(Flashcard.category, Flashcard.french).all()
        
        if not cards:
            print("❌ No flashcards to export")
            return False
        
        # Convert to DataFrame
        data = []
        for card in cards:
            data.append({
                'french': card.french,
                'english': card.english,
                'ipa': card.ipa or '',
                'category': card.category or '',
                'wordType': card.wordType or '',
                'level': card.level or '',
                'notes': card.notes or ''
            })
        
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        print(f"✅ Exported {len(cards)} flashcards to: {filename}")
        return True
        
    except Exception as e:
        print(f"❌ Error exporting data: {e}")
        return False
    finally:
        db.close()

def show_menu():
    """Show the main menu"""
    print("\n" + "="*60)
    print("🗃️  FlashCard Database Manager")
    print("="*60)
    print("1. View all cards")
    print("2. Add new card")
    print("3. Search cards")
    print("4. Delete card")
    print("5. Initialize database")
    print("6. Download CSV template")
    print("7. Upload CSV (replace all)")
    print("8. Export to CSV")
    print("9. Backup database")
    print("10. Restore database")
    print("11. Exit")
    print("="*60)

def main():
    """Main function"""
    while True:
        show_menu()
        choice = input("Choose an option (1-11): ").strip()
        
        if choice == "1":
            list_all_cards()
        
        elif choice == "2":
            print("\n➕ Add New Flashcard:")
            french = input("French word: ").strip()
            english = input("English translation: ").strip()
            ipa = input("IPA pronunciation (optional): ").strip()
            category = input("Category (default: General): ").strip() or "General"
            wordType = input("Word type (default: Not specified): ").strip() or "Not specified"
            level = input("Level (A1/A2/B1/B2/C1/C2, default: XX): ").strip() or "XX"
            notes = input("Notes (optional): ").strip()
            
            if french and english:
                add_flashcard(french, english, ipa, category, wordType, level, notes)
            else:
                print("❌ French and English are required!")
        
        elif choice == "3":
            search_term = input("Enter search term: ").strip()
            if search_term:
                search_cards(search_term)
            else:
                print("❌ Please enter a search term")
        
        elif choice == "4":
            list_all_cards()
            try:
                card_id = int(input("Enter card ID to delete: "))
                delete_card(card_id)
            except ValueError:
                print("❌ Please enter a valid number")
        
        elif choice == "5":
            print("🗄️  Initializing database...")
            init_db()
            print("✅ Database initialized!")
        
        elif choice == "6":
            download_template()
        
        elif choice == "7":
            print("\n⚠️  WARNING: This will replace ALL existing flashcards!")
            confirm = input("Type 'YES' to confirm: ").strip()
            if confirm == "YES":
                csv_file = input("Enter CSV filename: ").strip()
                if csv_file:
                    upload_csv_replace_all(csv_file)
                else:
                    print("❌ Please enter a filename")
            else:
                print("❌ Import cancelled")
        
        elif choice == "8":
            filename = input("Enter export filename (default: flashcards_export.csv): ").strip()
            if not filename:
                filename = "flashcards_export.csv"
            export_to_csv(filename)
        
        elif choice == "9":
            backup_database()
        
        elif choice == "10":
            backup_files = [f for f in os.listdir('.') if f.startswith('flashcards_backup_') and f.endswith('.db')]
            if backup_files:
                print("\n📁 Available backups:")
                for i, backup in enumerate(sorted(backup_files, reverse=True), 1):
                    print(f"  {i}. {backup}")
                
                try:
                    backup_choice = int(input("Choose backup number: ")) - 1
                    if 0 <= backup_choice < len(backup_files):
                        selected_backup = sorted(backup_files, reverse=True)[backup_choice]
                        restore_database(selected_backup)
                    else:
                        print("❌ Invalid choice")
                except ValueError:
                    print("❌ Please enter a valid number")
            else:
                print("❌ No backup files found")
        
        elif choice == "11":
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
