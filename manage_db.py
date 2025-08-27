#!/usr/bin/env python3
"""
Database management script for FlashCard app
Use this to add, view, and manage flashcards
"""

import pandas as pd
import os
import shutil
import csv
from datetime import datetime
from sqlalchemy import func
from models import init_db, SessionLocal_FR, SessionLocal_EN, Flashcard_FR, Flashcard_EN

def add_flashcard_fr(french, english, ipa, category="General", wordType="Not specified", level="XX", note1="", note2=""):
    """Add a new French flashcard to the database"""
    db = SessionLocal_FR()
    try:
        new_card = Flashcard_FR(
            french=french,
            english=english,
            ipa=ipa,
            category=category,
            wordType=wordType,
            level=level,
            note1=note1,
            note2=note2
        )
        db.add(new_card)
        db.commit()
        print(f"✅ Added French card: {french} -> {english}")
        return new_card.id
    except Exception as e:
        print(f"❌ Error adding French card: {e}")
        db.rollback()
        return None
    finally:
        db.close()

def add_flashcard_en(english, chinese, ipa, category="General", wordType="Not specified", notes=""):
    """Add a new English flashcard to the database"""
    db = SessionLocal_EN()
    try:
        new_card = Flashcard_EN(
            english=english,
            chinese=chinese,
            ipa=ipa,
            category=category,
            wordType=wordType,
            notes=notes
        )
        db.add(new_card)
        db.commit()
        print(f"✅ Added English card: {english} -> {chinese}")
        return new_card.id
    except Exception as e:
        print(f"❌ Error adding English card: {e}")
        db.rollback()
        return None
    finally:
        db.close()

def list_all_cards_fr():
    """List all French flashcards in the database"""
    db = SessionLocal_FR()
    try:
        cards = db.query(Flashcard_FR).order_by(Flashcard_FR.category, Flashcard_FR.french).all()
        if not cards:
            print("No French flashcards found in database.")
            return
        
        print(f"\n📚 Found {len(cards)} French flashcards:\n")
        current_category = None
        
        for card in cards:
            if card.category != current_category:
                current_category = card.category
                print(f"\n🏷️  {current_category}:")
            
            note1_display = f" ({card.note1})" if card.note1 else ""
            note2_display = f" [{card.note2}]" if card.note2 else ""
            level_display = f" [{card.level}]" if card.level != "XX" else ""
            wordtype_display = f" <{card.wordType}>" if card.wordType != "Not specified" else ""
            print(f"  • {card.french} → {card.english} [{card.ipa}]{level_display}{wordtype_display}{note1_display}{note2_display}")
        
        print()
    finally:
        db.close()

def list_all_cards_en():
    """List all English flashcards in the database"""
    db = SessionLocal_EN()
    try:
        cards = db.query(Flashcard_EN).order_by(Flashcard_EN.category, Flashcard_EN.english).all()
        if not cards:
            print("No English flashcards found in database.")
            return
        
        print(f"\n📚 Found {len(cards)} English flashcards:\n")
        current_category = None
        
        for card in cards:
            if card.category != current_category:
                current_category = card.category
                print(f"\n🏷️  {current_category}:")
            
            notes_display = f" ({card.notes})" if card.notes else ""
            wordtype_display = f" <{card.wordType}>" if card.wordType != "Not specified" else ""
            print(f"  • {card.english} → {card.chinese} [{card.ipa}]{wordtype_display}{notes_display}")
        
        print()
    finally:
        db.close()

def search_cards_fr(search_term):
    """Search for French flashcards by French or English text"""
    db = SessionLocal_FR()
    try:
        search_pattern = f"%{search_term}%"
        cards = db.query(Flashcard_FR).filter(
            (Flashcard_FR.french.ilike(search_pattern)) |
            (Flashcard_FR.english.ilike(search_pattern))
        ).all()
        
        if not cards:
            print(f"No French cards found matching '{search_term}'")
            return
        
        print(f"\n🔍 Found {len(cards)} French cards matching '{search_term}':\n")
        for card in cards:
            note1_display = f" [{card.note1}]" if card.note1 else ""
            note2_display = f" [{card.note2}]" if card.note2 else ""
            level_display = f" [{card.level}]" if card.level != "XX" else ""
            wordtype_display = f" <{card.wordType}>" if card.wordType != "Not specified" else ""
            print(f"  • {card.french} → {card.english} [{card.ipa}] [{card.category}]{level_display}{wordtype_display}{note1_display}{note2_display}")
        print()
    finally:
        db.close()

