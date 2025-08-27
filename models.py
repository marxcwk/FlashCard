from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import os

# Database setup for multiple languages
DATABASE_URL_FR = 'sqlite:///Flashcard_FR.db'
DATABASE_URL_EN = 'sqlite:///Flashcard_EN.db'

# Create engines for both databases
engine_fr = create_engine(DATABASE_URL_FR, echo=False)
engine_en = create_engine(DATABASE_URL_EN, echo=False)

Base = declarative_base()

class Flashcard_FR(Base):
    __tablename__ = 'flashcards_fr'
    
    id = Column(Integer, primary_key=True)
    french = Column(String(100), nullable=False)
    english = Column(String(100), nullable=False)
    ipa = Column(String(100))
    category = Column(String(50), default='General')
    wordType = Column(String(50), default='Not specified')
    level = Column(String(2), default='XX')
    note1 = Column(Text)  # Added note field for m/f regular/irregular
    note2 = Column(Text)  # Added note field for foot note
    created_at = Column(DateTime, default=datetime.utcnow)

class Flashcard_EN(Base):
    __tablename__ = 'flashcards_en'
    
    id = Column(Integer, primary_key=True)
    english = Column(String(100), nullable=False)
    chinese = Column(String(100), nullable=False)
    ipa = Column(String(100))
    category = Column(String(50), default='General')
    wordType = Column(String(50), default='Not specified')
    notes = Column(Text)  # Added note field for additional information
    created_at = Column(DateTime, default=datetime.utcnow)

# Create all tables for both databases
def create_tables():
    Base.metadata.create_all(engine_fr)
    Base.metadata.create_all(engine_en)

# Create session factories for both databases
SessionLocal_FR = sessionmaker(autocommit=False, autoflush=False, bind=engine_fr)
SessionLocal_EN = sessionmaker(autocommit=False, autoflush=False, bind=engine_en)

# Database session dependency functions
def get_db_fr():
    db = SessionLocal_FR()
    try:
        yield db
    finally:
        db.close()

def get_db_en():
    db = SessionLocal_EN()
    try:
        yield db
    finally:
        db.close()

# Initialize database with sample data
def init_db():
    create_tables()
    
    # Initialize French database
    init_db_fr()
    
    # Initialize English database
    init_db_en()

