import spacy
from spacy.tokens import Span
from textblob import TextBlob

# Load the English language model
nlp = spacy.load("en_core_web_sm")

# Register a custom extension for sentiment if not already registered


# Define the custom sentiment analyzer function
def sentiment_analyzer(doc):
    """
    Custom component for sentiment analysis using TextBlob.
    """
    for sent in doc.sents:
        blob = TextBlob(sent.text)
        # Normalize polarity to range [0, 1]
        normalized_sentiment = (blob.sentiment.polarity + 1) / 2
        sent._.sentiment = normalized_sentiment
    return doc

@spacy.language.Language.component("sentiment_analyzer")
def sentiment_component(doc):
    return sentiment_analyzer(doc)

nlp.add_pipe("sentiment_analyzer", last=True)

text = "I love spaCy! It's a great library for NLP tasks. However, sometimes it can be complex to use."

# Process the text
doc = nlp(text)

# Print sentiment for each sentence
for sent in doc.sents:
    print(f"Sentence: {sent.text}\nNormalized Sentiment: {sent._.sentiment:.2f}\n")
