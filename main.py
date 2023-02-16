from flask import Flask, request
from flask_caching import Cache
import spacy
import pytextrank

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("textrank")

@app.route('/process-reviews', methods=['POST'])
@cache.cached(timeout=60*60, query_string=True)
def process_text():
    text = request.json['text']
    doc = nlp(text)
    phrases = [phrase.text for phrase in doc._.phrases[:10]]
    return {'phrases': phrases}

if __name__ == '__main__':
    app.run()
