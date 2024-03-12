from textblob import TextBlob
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer

# Spelling autocorrection using TextBlob
def correct_spelling(text):
    blob = TextBlob(text)
    corrected_text = str(blob.correct())
    return corrected_text

# Sentence tokenization using NLTK
def tokenize_sentences(text):
    sentences = sent_tokenize(text)
    return sentences

# Text preprocessing: Lowercasing, removing punctuation, and stopwords
def preprocess_text(text):
    text = text.lower()
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(text)
    tokens = [token for token in tokens if token not in stop_words]
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
    preprocessed_text = ' '.join(lemmatized_tokens)
    return preprocessed_text


