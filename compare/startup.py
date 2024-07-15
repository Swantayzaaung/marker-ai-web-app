import spacy

nlp = None

def load_model():
    global nlp
    nlp = spacy.load("en_core_web_lg")

load_model()