import nltk
from textblob import TextBlob
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from summa import summarizer
from transformers import pipeline
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize

from text_preprocessing import preprocess_text
from text_preprocessing import tokenize_sentences
def summarize_text_tfidf(text, num_sentences=3):
    # Tokenize sentences
    sentences = tokenize_sentences(text)

    # Preprocess text
    preprocessed_text = preprocess_text(text)

    if len(sentences) < num_sentences:
        num_sentences = len(sentences)

    if num_sentences == 1:
        return [text]

    # Remove stopwords and create TF-IDF matrix
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(sentences)
    X = X.toarray()

    # Apply K-Means clustering
    if num_sentences <= len(sentences):
        kmeans = KMeans(n_clusters=num_sentences)
        kmeans.fit(X)

        # Get representative sentences from each cluster
        summarized_sentences = []
        for cluster_id in range(num_sentences):
            cluster_sentences = [sentences[i] for i, label in enumerate(kmeans.labels_) if label == cluster_id]
            summarized_sentences.append(cluster_sentences[0])

        return summarized_sentences
    else:
        return sentences[:num_sentences]

# Text summarization using TextRank algorithm
def summarize_textrank(text, ratio=0.3):
    sentences = sent_tokenize(text)
    
    stop_words = set(stopwords.words('english'))
    words = [word for sentence in sentences for word in word_tokenize(sentence) if word.lower() not in stop_words]
    
    stemmer = PorterStemmer()
    stemmed_words = [stemmer.stem(word) for word in words]
    
    word_freq = nltk.FreqDist(stemmed_words)
    
    ranked_sentences = [(sentence, sum(word_freq[stemmer.stem(word)] for word in word_tokenize(sentence) if word.lower() not in stop_words)) for sentence in sentences]
    ranked_sentences.sort(key=lambda x: x[1], reverse=True)
    
    num_sentences = int(len(sentences) * ratio)
    summary_sentences = [sentence for sentence, _ in ranked_sentences[:num_sentences]]
    summary = ' '.join(summary_sentences)
    
    return summary

#Summarization with pipeline
def summarize_pipeline(text, r):
    summarization = pipeline("summarization", model="facebook/bart-base")

    # Text chunking and summarization
    num_iters = int(len(text) / 1000)
    summarized_text = []

    for i in range(0, num_iters + 1):
        start = i * 1000
        end = (i + 1) * 1000
    
        # Perform summarization on each chunk
        chunk_summary = summarization(text[start:end], min_length=5, max_length= r, num_beams=4)
        chunk_summary = chunk_summary[0]['summary_text']
        summarized_text.append(chunk_summary)
    return summarized_text

def display_menu():
    print("Choose an option:")
    print("1. Summarize text with pipeline")
    print("2. Summarize text with TF-IDF")
    print("3. Summarize text with TextRank")
    print("4. Exit")

def summary(text):
    while True:
        display_menu()
        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            #Summarize the text using Pipeline
            r = int(input("Enter maximum length of the text you want : "))
            summary_pipe = summarize_pipeline(text, r)
            return summary_pipe

        elif choice == "2":
            # Summarize text using TF-IDF and K-Means clustering
            summary_tfidf = summarize_text_tfidf(text, num_sentences=2)
            return summary_tfidf

        elif choice == "3":
             # Summarize text using TextRank algorithm
            summary_tr = summarize_textrank(text)
            return summary_tr

        elif choice == "4":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 4.")