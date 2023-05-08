import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class ContentBasedRS:
    def __init__(self, data):
        # Initializing the class with the given dataset
        self.df = data
        self.df['text'] = self.df['text'].fillna('')
        features = ['text', 'categories', 'cuisines']
        # Combining the features to create a new feature column
        self.df["combined_features"] = data[features].apply(lambda x: " ".join(x.dropna().astype(str)), axis=1)
        # Initializing a TfidfVectorizer and generating the tf-idf matrix
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = self.vectorizer.fit_transform(self.df["combined_features"])

    def recommend(self, text, top_n=10):
        # Transforming the given text to a tf-idf vector
        text_tfidf = self.vectorizer.transform([text])
        # Calculating cosine similarity between the given text vector and all vectors in the tf-idf matrix
        similarity_scores = cosine_similarity(text_tfidf, self.tfidf_matrix)[0]
        # Getting the indices of the top_n most similar items
        top_indices = similarity_scores.argsort()[::-1][:top_n]


        # Filtering the items with stars>=3, sorting them in descending order by stars and selecting top_n items
        output_data = self.df.iloc[top_indices][
            ['business_id', 'latitude', 'longitude', 'name', 'categories', 'cuisines', 'text', 'stars']]
        output_data = output_data[output_data['stars'] >= 3]
        output_data = output_data.sort_values(by='stars', ascending=False)
        # Scaling the similarity scores to a range of 0 to 100 and adding them as a new column
        scores = similarity_scores
        min_score = np.min(scores)
        max_score = np.max(scores)
        scaled_scores = np.round((scores - min_score) / (max_score - min_score) * 100, 2)
        l=len(output_data)
        output_data['scores'] = scaled_scores[top_indices[:l]]
        # Returning the recommended items with their details and similarity scores
        return output_data