def search_cards_en(search_term):
    """Search for English flashcards by English or Chinese text"""
    db = SessionLocal_EN()
    try:
        search_pattern = f"%{search_term}%"
        cards = db.query(Flashcard_EN).filter(
            (Flashcard_EN.english.ilike(search_pattern)) |
            (Flashcard_EN.chinese.ilike(search_pattern))
        ).all()
        
        if not cards:
            print(f"No English cards found matching '{search_term}'")
            return
        
        print(f"\n🔍 Found {len(cards)} English cards matching '{search_term}':\n")
        for card in cards:
            notes_display = f" [{card.notes}]" if card.notes else ""
            wordtype_display = f" <{card.wordType}>" if card.wordType != "Not specified" else ""
            print(f"  • {card.english} → {card.chinese} [{card.ipa}] [{card.category}]{wordtype_display}{notes_display}")
        print()
    finally:
        db.close()

def delete_card_fr(card_id):
    """Delete a French flashcard by ID"""
    db = SessionLocal_FR()
    try:
        card = db.query(Flashcard_FR).filter(Flashcard_FR.id == card_id).first()
        if card:
            print(f"🗑️  Deleting French card: {card.french} -> {card.english}")
            db.delete(card)
            db.commit()
            print("✅ French card deleted successfully")
        else:
            print(f"❌ French card with ID {card_id} not found")
    except Exception as e:
        print(f"❌ Error deleting French card: {e}")
        db.rollback()
    finally:
        db.close()

def delete_card_en(card_id):
    """Delete an English flashcard by ID"""
    db = SessionLocal_EN()
    try:
        card = db.query(Flashcard_EN).filter(Flashcard_EN.id == card_id).first()
        if card:
            print(f"🗑️  Deleting English card: {card.english} -> {card.chinese}")
            db.delete(card)
            db.commit()
            print("✅ English card deleted successfully")
        else:
            print(f"❌ English card with ID {card_id} not found")
    except Exception as e:
        print(f"❌ Error deleting English card: {e}")
        db.rollback()
    finally:
        db.close()

