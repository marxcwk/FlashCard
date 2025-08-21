# 📚 FlashCard WebApp

A modern, responsive flashcard web application built with Flask, featuring a beautiful UI and interactive functionality.

## ✨ Features

- **Create Flashcards**: Add new flashcards with questions and answers
- **Category Organization**: Organize flashcards by categories
- **Interactive Cards**: Flip cards to reveal answers
- **Review Tracking**: Track how many times you've reviewed each card
- **Responsive Design**: Works perfectly on desktop and mobile devices
- **Modern UI**: Beautiful gradient design with smooth animations
- **Real-time Updates**: Dynamic content updates without page refresh

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone or download the project files**

2. **Create a virtual environment**
   ```bash
   # On Windows
   python -m venv venv
   
   # On macOS/Linux
   python3 -m venv venv
   ```

3. **Activate the virtual environment**
   ```bash
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open your browser and navigate to**
   ```
   http://localhost:5000
   ```

## 📁 Project Structure

```
FlashCard/
├── app.py                 # Main Flask application
├── models.py              # Database models and setup
├── manage_db.py           # Database management script
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── static/               # Static assets
│   ├── style.css        # CSS styles
│   └── app.js           # JavaScript functionality
└── templates/            # HTML templates
    └── base.html        # Main HTML template
```

## 🛠️ How It Works

### Backend (Flask)
- **app.py**: Main Flask application with study session management
- **models.py**: SQLAlchemy database models and database initialization
- **Data Storage**: Flashcards are stored in SQLite database (`flashcards.db`)
- **API Endpoints**:
  - `GET /`: Display start screen
  - `POST /start_study`: Begin study session
  - `POST /submit_answer`: Submit answer for current card
  - `POST /next_card`: Move to next random card
  - `POST /get_hint`: Get hint for current card
  - `POST /reset_study`: Reset study session
  - `POST /go_to_start`: Return to start screen

### Frontend
- **HTML**: Semantic structure with Jinja2 templating
- **CSS**: Modern, responsive design with CSS Grid and Flexbox
- **JavaScript**: Interactive functionality for card management

## 🎨 Features in Detail

### Study Sessions
- **Random Card Selection**: Cards appear in random order for better learning
- **Progress Tracking**: Visual progress bar showing completion
- **Score Tracking**: Monitor correct answers throughout the session
- **Hint System**: Progressive hints that reveal letters gradually

### Database Management
- **SQLite Storage**: Persistent storage for all flashcards
- **Easy Management**: Use `python manage_db.py` to add/edit/delete cards
- **Categories**: Organize cards by categories (Greetings, Questions, etc.)
- **Scalable**: Easy to add hundreds of vocabulary words

### Learning Experience
- **Spaced Repetition Ready**: Database structure supports future spaced repetition
- **Random Order**: No memorization based on sequence
- **IPA Pronunciation**: Each card includes International Phonetic Alphabet pronunciation

### Responsive Design
- Mobile-first approach
- Adaptive grid layout
- Touch-friendly interface

## 🔧 Customization

### Adding New Categories
Categories are automatically generated based on the flashcards you create. Simply type a new category name when adding a card.

### Styling
Modify `static/style.css` to customize colors, fonts, and layout.

### Functionality
Extend `static/app.js` to add new interactive features.

## 🚀 Deployment

### Local Development
The app runs in debug mode by default, perfect for development.

### Production Deployment
For production, consider:
- Setting `debug=False` in `app.py`
- Using a production WSGI server (Gunicorn, uWSGI)
- Setting up environment variables for configuration
- Using a proper database instead of JSON files

## 🐛 Troubleshooting

### Common Issues

1. **Port already in use**
   - Change the port in `app.py`: `app.run(debug=True, port=5001)`

2. **Module not found errors**
   - Ensure virtual environment is activated
   - Run `pip install -r requirements.txt`

3. **Permission errors (Windows)**
   - Run PowerShell as Administrator
   - Or use: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

### Getting Help
- Check that all files are in the correct folders
- Verify Python version compatibility
- Ensure virtual environment is properly activated

## 📱 Browser Compatibility

- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve the application.

## 📄 License

This project is open source and available under the MIT License.

---

**Happy Studying! 📖✨**
