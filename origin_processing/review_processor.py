from pathlib import Path
import os

import spacy
from spacy.tokens import Span
from textblob import TextBlob


BASE_DIR = Path(__file__).resolve().parent.parent

if not Span.has_extension("sentiment"):
    Span.set_extension("sentiment", default=None)

def stream_review(file_path):
    with open(os.path.join(BASE_DIR, file_path), "r", encoding="utf-8") as file:
        review_text = file.read()
        encoded_bytes = review_text.encode('utf-8', errors='ignore')
        nuanced_review = encoded_bytes.decode('ascii', errors='ignore')

    lines = nuanced_review.split('\n')
    process_review = [
        line.strip().replace("=", "") for line in lines if len(line.strip()) > 0
    ]

    return nuanced_review, process_review

def sentiment_review(process_review):
    for sent in process_review.sents:
        blob = TextBlob(sent.text)
        # Normalize polarity to range [0, 1]
        normalized_sentiment = (blob.sentiment.polarity + 1) / 2
        sent._.sentiment = normalized_sentiment
    return process_review

@spacy.language.Language.component("sentiment_review")
def sentiment_component(process_review):
    return sentiment_review(process_review)