def backup_database():
    """Create a backup of the current databases"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    backup_files = []
    
    if os.path.exists("Flashcard_FR.db"):
        backup_filename_fr = f"Flashcard_FR_backup_{timestamp}.db"
        shutil.copy2("Flashcard_FR.db", backup_filename_fr)
        backup_files.append(backup_filename_fr)
        print(f"✅ French database backed up to: {backup_filename_fr}")
    
    if os.path.exists("Flashcard_EN.db"):
        backup_filename_en = f"Flashcard_EN_backup_{timestamp}.db"
        shutil.copy2("Flashcard_EN.db", backup_filename_en)
        backup_files.append(backup_filename_en)
        print(f"✅ English database backed up to: {backup_filename_en}")
    
    if not backup_files:
        print("❌ No database files found to backup")
        return None
    
    return backup_files

def restore_database(backup_filename):
    """Restore database from a backup file"""
    if not os.path.exists(backup_filename):
        print(f"❌ Backup file '{backup_filename}' not found")
        return False
    
    try:
        # Create backup of current database before restore
        current_backup = backup_database()
        
        # Determine which database to restore based on filename
        if "Flashcard_FR" in backup_filename:
            shutil.copy2(backup_filename, "Flashcard_FR.db")
            print(f"✅ French database restored from: {backup_filename}")
        elif "Flashcard_EN" in backup_filename:
            shutil.copy2(backup_filename, "Flashcard_EN.db")
            print(f"✅ English database restored from: {backup_filename}")
        else:
            print("❌ Could not determine database type from filename")
            return False
        
        if current_backup:
            print(f"📁 Previous databases backed up to: {current_backup}")
        
        return True
    except Exception as e:
        print(f"❌ Error restoring database: {e}")
        return False

def download_template_fr():
    """Download the French CSV template file"""
    template_file = "flashcard_french_template.csv"
    
    try:
        # Get current working directory
        current_dir = os.getcwd()
        print(f"📁 Current working directory: {current_dir}")
        
        # Create sample data for the template
        sample_data = [
            ['french', 'english', 'ipa', 'category', 'wordType', 'level', 'note1', 'note2'],
            ['Bonjour', 'Hello', 'bɔ̃ʒuʁ', 'Greetings', 'Interjection', 'A1', 'Formal greeting', ''],
            ['Merci', 'Thank you', 'mɛʁsi', 'Politeness', 'Interjection', 'A1', 'Informal', ''],
            ['Au revoir', 'Goodbye', 'o ʁəvwaʁ', 'Greetings', 'Interjection', 'A1', 'Formal', ''],
            ['S''il vous plaît', 'Please', 's‿il vu plɛ', 'Politeness', 'Interjection', 'A1', 'Formal', ''],
            ['Excusez-moi', 'Excuse me', 'ɛkskyze mwa', 'Politeness', 'Interjection', 'A1', 'Formal', '']
        ]
        
        # Write CSV file
        with open(template_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(sample_data)
        
        # Verify file was created
        if os.path.exists(template_file):
            file_size = os.path.getsize(template_file)
            print(f"✅ French CSV template created: {template_file}")
            print(f"📊 File size: {file_size} bytes")
            print("📋 Instructions:")
            print("  1. Open this file in Excel or text editor")
            print("  2. Fill in your vocabulary (french and english are required)")
            print("  3. Save the file")
            print("  4. Use option 12 to upload and replace all French flashcards")
            print()
            print("📝 CSV Format:")
            print("  french,english,ipa,category,wordType,level,note1,note2")
            print("  Bonjour,Hello,bɔ̃ʒuʁ,Greetings,Interjection,A1,Formal greeting,")
            print()
            print("📊 Field Descriptions:")
            print("  • french: French word/phrase (required)")
            print("  • english: English translation (required)")
            print("  • ipa: International Phonetic Alphabet pronunciation")
            print("  • category: Word category (default: General)")
            print("  • wordType: Part of speech (Verb, Noun, Adjective, etc.)")
            print("  • level: CEFR level (A1, A2, B1, B2, C1, C2)")
            print("  • note1: Additional information (e.g., m/f, regular/irregular)")
            print("  • note2: Additional notes")
            print()
            print(f"📁 File saved to: {os.path.abspath(template_file)}")
        else:
            print("❌ File was not created successfully")
        
    except Exception as e:
        print(f"❌ Error creating French template: {e}")
        import traceback
        traceback.print_exc()

def download_template_en():
    """Download the English CSV template file"""
    template_file = "flashcard_english_template.csv"
    
    try:
        # Get current working directory
        current_dir = os.getcwd()
        print(f"📁 Current working directory: {current_dir}")
        
        # Create sample data for the template
        sample_data = [
            ['english', 'chinese', 'ipa', 'category', 'wordType', 'notes'],
            ['Hello', '你好', 'həˈloʊ', 'Greetings', 'Interjection', 'Formal greeting'],
            ['Thank you', '谢谢', 'θæŋk ju', 'Politeness', 'Interjection', 'Informal'],
            ['Goodbye', '再见', 'ɡʊdˈbaɪ', 'Greetings', 'Interjection', 'Formal'],
            ['Please', '请', 'pliːz', 'Politeness', 'Interjection', 'Formal'],
            ['Excuse me', '对不起', 'ɪkˈskjuːz mi', 'Politeness', 'Interjection', 'Formal']
        ]
        
        # Write CSV file
        with open(template_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(sample_data)
        
        # Verify file was created
        if os.path.exists(template_file):
            file_size = os.path.getsize(template_file)
            print(f"✅ English CSV template created: {template_file}")
            print(f"📊 File size: {file_size} bytes")
            print("📋 Instructions:")
            print("  1. Open this file in Excel or text editor")
            print("  2. Fill in your vocabulary (english and chinese are required)")
            print("  3. Save the file")
            print("  4. Use option 13 to upload and replace all English flashcards")
            print()
            print("📝 CSV Format:")
            print("  english,chinese,ipa,category,wordType,notes")
            print("  Hello,你好,həˈloʊ,Greetings,Interjection,Formal greeting")
            print()
            print("📊 Field Descriptions:")
            print("  • english: English word/phrase (required)")
            print("  • chinese: Chinese translation (required)")
            print("  • ipa: International Phonetic Alphabet pronunciation")
            print("  • category: Word category (default: General)")
            print("  • wordType: Part of speech (Verb, Noun, Adjective, etc.)")
            print("  • notes: Additional information and notes")
            print()
            print(f"📁 File saved to: {os.path.abspath(template_file)}")
        else:
            print("❌ File was not created successfully")
        
    except Exception as e:
        print(f"❌ Error creating English template: {e}")
        import traceback
        traceback.print_exc()

def upload_csv_replace_all_fr(csv_file):
    """Upload CSV file and completely replace all French flashcards"""
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
        db = SessionLocal_FR()
        try:
            # Delete all existing cards
            existing_count = db.query(Flashcard_FR).count()
            db.query(Flashcard_FR).delete()
            print(f"🗑️  Deleted {existing_count} existing French flashcards")
            
            # Import new cards
            new_cards = []
            for _, row in df.iterrows():
                card = Flashcard_FR(
                    french=str(row['french']).strip(),
                    english=str(row['english']).strip(),
                    ipa=str(row.get('ipa', '')).strip() if pd.notna(row.get('ipa')) else '',
                    category=str(row.get('category', 'General')).strip() if pd.notna(row.get('category')) else 'General',
                    wordType=str(row.get('wordType', 'Not specified')).strip() if pd.notna(row.get('wordType')) else 'Not specified',
                    level=str(row.get('level', 'XX')).strip() if pd.notna(row.get('level')) else 'XX',
                    note1=str(row.get('note1', '')).strip() if pd.notna(row.get('note1')) else '',
                    note2=str(row.get('note2', '')).strip() if pd.notna(row.get('note2')) else ''
                )
                new_cards.append(card)
            
            db.add_all(new_cards)
            db.commit()
            
            print(f"✅ Successfully imported {len(new_cards)} French flashcards")
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

def upload_csv_replace_all_en(csv_file):
    """Upload CSV file and completely replace all English flashcards"""
    if not os.path.exists(csv_file):
        print(f"❌ File '{csv_file}' not found")
        return False
    
    try:
        # Read CSV file
        print(f"📖 Reading CSV file: {csv_file}")
        df = pd.read_csv(csv_file)
        
        # Validate required columns
        required_columns = ['english', 'chinese']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            print(f"❌ Missing required columns: {missing_columns}")
            return False
        
        # Validate data
        print("🔍 Validating data...")
        df = df.dropna(subset=['english', 'chinese'])  # Remove rows with missing required fields
        
        if df.empty:
            print("❌ No valid data found in CSV")
            return False
        
        # Create backup before replacement
        backup_file = backup_database()
        if not backup_file:
            print("❌ Failed to create backup. Aborting import.")
            return False
        
        # Clear existing database and import new data
        db = SessionLocal_EN()
        try:
            # Delete all existing cards
            existing_count = db.query(Flashcard_EN).count()
            db.query(Flashcard_EN).delete()
            print(f"🗑️  Deleted {existing_count} existing English flashcards")
            
            # Import new cards
            new_cards = []
            for _, row in df.iterrows():
                card = Flashcard_EN(
                    english=str(row['english']).strip(),
                    chinese=str(row['chinese']).strip(),
                    ipa=str(row.get('ipa', '')).strip() if pd.notna(row.get('ipa')) else '',
                    category=str(row.get('category', 'General')).strip() if pd.notna(row.get('category')) else 'General',
                    wordType=str(row.get('wordType', 'Not specified')).strip() if pd.notna(row.get('wordType')) else 'Not specified',
                    notes=str(row.get('notes', '')).strip() if pd.notna(row.get('notes')) else ''
                )
                new_cards.append(card)
            
            db.add_all(new_cards)
            db.commit()
            
            print(f"✅ Successfully imported {len(new_cards)} English flashcards")
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

def export_to_csv_fr(filename="flashcards_french_export.csv"):
    """Export all French flashcards to CSV file"""
    db = SessionLocal_FR()
    try:
        cards = db.query(Flashcard_FR).order_by(Flashcard_FR.category, Flashcard_FR.french).all()
        
        if not cards:
            print("❌ No French flashcards to export")
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
                'note1': card.note1 or '',
                'note2': card.note2 or ''
            })
        
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        print(f"✅ Exported {len(cards)} French flashcards to: {filename}")
        return True
        
    except Exception as e:
        print(f"❌ Error exporting French data: {e}")
        return False
    finally:
        db.close()

def export_to_csv_en(filename="flashcards_english_export.csv"):
    """Export all English flashcards to CSV file"""
    db = SessionLocal_EN()
    try:
        cards = db.query(Flashcard_EN).order_by(Flashcard_EN.category, Flashcard_EN.english).all()
        
        if not cards:
            print("❌ No English flashcards to export")
            return False
        
        # Convert to DataFrame
        data = []
        for card in cards:
            data.append({
                'english': card.english,
                'chinese': card.chinese,
                'ipa': card.ipa or '',
                'category': card.category or '',
                'wordType': card.wordType or '',
                'notes': card.notes or ''
            })
        
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        print(f"✅ Exported {len(cards)} English flashcards to: {filename}")
        return True
        
    except Exception as e:
        print(f"❌ Error exporting English data: {e}")
        return False
    finally:
        db.close()

def show_menu():
    """Show the main menu"""
    print("\n" + "="*70)
    print("🗃️  FlashCard Database Manager - Multi-Language")
    print("="*70)
    print("1. View all French cards")
    print("2. View all English cards")
    print("3. Add new French card")
    print("4. Add new English card")
    print("5. Search French cards")
    print("6. Search English cards")
    print("7. Delete French card")
    print("8. Delete English card")
    print("9. Initialize databases")
    print("10. Download French CSV template")
    print("11. Download English CSV template")
    print("12. Upload French CSV (replace all)")
    print("13. Upload English CSV (replace all)")
    print("14. Export French to CSV")
    print("15. Export English to CSV")
    print("16. Backup databases")
    print("17. Restore database")
    print("18. Exit")
    print("="*70)

def main():
    """Main function"""
    while True:
        show_menu()
        choice = input("Choose an option (1-18): ").strip()
        
        if choice == "1":
            list_all_cards_fr()
        
        elif choice == "2":
            list_all_cards_en()
        
        elif choice == "3":
            print("\n➕ Add New French Flashcard:")
            french = input("French word: ").strip()
            english = input("English translation: ").strip()
            ipa = input("IPA pronunciation (optional): ").strip()
            category = input("Category (default: General): ").strip() or "General"
            wordType = input("Word type (default: Not specified): ").strip() or "Not specified"
            level = input("Level (A1/A2/B1/B2/C1/C2, default: XX): ").strip() or "XX"
            note1 = input("Note 1 (optional): ").strip()
            note2 = input("Note 2 (optional): ").strip()
            
            if french and english:
                add_flashcard_fr(french, english, ipa, category, wordType, level, note1, note2)
            else:
                print("❌ French and English are required!")
        
        elif choice == "4":
            print("\n➕ Add New English Flashcard:")
            english = input("English word: ").strip()
            chinese = input("Chinese translation: ").strip()
            ipa = input("IPA pronunciation (optional): ").strip()
            category = input("Category (default: General): ").strip() or "General"
            wordType = input("Word type (default: Not specified): ").strip() or "Not specified"
            notes = input("Notes (optional): ").strip()
            
            if english and chinese:
                add_flashcard_en(english, chinese, ipa, category, wordType, notes)
            else:
                print("❌ English and Chinese are required!")
        
        elif choice == "5":
            search_term = input("Enter search term for French cards: ").strip()
            if search_term:
                search_cards_fr(search_term)
            else:
                print("❌ Please enter a search term")
        
        elif choice == "6":
            search_term = input("Enter search term for English cards: ").strip()
            if search_term:
                search_cards_en(search_term)
            else:
                print("❌ Please enter a search term")
        
        elif choice == "7":
            list_all_cards_fr()
            try:
                card_id = int(input("Enter French card ID to delete: "))
                delete_card_fr(card_id)
            except ValueError:
                print("❌ Please enter a valid number")
        
        elif choice == "8":
            list_all_cards_en()
            try:
                card_id = int(input("Enter English card ID to delete: "))
                delete_card_en(card_id)
            except ValueError:
                print("❌ Please enter a valid number")
        
        elif choice == "9":
            print("🗄️  Initializing databases...")
            init_db()
            print("✅ Databases initialized!")
        
        elif choice == "10":
            download_template_fr()
        
        elif choice == "11":
            download_template_en()
        
        elif choice == "12":
            print("\n⚠️  WARNING: This will replace ALL existing French flashcards!")
            confirm = input("Type 'YES' to confirm: ").strip()
            if confirm == "YES":
                csv_file = input("Enter CSV filename: ").strip()
                if csv_file:
                    upload_csv_replace_all_fr(csv_file)
                else:
                    print("❌ Please enter a filename")
            else:
                print("❌ Import cancelled")
        
        elif choice == "13":
            print("\n⚠️  WARNING: This will replace ALL existing English flashcards!")
            confirm = input("Type 'YES' to confirm: ").strip()
            if confirm == "YES":
                csv_file = input("Enter CSV filename: ").strip()
                if csv_file:
                    upload_csv_replace_all_en(csv_file)
                else:
                    print("❌ Please enter a filename")
            else:
                print("❌ Import cancelled")
        
        elif choice == "14":
            filename = input("Enter export filename (default: flashcards_french_export.csv): ").strip()
            if not filename:
                filename = "flashcards_french_export.csv"
            export_to_csv_fr(filename)
        
        elif choice == "15":
            filename = input("Enter export filename (default: flashcards_english_export.csv): ").strip()
            if not filename:
                filename = "flashcards_english_export.csv"
            export_to_csv_en(filename)
        
        elif choice == "16":
            backup_database()
        
        elif choice == "17":
            backup_files = [f for f in os.listdir('.') if f.startswith(('Flashcard_FR_backup_', 'Flashcard_EN_backup_')) and f.endswith('.db')]
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
        
        elif choice == "18":
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
