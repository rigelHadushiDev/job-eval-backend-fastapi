import re
import string
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from typing import List, Tuple

def clean_text(text: str) -> str:

    soup = BeautifulSoup(text, "html.parser")
    text = soup.get_text()
    
    text = text.translate(str.maketrans("", "", string.punctuation))

    tokens = word_tokenize(text)

    tokens = [t.lower() for t in tokens if t.isalpha()]

    stop_words = set(stopwords.words('english'))
    tokens = [t for t in tokens if t not in stop_words]

    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(t) for t in tokens]
    
    return ' '.join(tokens)

def get_embeddings(model, titles: List[str], texts: List[str]) -> Tuple[List, List]:
    clean_titles = [clean_text(t) for t in titles]
    clean_texts = [clean_text(t) for t in texts]
    
    title_embeddings = model.encode(clean_titles)
    text_embeddings = model.encode(clean_texts)
    
    return title_embeddings, text_embeddings