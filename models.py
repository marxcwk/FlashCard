from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import os

# Database setup
DATABASE_URL = 'sqlite:///flashcards.db'
engine = create_engine(DATABASE_URL, echo=False)  # Set echo=True for debugging
Base = declarative_base()

class Flashcard(Base):
    __tablename__ = 'flashcards'
    
    id = Column(Integer, primary_key=True)
    french = Column(String(100), nullable=False)
    english = Column(String(100), nullable=False)
    ipa = Column(String(100))
    category = Column(String(50), default='General')
    wordType = Column(String(50), default='Not specified')
    level = Column(String(2), default='XX')
    notes = Column(Text)  # Added notes field
    created_at = Column(DateTime, default=datetime.utcnow)

# Create all tables
def create_tables():
    Base.metadata.create_all(engine)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Database session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize database with sample data
def init_db():
    create_tables()
    
    # Check if database is empty
    db = SessionLocal()
    try:
        existing_cards = db.query(Flashcard).count()
        if existing_cards == 0:
            # Add sample French vocabulary with new structure
            sample_cards = [
                # Greetings
                Flashcard(french="Bonjour", english="Hello", ipa="bɔ̃ʒuʁ", category="Greetings", wordType="Interjection", level="A1", notes="Formal greeting, used throughout the day"),
                Flashcard(french="Salut", english="Hi", ipa="saly", category="Greetings", wordType="Interjection", level="A1", notes="Informal greeting among friends"),
                Flashcard(french="Bonsoir", english="Good evening", ipa="bɔ̃swaʁ", category="Greetings", wordType="Interjection", level="A1", notes="Evening greeting"),
                Flashcard(french="Bonne nuit", english="Good night", ipa="bɔn nɥi", category="Greetings", wordType="Phrase", level="A1", notes="Night farewell"),
                Flashcard(french="Au revoir", english="Goodbye", ipa="o ʁəvwaʁ", category="Greetings", wordType="Phrase", level="A1", notes="Standard farewell"),
                
                # Politeness
                Flashcard(french="Merci", english="Thank you", ipa="mɛʁsi", category="Politeness", wordType="Interjection", level="A1", notes="Most common way to say thank you"),
                Flashcard(french="Merci beaucoup", english="Thank you very much", ipa="mɛʁsi boku", category="Politeness", wordType="Phrase", level="A1", notes="Emphasized gratitude"),
                Flashcard(french="De rien", english="You're welcome", ipa="də ʁjɛ̃", category="Politeness", wordType="Phrase", level="A1", notes="Response to thank you"),
                Flashcard(french="S'il vous plaît", english="Please", ipa="sil vu plɛ", category="Politeness", wordType="Phrase", level="A1", notes="Very polite, formal"),
                Flashcard(french="Excusez-moi", english="Excuse me", ipa="ɛkskyze mwa", category="Politeness", wordType="Phrase", level="A1", notes="Getting attention or apologizing"),
                Flashcard(french="Pardon", english="Pardon me", ipa="paʁdɔ̃", category="Politeness", wordType="Interjection", level="A1", notes="Simple apology"),
                
                # Conversation
                Flashcard(french="Comment allez-vous?", english="How are you?", ipa="kɔmɑ̃ tale vu", category="Conversation", wordType="Question", level="A1", notes="Formal way to ask about well-being"),
                Flashcard(french="Ça va?", english="How are you?", ipa="sa va", category="Conversation", wordType="Question", level="A1", notes="Informal, casual way"),
                Flashcard(french="Ça va bien", english="It's going well", ipa="sa va bjɛ̃", category="Conversation", wordType="Phrase", level="A1", notes="Positive response"),
                Flashcard(french="Je ne comprends pas", english="I don't understand", ipa="ʒə nə kɔ̃pʁɑ̃ pa", category="Communication", wordType="Phrase", level="A2", notes="Essential phrase for learners"),
                Flashcard(french="Parlez-vous anglais?", english="Do you speak English?", ipa="paʁle vu ɑ̃glɛ", category="Communication", wordType="Question", level="A2", notes="Useful when in trouble"),
                
                # Introduction
                Flashcard(french="Je m'appelle", english="My name is", ipa="ʒə mapɛl", category="Introduction", wordType="Phrase", level="A1", notes="Self introduction"),
                Flashcard(french="Enchanté", english="Nice to meet you", ipa="ɑ̃ʃɑ̃te", category="Introduction", wordType="Adjective", level="A1", notes="Response to introduction"),
                Flashcard(french="Comment vous appelez-vous?", english="What's your name?", ipa="kɔmɑ̃ vu zaple vu", category="Introduction", wordType="Question", level="A1", notes="Asking someone's name"),
                
                # Questions
                Flashcard(french="Où est...?", english="Where is...?", ipa="u ɛ", category="Questions", wordType="Question", level="A1", notes="Location question"),
                Flashcard(french="Combien ça coûte?", english="How much does it cost?", ipa="kɔ̃bjɛ̃ sa kut", category="Questions", wordType="Question", level="A2", notes="Price question"),
                Flashcard(french="Qu'est-ce que c'est?", english="What is this?", ipa="kɛs kə sɛ", category="Questions", wordType="Question", level="A1", notes="Object identification"),
                Flashcard(french="Quelle heure est-il?", english="What time is it?", ipa="kɛl œʁ ɛtil", category="Questions", wordType="Question", level="A2", notes="Time question"),
                Flashcard(french="Pourquoi?", english="Why?", ipa="puʁkwa", category="Questions", wordType="Question", level="A2", notes="Reason question"),
                Flashcard(french="Comment?", english="How?", ipa="kɔmɑ̃", category="Questions", wordType="Question", level="A1", notes="Method question"),
                
                # Basic responses
                Flashcard(french="Oui", english="Yes", ipa="wi", category="Basic", wordType="Adverb", level="A1", notes="Simple affirmative"),
                Flashcard(french="Non", english="No", ipa="nɔ̃", category="Basic", wordType="Adverb", level="A1", notes="Simple negative"),
                Flashcard(french="Peut-être", english="Maybe", ipa="pøtɛtʁ", category="Basic", wordType="Adverb", level="A2", notes="Uncertainty expression"),
                Flashcard(french="Bien sûr", english="Of course", ipa="bjɛ̃ syʁ", category="Basic", wordType="Phrase", level="A2", notes="Confirmation"),
                
                # Time
                Flashcard(french="Maintenant", english="Now", ipa="mɛ̃tnɑ̃", category="Time", wordType="Adverb", level="A1", notes="Current moment"),
                Flashcard(french="Aujourd'hui", english="Today", ipa="oʒuʁdɥi", category="Time", wordType="Adverb", level="A1", notes="Current day"),
                Flashcard(french="Demain", english="Tomorrow", ipa="dəmɛ̃", category="Time", wordType="Adverb", level="A1", notes="Next day"),
                Flashcard(french="Hier", english="Yesterday", ipa="jɛʁ", category="Time", wordType="Adverb", level="A1", notes="Previous day"),
                Flashcard(french="Bientôt", english="Soon", ipa="bjɛ̃to", category="Time", wordType="Adverb", level="A2", notes="Near future"),
                Flashcard(french="Toujours", english="Always", ipa="tuʒuʁ", category="Time", wordType="Adverb", level="A2", notes="Frequency adverb"),
                
                # Days of the week
                Flashcard(french="Lundi", english="Monday", ipa="lœ̃di", category="Time", wordType="Noun", level="A1", notes="First day of week"),
                Flashcard(french="Mardi", english="Tuesday", ipa="maʁdi", category="Time", wordType="Noun", level="A1", notes="Second day of week"),
                Flashcard(french="Mercredi", english="Wednesday", ipa="mɛʁkʁədi", category="Time", wordType="Noun", level="A1", notes="Third day of week"),
                Flashcard(french="Jeudi", english="Thursday", ipa="ʒødi", category="Time", wordType="Noun", level="A1", notes="Fourth day of week"),
                Flashcard(french="Vendredi", english="Friday", ipa="vɑ̃dʁədi", category="Time", wordType="Noun", level="A1", notes="Fifth day of week"),
                Flashcard(french="Samedi", english="Saturday", ipa="samdi", category="Time", wordType="Noun", level="A1", notes="Sixth day of week"),
                Flashcard(french="Dimanche", english="Sunday", ipa="dimɑ̃ʃ", category="Time", wordType="Noun", level="A1", notes="Seventh day of week"),
                
                # Numbers
                Flashcard(french="Un", english="One", ipa="œ̃", category="Numbers", wordType="Number", level="A1", notes="Cardinal number, masculine"),
                Flashcard(french="Deux", english="Two", ipa="dø", category="Numbers", wordType="Number", level="A1", notes="Cardinal number"),
                Flashcard(french="Trois", english="Three", ipa="tʁwa", category="Numbers", wordType="Number", level="A1", notes="Cardinal number"),
                Flashcard(french="Quatre", english="Four", ipa="katʁ", category="Numbers", wordType="Number", level="A1", notes="Cardinal number"),
                Flashcard(french="Cinq", english="Five", ipa="sɛ̃k", category="Numbers", wordType="Number", level="A1", notes="Cardinal number"),
                Flashcard(french="Six", english="Six", ipa="sis", category="Numbers", wordType="Number", level="A1", notes="Cardinal number"),
                Flashcard(french="Sept", english="Seven", ipa="sɛt", category="Numbers", wordType="Number", level="A1", notes="Cardinal number"),
                Flashcard(french="Huit", english="Eight", ipa="ɥit", category="Numbers", wordType="Number", level="A1", notes="Cardinal number"),
                Flashcard(french="Neuf", english="Nine", ipa="nœf", category="Numbers", wordType="Number", level="A1", notes="Cardinal number"),
                Flashcard(french="Dix", english="Ten", ipa="dis", category="Numbers", wordType="Number", level="A1", notes="Cardinal number"),
                
                # Common verbs
                Flashcard(french="Être", english="To be", ipa="ɛtʁ", category="Verbs", wordType="Verb", level="A1", notes="Most important verb, irregular"),
                Flashcard(french="Avoir", english="To have", ipa="avwaʁ", category="Verbs", wordType="Verb", level="A1", notes="Essential verb, irregular"),
                Flashcard(french="Aller", english="To go", ipa="ale", category="Verbs", wordType="Verb", level="A1", notes="Movement verb, irregular"),
                Flashcard(french="Faire", english="To do/make", ipa="fɛʁ", category="Verbs", wordType="Verb", level="A1", notes="Very common verb, irregular"),
                Flashcard(french="Vouloir", english="To want", ipa="vulwaʁ", category="Verbs", wordType="Verb", level="A2", notes="Desire verb, irregular"),
                Flashcard(french="Pouvoir", english="To be able to", ipa="puvwaʁ", category="Verbs", wordType="Verb", level="A2", notes="Ability verb, irregular"),
                
                # Common adjectives
                Flashcard(french="Bon", english="Good", ipa="bɔ̃", category="Adjectives", wordType="Adjective", level="A1", notes="Positive quality, masculine"),
                Flashcard(french="Bonne", english="Good", ipa="bɔn", category="Adjectives", wordType="Adjective", level="A1", notes="Positive quality, feminine"),
                Flashcard(french="Mauvais", english="Bad", ipa="movɛ", category="Adjectives", wordType="Adjective", level="A1", notes="Negative quality, masculine"),
                Flashcard(french="Grand", english="Big/Tall", ipa="ɡʁɑ̃", category="Adjectives", wordType="Adjective", level="A1", notes="Size adjective, masculine"),
                Flashcard(french="Petit", english="Small/Short", ipa="pəti", category="Adjectives", wordType="Adjective", level="A1", notes="Size adjective, masculine"),
                Flashcard(french="Nouveau", english="New", ipa="nuvo", category="Adjectives", wordType="Adjective", level="A1", notes="Time adjective, masculine"),
                Flashcard(french="Vieux", english="Old", ipa="vjø", category="Adjectives", wordType="Adjective", level="A1", notes="Time adjective, masculine"),
                
                # Food and drink
                Flashcard(french="Pain", english="Bread", ipa="pɛ̃", category="Food", wordType="Noun", level="A1", notes="Basic food item"),
                Flashcard(french="Eau", english="Water", ipa="o", category="Food", wordType="Noun", level="A1", notes="Basic drink"),
                Flashcard(french="Café", english="Coffee", ipa="kafe", category="Food", wordType="Noun", level="A1", notes="Popular drink"),
                Flashcard(french="Vin", english="Wine", ipa="vɛ̃", category="Food", wordType="Noun", level="A2", notes="Alcoholic beverage"),
                Flashcard(french="Fromage", english="Cheese", ipa="fʁɔmaʒ", category="Food", wordType="Noun", level="A2", notes="Dairy product"),
                
                # Places
                Flashcard(french="Maison", english="House", ipa="mɛzɔ̃", category="Places", wordType="Noun", level="A1", notes="Living place"),
                Flashcard(french="Restaurant", english="Restaurant", ipa="ʁɛstɔʁɑ̃", category="Places", wordType="Noun", level="A1", notes="Eating place"),
                Flashcard(french="Hôtel", english="Hotel", ipa="otɛl", category="Places", wordType="Noun", level="A1", notes="Accommodation"),
                Flashcard(french="Banque", english="Bank", ipa="bɑ̃k", category="Places", wordType="Noun", level="A2", notes="Financial institution"),
                Flashcard(french="École", english="School", ipa="ekɔl", category="Places", wordType="Noun", level="A1", notes="Educational institution")
            ]
            
            db.add_all(sample_cards)
            db.commit()
            print(f"Added {len(sample_cards)} sample flashcards to database")
        else:
            print(f"Database already contains {existing_cards} flashcards")
            
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()
