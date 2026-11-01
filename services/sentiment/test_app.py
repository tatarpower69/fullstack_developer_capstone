import unittest
from app import app, analyze

class SentimentTests(unittest.TestCase):
    def test_positive_negative_neutral_and_negation(self):
        for text,label in [('Fantastic services','positive'),('Terrible rude team','negative'),('I visited yesterday','neutral'),('not good','negative')]:
            self.assertEqual(analyze(text)['sentiment'],label)
    def test_empty_input_rejected(self):
        self.assertEqual(app.test_client().get('/analyze').status_code,400)