def init_db_fr():
    """Initialize French database with sample data"""
    db = SessionLocal_FR()
    try:
        existing_cards = db.query(Flashcard_FR).count()
        if existing_cards == 0:
            # Add sample French vocabulary with new structure
            sample_cards = [
                # Greetings
                Flashcard_FR(french="Bonjour", english="Hello", ipa="bɔ̃ʒuʁ", category="Greetings", wordType="Interjection", level="A1", note1="Formal greeting, used throughout the day", note2=""),
                Flashcard_FR(french="Salut", english="Hi", ipa="saly", category="Greetings", wordType="Interjection", level="A1", note1="Informal greeting among friends", note2=""),
                Flashcard_FR(french="Bonsoir", english="Good evening", ipa="bɔ̃swaʁ", category="Greetings", wordType="Interjection", level="A1", note1="Evening greeting", note2=""),
                Flashcard_FR(french="Bonne nuit", english="Good night", ipa="bɔn nɥi", category="Greetings", wordType="Phrase", level="A1", note1="Night farewell", note2=""),
                Flashcard_FR(french="Au revoir", english="Goodbye", ipa="o ʁəvwaʁ", category="Greetings", wordType="Phrase", level="A1", note1="Standard farewell", note2=""),
                
                # Politeness
                Flashcard_FR(french="Merci", english="Thank you", ipa="mɛʁsi", category="Politeness", wordType="Interjection", level="A1", note1="Most common way to say thank you", note2=""),
                Flashcard_FR(french="Merci beaucoup", english="Thank you very much", ipa="mɛʁsi boku", category="Politeness", wordType="Phrase", level="A1", note1="Emphasized gratitude", note2=""),
                Flashcard_FR(french="De rien", english="You're welcome", ipa="də ʁjɛ̃", category="Politeness", wordType="Phrase", level="A1", note1="Response to thank you", note2=""),
                Flashcard_FR(french="S'il vous plaît", english="Please", ipa="sil vu plɛ", category="Politeness", wordType="Phrase", level="A1", note1="Very polite, formal", note2=""),
                Flashcard_FR(french="Excusez-moi", english="Excuse me", ipa="ɛkskyze mwa", category="Politeness", wordType="Phrase", level="A1", note1="Getting attention or apologizing", note2=""),
                Flashcard_FR(french="Pardon", english="Pardon me", ipa="paʁdɔ̃", category="Politeness", wordType="Interjection", level="A1", note1="Simple apology", note2=""),
                
                # Conversation
                Flashcard_FR(french="Comment allez-vous?", english="How are you?", ipa="kɔmɑ̃ tale vu", category="Conversation", wordType="Question", level="A1", note1="Formal way to ask about well-being", note2=""),
                Flashcard_FR(french="Ça va?", english="How are you?", ipa="sa va", category="Conversation", wordType="Question", level="A1", note1="Informal, casual way", note2=""),
                Flashcard_FR(french="Ça va bien", english="It's going well", ipa="sa va bjɛ̃", category="Conversation", wordType="Phrase", level="A1", note1="Positive response", note2=""),
                Flashcard_FR(french="Je ne comprends pas", english="I don't understand", ipa="ʒə nə kɔ̃pʁɑ̃ pa", category="Communication", wordType="Phrase", level="A2", note1="Essential phrase for learners", note2=""),
                Flashcard_FR(french="Parlez-vous anglais?", english="Do you speak English?", ipa="paʁle vu ɑ̃glɛ", category="Communication", wordType="Question", level="A2", note1="Useful when in trouble", note2=""),
                
                # Introduction
                Flashcard_FR(french="Je m'appelle", english="My name is", ipa="ʒə mapɛl", category="Introduction", wordType="Phrase", level="A1", note1="Self introduction", note2=""),
                Flashcard_FR(french="Enchanté", english="Nice to meet you", ipa="ɑ̃ʃɑ̃te", category="Introduction", wordType="Adjective", level="A1", note1="Response to introduction", note2=""),
                Flashcard_FR(french="Comment vous appelez-vous?", english="What's your name?", ipa="kɔmɑ̃ vu zaple vu", category="Introduction", wordType="Question", level="A1", note1="Asking someone's name", note2=""),
                
                # Questions
                Flashcard_FR(french="Où est...?", english="Where is...?", ipa="u ɛ", category="Questions", wordType="Question", level="A1", note1="Location question", note2=""),
                Flashcard_FR(french="Combien ça coûte?", english="How much does it cost?", ipa="kɔ̃bjɛ̃ sa kut", category="Questions", wordType="Question", level="A2", note1="Price question", note2=""),
                Flashcard_FR(french="Qu'est-ce que c'est?", english="What is this?", ipa="kɛs kə sɛ", category="Questions", wordType="Question", level="A1", note1="Object identification", note2=""),
                Flashcard_FR(french="Quelle heure est-il?", english="What time is it?", ipa="kɛl œʁ ɛtil", category="Questions", wordType="Question", level="A2", note1="Time question", note2=""),
                Flashcard_FR(french="Pourquoi?", english="Why?", ipa="puʁkwa", category="Questions", wordType="Question", level="A2", note1="Reason question", note2=""),
                Flashcard_FR(french="Comment?", english="How?", ipa="kɔmɑ̃", category="Questions", wordType="Question", level="A1", note1="Method question", note2=""),
                
                # Basic responses
                Flashcard_FR(french="Oui", english="Yes", ipa="wi", category="Basic", wordType="Adverb", level="A1", note1="Simple affirmative", note2=""),
                Flashcard_FR(french="Non", english="No", ipa="nɔ̃", category="Basic", wordType="Adverb", level="A1", note1="Simple negative", note2=""),
                Flashcard_FR(french="Peut-être", english="Maybe", ipa="pøtɛtʁ", category="Basic", wordType="Adverb", level="A2", note1="Uncertainty expression", note2=""),
                Flashcard_FR(french="Bien sûr", english="Of course", ipa="bjɛ̃ syʁ", category="Basic", wordType="Phrase", level="A2", note1="Confirmation", note2=""),
                
                # Time
                Flashcard_FR(french="Maintenant", english="Now", ipa="mɛ̃tnɑ̃", category="Time", wordType="Adverb", level="A1", note1="Current moment", note2=""),
                Flashcard_FR(french="Aujourd'hui", english="Today", ipa="oʒuʁdɥi", category="Time", wordType="Adverb", level="A1", note1="Current day", note2=""),
                Flashcard_FR(french="Demain", english="Tomorrow", ipa="dəmɛ̃", category="Time", wordType="Adverb", level="A1", note1="Next day", note2=""),
                Flashcard_FR(french="Hier", english="Yesterday", ipa="jɛʁ", category="Time", wordType="Adverb", level="A1", note1="Previous day", note2=""),
                Flashcard_FR(french="Bientôt", english="Soon", ipa="bjɛ̃to", category="Time", wordType="Adverb", level="A2", note1="Near future", note2=""),
                Flashcard_FR(french="Toujours", english="Always", ipa="tuʒuʁ", category="Time", wordType="Adverb", level="A2", note1="Frequency adverb", note2=""),
                
                # Days of the week
                Flashcard_FR(french="Lundi", english="Monday", ipa="lœ̃di", category="Time", wordType="Noun", level="A1", note1="First day of week", note2=""),
                Flashcard_FR(french="Mardi", english="Tuesday", ipa="maʁdi", category="Time", wordType="Noun", level="A1", note1="Second day of week", note2=""),
                Flashcard_FR(french="Mercredi", english="Wednesday", ipa="mɛʁkʁədi", category="Time", wordType="Noun", level="A1", note1="Third day of week", note2=""),
                Flashcard_FR(french="Jeudi", english="Thursday", ipa="ʒødi", category="Time", wordType="Noun", level="A1", note1="Fourth day of week", note2=""),
                Flashcard_FR(french="Vendredi", english="Friday", ipa="vɑ̃dʁədi", category="Time", wordType="Noun", level="A1", note1="Fifth day of week", note2=""),
                Flashcard_FR(french="Samedi", english="Saturday", ipa="samdi", category="Time", wordType="Noun", level="A1", note1="Sixth day of week", note2=""),
                Flashcard_FR(french="Dimanche", english="Sunday", ipa="dimɑ̃ʃ", category="Time", wordType="Noun", level="A1", note1="Seventh day of week", note2=""),
                
                # Numbers
                Flashcard_FR(french="Un", english="One", ipa="œ̃", category="Numbers", wordType="Number", level="A1", note1="Cardinal number, masculine", note2=""),
                Flashcard_FR(french="Deux", english="Two", ipa="dø", category="Numbers", wordType="Number", level="A1", note1="Cardinal number", note2=""),
                Flashcard_FR(french="Trois", english="Three", ipa="tʁwa", category="Numbers", wordType="Number", level="A1", note1="Cardinal number", note2=""),
                Flashcard_FR(french="Quatre", english="Four", ipa="katʁ", category="Numbers", wordType="Number", level="A1", note1="Cardinal number", note2=""),
                Flashcard_FR(french="Cinq", english="Five", ipa="sɛ̃k", category="Numbers", wordType="Number", level="A1", note1="Cardinal number", note2=""),
                Flashcard_FR(french="Six", english="Six", ipa="sis", category="Numbers", wordType="Number", level="A1", note1="Cardinal number", note2=""),
                Flashcard_FR(french="Sept", english="Seven", ipa="sɛt", category="Numbers", wordType="Number", level="A1", note1="Cardinal number", note2=""),
                Flashcard_FR(french="Huit", english="Eight", ipa="ɥit", category="Numbers", wordType="Number", level="A1", note1="Cardinal number", note2=""),
                Flashcard_FR(french="Neuf", english="Nine", ipa="nœf", category="Numbers", wordType="Number", level="A1", note1="Cardinal number", note2=""),
                Flashcard_FR(french="Dix", english="Ten", ipa="dis", category="Numbers", wordType="Number", level="A1", note1="Cardinal number", note2=""),
                
                # Common verbs
                Flashcard_FR(french="Être", english="To be", ipa="ɛtʁ", category="Verbs", wordType="Verb", level="A1", note1="Most important verb, irregular", note2=""),
                Flashcard_FR(french="Avoir", english="To have", ipa="avwaʁ", category="Verbs", wordType="Verb", level="A1", note1="Essential verb, irregular", note2=""),
                Flashcard_FR(french="Aller", english="To go", ipa="ale", category="Verbs", wordType="Verb", level="A1", note1="Movement verb, irregular", note2=""),
                Flashcard_FR(french="Faire", english="To do/make", ipa="fɛʁ", category="Verbs", wordType="Verb", level="A1", note1="Very common verb, irregular", note2=""),
                Flashcard_FR(french="Vouloir", english="To want", ipa="vulwaʁ", category="Verbs", wordType="Verb", level="A2", note1="Desire verb, irregular", note2=""),
                Flashcard_FR(french="Pouvoir", english="To be able to", ipa="puvwaʁ", category="Verbs", wordType="Verb", level="A2", note1="Ability verb, irregular", note2=""),
                
                # Common adjectives
                Flashcard_FR(french="Bon", english="Good", ipa="bɔ̃", category="Adjectives", wordType="Adjective", level="A1", note1="Positive quality, masculine", note2=""),
                Flashcard_FR(french="Bonne", english="Good", ipa="bɔn", category="Adjectives", wordType="Adjective", level="A1", note1="Positive quality, feminine", note2=""),
                Flashcard_FR(french="Mauvais", english="Bad", ipa="movɛ", category="Adjectives", wordType="Adjective", level="A1", note1="Negative quality, masculine", note2=""),
                Flashcard_FR(french="Grand", english="Big/Tall", ipa="ɡʁɑ̃", category="Adjectives", wordType="Adjective", level="A1", note1="Size adjective, masculine", note2=""),
                Flashcard_FR(french="Petit", english="Small/Short", ipa="pəti", category="Adjectives", wordType="Adjective", level="A1", note1="Size adjective, masculine", note2=""),
                Flashcard_FR(french="Nouveau", english="New", ipa="nuvo", category="Adjectives", wordType="Adjective", level="A1", note1="Time adjective, masculine", note2=""),
                Flashcard_FR(french="Vieux", english="Old", ipa="vjø", category="Adjectives", wordType="Adjective", level="A1", note1="Time adjective, masculine", note2=""),
                
                # Food and drink
                Flashcard_FR(french="Pain", english="Bread", ipa="pɛ̃", category="Food", wordType="Noun", level="A1", note1="Basic food item", note2=""),
                Flashcard_FR(french="Eau", english="Water", ipa="o", category="Food", wordType="Noun", level="A1", note1="Basic drink", note2=""),
                Flashcard_FR(french="Café", english="Coffee", ipa="kafe", category="Food", wordType="Noun", level="A1", note1="Popular drink", note2=""),
                Flashcard_FR(french="Vin", english="Wine", ipa="vɛ̃", category="Food", wordType="Noun", level="A2", note1="Alcoholic beverage", note2=""),
                Flashcard_FR(french="Fromage", english="Cheese", ipa="fʁɔmaʒ", category="Food", wordType="Noun", level="A2", note1="Dairy product", note2=""),
                
                # Places
                Flashcard_FR(french="Maison", english="House", ipa="mɛzɔ̃", category="Places", wordType="Noun", level="A1", note1="Living place", note2=""),
                Flashcard_FR(french="Restaurant", english="Restaurant", ipa="ʁɛstɔʁɑ̃", category="Places", wordType="Noun", level="A1", note1="Eating place", note2=""),
                Flashcard_FR(french="Hôtel", english="Hotel", ipa="otɛl", category="Places", wordType="Noun", level="A1", note1="Accommodation", note2=""),
                Flashcard_FR(french="Banque", english="Bank", ipa="bɑ̃k", category="Places", wordType="Noun", level="A2", note1="Financial institution", note2=""),
                Flashcard_FR(french="École", english="School", ipa="ekɔl", category="Places", wordType="Noun", level="A1", note1="Educational institution", note2="")
            ]
            
            db.add_all(sample_cards)
            db.commit()
            print(f"Added {len(sample_cards)} sample French flashcards to database")
        else:
            print(f"French database already contains {existing_cards} flashcards")
            
    except Exception as e:
        print(f"Error initializing French database: {e}")
        db.rollback()
    finally:
        db.close()

