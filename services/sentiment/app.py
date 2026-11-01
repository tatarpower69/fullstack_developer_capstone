"""A transparent local lexicon baseline, not an IBM Watson model."""
import re
import os
from flask import Flask, jsonify, request
app = Flask(__name__)
POSITIVE = {'fantastic', 'excellent', 'great', 'good', 'love', 'friendly', 'amazing', 'helpful', 'smooth', 'best', 'wonderful'}
NEGATIVE = {'terrible', 'bad', 'awful', 'poor', 'hate', 'rude', 'worst', 'disappointed', 'horrible'}

def analyze(text):
    words = re.findall(r"[a-z']+", text.lower())
    score = 0
    for i, word in enumerate(words):
        value = int(word in POSITIVE) - int(word in NEGATIVE)
        if any(w in {'not', 'never', 'no'} for w in words[max(0, i-2):i]): value *= -1
        score += value
    return {'sentiment': 'positive' if score > 0 else 'negative' if score < 0 else 'neutral', 'score': score, 'model': 'local-lexicon-baseline'}

@app.get('/analyze')
def analyze_route():
    text = request.args.get('text', '')
    if not text.strip() or len(text) > 5000: return jsonify(error='Provide 1–5000 characters'), 400
    return jsonify(analyze(text))

@app.get('/analyze/<path:text>')
def analyze_path(text): return jsonify(analyze(text))

if __name__ == '__main__': app.run(host='127.0.0.1', port=int(os.environ.get('SENTIMENT_PORT', '5050')))
