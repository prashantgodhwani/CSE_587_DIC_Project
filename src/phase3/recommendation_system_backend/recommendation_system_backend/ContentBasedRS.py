import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class ContentBasedRS:
    def __init__(self, data):
        self.df = data
        self.df['text'] = self.df['text'].fillna('')
        features = ['text', 'categories', 'cuisines']
        self.df["combined_features"] = data[features].apply(lambda x: " ".join(x.dropna().astype(str)), axis=1)
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = self.vectorizer.fit_transform(self.df["combined_features"])

    def recommend(self, text, top_n=10):
        text_tfidf = self.vectorizer.transform([text])
        similarity_scores = cosine_similarity(text_tfidf, self.tfidf_matrix)[0]
        top_indices = similarity_scores.argsort()[::-1][:top_n]

        output_data = self.df.iloc[top_indices][
            ['business_id', 'latitude', 'longitude', 'name', 'categories', 'cuisines', 'text', 'stars']]
        output_data = output_data[output_data['stars'] >= 3]
        output_data = output_data.sort_values(by='stars', ascending=False)
        scores = similarity_scores
        min_score = np.min(scores)
        max_score = np.max(scores)
        scaled_scores = np.round((scores - min_score) / (max_score - min_score) * 100, 2)
        l=len(output_data)
        output_data['scores'] = scaled_scores[top_indices[:l]]
        return output_data