def init_db_en():
    """Initialize English database with sample data"""
    db = SessionLocal_EN()
    try:
        existing_cards = db.query(Flashcard_EN).count()
        if existing_cards == 0:
            # Add sample English vocabulary with Chinese translations
            sample_cards = [
                # Greetings
                Flashcard_EN(english="Hello", chinese="你好", ipa="həˈloʊ", category="Greetings", wordType="Interjection", notes="Formal greeting"),
                Flashcard_EN(english="Hi", chinese="嗨", ipa="haɪ", category="Greetings", wordType="Interjection", notes="Informal greeting"),
                Flashcard_EN(english="Good morning", chinese="早上好", ipa="ɡʊd ˈmɔrnɪŋ", category="Greetings", wordType="Phrase", notes="Morning greeting"),
                Flashcard_EN(english="Good afternoon", chinese="下午好", ipa="ɡʊd ˌæftərˈnun", category="Greetings", wordType="Phrase", notes="Afternoon greeting"),
                Flashcard_EN(english="Good evening", chinese="晚上好", ipa="ɡʊd ˈivnɪŋ", category="Greetings", wordType="Phrase", notes="Evening greeting"),
                Flashcard_EN(english="Goodbye", chinese="再见", ipa="ˌɡʊdˈbaɪ", category="Greetings", wordType="Interjection", notes="Farewell"),
                
                # Politeness
                Flashcard_EN(english="Thank you", chinese="谢谢", ipa="ˈθæŋk ju", category="Politeness", wordType="Phrase", notes="Expression of gratitude"),
                Flashcard_EN(english="You're welcome", chinese="不客气", ipa="jʊr ˈwɛlkəm", category="Politeness", wordType="Phrase", notes="Response to thank you"),
                Flashcard_EN(english="Please", chinese="请", ipa="pliz", category="Politeness", wordType="Interjection", notes="Polite request"),
                Flashcard_EN(english="Excuse me", chinese="对不起", ipa="ɪkˈskjuz mi", category="Politeness", wordType="Phrase", notes="Apology or getting attention"),
                Flashcard_EN(english="Sorry", chinese="抱歉", ipa="ˈsɑri", category="Politeness", wordType="Adjective", notes="Apology"),
                
                # Basic words
                Flashcard_EN(english="Yes", chinese="是", ipa="jɛs", category="Basic", wordType="Adverb", notes="Affirmative response"),
                Flashcard_EN(english="No", chinese="不", ipa="noʊ", category="Basic", wordType="Adverb", notes="Negative response"),
                Flashcard_EN(english="Maybe", chinese="也许", ipa="ˈmeɪbi", category="Basic", wordType="Adverb", notes="Uncertainty"),
                Flashcard_EN(english="Of course", chinese="当然", ipa="əv ˈkɔrs", category="Basic", wordType="Phrase", notes="Confirmation"),
                
                # Numbers
                Flashcard_EN(english="One", chinese="一", ipa="wʌn", category="Numbers", wordType="Number", notes="Cardinal number"),
                Flashcard_EN(english="Two", chinese="二", ipa="tu", category="Numbers", wordType="Number", notes="Cardinal number"),
                Flashcard_EN(english="Three", chinese="三", ipa="θri", category="Numbers", wordType="Number", notes="Cardinal number"),
                Flashcard_EN(english="Four", chinese="四", ipa="fɔr", category="Numbers", wordType="Number", notes="Cardinal number"),
                Flashcard_EN(english="Five", chinese="五", ipa="faɪv", category="Numbers", wordType="Number", notes="Cardinal number"),
                
                # Common verbs
                Flashcard_EN(english="To be", chinese="是", ipa="tu bi", category="Verbs", wordType="Verb", notes="Most important verb"),
                Flashcard_EN(english="To have", chinese="有", ipa="tu hæv", category="Verbs", wordType="Verb", notes="Possession verb"),
                Flashcard_EN(english="To go", chinese="去", ipa="tu ɡoʊ", category="Verbs", wordType="Verb", notes="Movement verb"),
                Flashcard_EN(english="To come", chinese="来", ipa="tu kʌm", category="Verbs", wordType="Verb", notes="Movement verb"),
                Flashcard_EN(english="To do", chinese="做", ipa="tu du", category="Verbs", wordType="Verb", notes="Action verb"),
                
                # Common adjectives
                Flashcard_EN(english="Good", chinese="好", ipa="ɡʊd", category="Adjectives", wordType="Adjective", notes="Positive quality"),
                Flashcard_EN(english="Bad", chinese="坏", ipa="bæd", category="Adjectives", wordType="Adjective", notes="Negative quality"),
                Flashcard_EN(english="Big", chinese="大", ipa="bɪɡ", category="Adjectives", wordType="Adjective", notes="Size adjective"),
                Flashcard_EN(english="Small", chinese="小", ipa="smɔl", category="Adjectives", wordType="Adjective", notes="Size adjective"),
                Flashcard_EN(english="New", chinese="新", ipa="nu", category="Adjectives", wordType="Adjective", notes="Time adjective"),
                Flashcard_EN(english="Old", chinese="旧", ipa="oʊld", category="Adjectives", wordType="Adjective", notes="Time adjective"),
                
                # Food and drink
                Flashcard_EN(english="Water", chinese="水", ipa="ˈwɔtər", category="Food", wordType="Noun", notes="Basic drink"),
                Flashcard_EN(english="Bread", chinese="面包", ipa="brɛd", category="Food", wordType="Noun", notes="Basic food"),
                Flashcard_EN(english="Rice", chinese="米饭", ipa="raɪs", category="Food", wordType="Noun", notes="Staple food"),
                Flashcard_EN(english="Tea", chinese="茶", ipa="ti", category="Food", wordType="Noun", notes="Popular drink"),
                Flashcard_EN(english="Coffee", chinese="咖啡", ipa="ˈkɔfi", category="Food", wordType="Noun", notes="Popular drink"),
                
                # Places
                Flashcard_EN(english="House", chinese="房子", ipa="haʊs", category="Places", wordType="Noun", notes="Living place"),
                Flashcard_EN(english="School", chinese="学校", ipa="skul", category="Places", wordType="Noun", notes="Educational institution"),
                Flashcard_EN(english="Hospital", chinese="医院", ipa="ˈhɑspɪtl", category="Places", wordType="Noun", notes="Medical facility"),
                Flashcard_EN(english="Restaurant", chinese="餐厅", ipa="ˈrɛstərɑnt", category="Places", wordType="Noun", notes="Eating place"),
                Flashcard_EN(english="Bank", chinese="银行", ipa="bæŋk", category="Places", wordType="Noun", notes="Financial institution")
            ]
            
            db.add_all(sample_cards)
            db.commit()
            print(f"Added {len(sample_cards)} sample English flashcards to database")
        else:
            print(f"English database already contains {existing_cards} flashcards")
            
    except Exception as e:
        print(f"Error initializing English database: {e}")
        db.rollback()
    finally:
        db.close()
