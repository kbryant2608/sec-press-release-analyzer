# src/text_analysis.py

import re
from typing import List, Tuple
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer

# Ensure you have downloaded these in your setup cell:
# nltk.download("vader_lexicon")
# nltk.download("stopwords")

def clean_text(text: str) -> str:
    """
    Lowercase the text, remove non-alphanumeric (except spaces),
    collapse multiple spaces, and strip leading/trailing whitespace.
    """
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def analyze_sentiment(text: str) -> dict:
    """
    Return VADER sentiment scores (neg/neu/pos/compound).
    """
    sia = SentimentIntensityAnalyzer()
    return sia.polarity_scores(text)

def extract_top_keywords(
    docs: List[str],
    top_n: int = 10
) -> List[Tuple[str, float]]:
    """
    Given a list of documents, compute TF-IDF and return the
    top_n terms (with their scores) for the concatenated corpus.
    """
    # Build TF-IDF model
    vectorizer = TfidfVectorizer(
        stop_words=stopwords.words("english"),
        ngram_range=(1,1),
        max_features=5000,
    )
    tfidf = vectorizer.fit_transform(docs)
    feature_array = vectorizer.get_feature_names_out()
    # Sum up TF-IDF scores across the corpus
    sums = tfidf.sum(axis=0).A1
    term_scores = list(zip(feature_array, sums))
    # Sort descending by score and return top_n
    top = sorted(term_scores, key=lambda x: x[1], reverse=True)[:top_n]
    return top
