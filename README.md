# Multi-Language Flashcard Application

A Flask-based flashcard application that supports multiple languages for vocabulary learning.

## Features

### 🌍 Multi-Language Support
- **French Flashcards**: Learn French vocabulary with English translations
- **English Flashcards**: Learn English vocabulary with Chinese translations
- **Scalable Architecture**: Easy to add more languages in the future

### 📚 Enhanced Database Schema
- **Split Notes**: Notes are now split into `note1` and `note2` fields for better organization
- **Multiple Databases**: Separate database files for each language
  - `Flashcard_FR.db` for French flashcards
  - `Flashcard_EN.db` for English flashcards

### 🎯 User Experience
- **Language Selection**: Users can choose their target language before starting
- **Adaptive Interface**: UI automatically adjusts based on selected language
- **Improved Navigation**: Clear flow from start → language selection → study mode

## Database Structure

### Flashcard_FR (French Database)
**Table Name**: `flashcards_fr`
```sql
- id: Primary key
- french: French word/phrase (required)
- english: English translation (required)
- ipa: International Phonetic Alphabet pronunciation
- category: Word category (default: General)
- wordType: Part of speech (Verb, Noun, Adjective, etc.)
- level: CEFR level (A1, A2, B1, B2, C1, C2)
- note1: Additional information (e.g., m/f, regular/irregular)
- note2: Additional notes
- created_at: Timestamp
```

### Flashcard_EN (English Database)
**Table Name**: `flashcards_en`
```sql
- id: Primary key
- english: English word/phrase (required)
- chinese: Chinese translation (required)
- ipa: International Phonetic Alphabet pronunciation
- category: Word category (default: General)
- wordType: Part of speech (Verb, Noun, Adjective, etc.)
- notes: Additional information and notes
- created_at: Timestamp
```

## Installation & Setup

1. **Activate Virtual Environment**:
   ```bash
   .\venv\Scripts\Activate.ps1  # Windows PowerShell
   # or
   .\venv\Scripts\activate      # Windows Command Prompt
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize Databases**:
   ```bash
   python test_setup.py
   ```

4. **Run the Application**:
   ```bash
   python app.py
   ```

5. **Access the Application**:
   Open your browser and go to `http://localhost:5000`

## Usage

### For Users
1. **Start Screen**: Click "Start Learning" to begin
2. **Language Selection**: Choose between French or English
3. **Study Mode**: Practice vocabulary with interactive flashcards
4. **Progress Tracking**: Monitor your learning progress and score

### For Administrators
Use the database management script to manage flashcards:

```bash
python manage_db.py
```

**Available Operations**:
- View all cards (French/English)
- Add new cards
- Search cards
- Delete cards
- Import/Export CSV files
- Backup/Restore databases

## File Structure

```
FlashCard/
├── app.py                 # Main Flask application
├── models.py             # Database models and setup
├── manage_db.py          # Database management script
├── test_setup.py         # Database initialization test
├── requirements.txt      # Python dependencies
├── static/               # CSS and JavaScript files
│   ├── style.css        # Application styles
│   └── app.js           # Frontend functionality
├── templates/            # HTML templates
│   └── base.html        # Main application template
├── Flashcard_FR.db      # French flashcards database
├── Flashcard_EN.db      # English flashcards database
└── README.md            # This file
```

## Adding New Languages

To add support for a new language:

1. **Create New Model Class** in `models.py`:
   ```python
   class Flashcard_XX(Base):
       __tablename__ = 'flashcards'
       id = Column(Integer, primary_key=True)
       # Define your language-specific fields
   ```

2. **Add Database Engine**:
   ```python
   DATABASE_URL_XX = 'sqlite:///Flashcard_XX.db'
   engine_xx = create_engine(DATABASE_URL_XX, echo=False)
   ```

3. **Update Session Factory**:
   ```python
   SessionLocal_XX = sessionmaker(autocommit=False, autoflush=False, bind=engine_xx)
   ```

4. **Add Routes** in `app.py`:
   ```python
   @app.route('/select_language_xx', methods=['POST'])
   def select_language_xx():
       # Implementation
   ```

5. **Update Frontend** in `base.html`:
   Add language selection option and study interface

## Sample Data

The application comes with pre-loaded sample vocabulary:

- **French**: 80+ words covering greetings, politeness, conversation, numbers, verbs, adjectives, food, and places
- **English**: 50+ words covering greetings, politeness, basic words, numbers, verbs, adjectives, food, and places

## Technical Details

- **Framework**: Flask 3.0.0
- **Database**: SQLite with SQLAlchemy ORM
- **Performance**: Server-side caching system with 50-card batches
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Custom CSS with responsive design
- **Session Management**: Flask sessions for user state

### Performance Optimizations

The application uses an intelligent caching system to dramatically improve performance:

- **50-Card Batches**: Cards are loaded in batches of 50 from the database
- **Server-Side Cache**: All card data is cached in server memory for instant access
- **Smart Refresh**: Cache automatically refreshes when all cards are used
- **Database Query Reduction**: From 3+ queries per interaction to 1 query per 50 interactions
- **Performance Improvement**: **~50x faster** for card operations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.
