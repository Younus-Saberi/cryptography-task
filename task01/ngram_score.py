# ngram_score.py
import math
from collections import defaultdict

class NgramScore:
    """
    A class to score text based on n-gram (quadgram) frequencies.
    """
    def __init__(self, ngram_file='english_quadgrams.txt', sep=' '):
        self.ngrams = defaultdict(int)
        self.total_count = 0
        
        try:
            with open(ngram_file, 'r', encoding='utf-8') as f:
                for line in f:
                    key, count_str = line.split(sep)
                    count = int(count_str)
                    self.ngrams[key.upper()] = count
                    self.total_count += count
        except FileNotFoundError:
            print(f"Error: '{ngram_file}' not found.")
            print("Please download this file. A sample is provided in the instructions.")
            exit()
            
        self.ngram_len = len(key)
        
        # Calculate log probabilities for faster scoring
        self.log_probs = defaultdict(float)
        floor = math.log10(0.01 / self.total_count)
        
        for key, count in self.ngrams.items():
            self.log_probs[key] = math.log10(count / self.total_count)
        self.log_probs.default_factory = lambda: floor

    def score(self, text: str) -> float:
        """
        Calculates the fitness score of a text.
        Higher scores are better.
        """
        # Clean the text: uppercase and keep only alphabet
        cleaned_text = "".join(filter(str.isalpha, text)).upper()
        
        score = 0.0
        for i in range(len(cleaned_text) - self.ngram_len + 1):
            quadgram = cleaned_text[i:i + self.ngram_len]
            score += self.log_probs[quadgram]
            
        return score