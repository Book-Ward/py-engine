from flask import Flask, request
import spacy
import pytextrank

app = Flask(__name__)

nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("textrank")

@app.route('/process-reviews', methods=['POST'])
def process_text():
    text = request.json['text']
    doc = nlp(text)
    phrases = [phrase.text for phrase in doc._.phrases[:10]]
    return {'phrases': phrases}

if __name__ == '__main__':
    app.run()
