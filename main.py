from flask import Flask, request
from flask_caching import Cache
import spacy
import pytextrank

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("textrank")

@app.route('/process-reviews', methods=['POST'])
@cache.cached(timeout=60*60*24, key_prefix=lambda: request.data)
def process_text():
    text = request.json['text']

    if (text is None):
        return {'phrases': []}

    doc = nlp(text)

    phrases = [phrase.text for phrase in doc._.phrases[:10]]

    filter_phrases(phrases)

    return {'phrases': phrases}

def filter_phrases(phrases):
    for phrase in phrases:
        if (phrase == ''):
            phrases.remove(phrase)
            
        if (len(phrase.split()) < 2):
            phrases.remove(phrase)

if __name__ == '__main__':
    app.run(port=8001, debug=True)
