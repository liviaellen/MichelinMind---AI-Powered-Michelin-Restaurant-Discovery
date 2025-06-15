import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from typing import List, Dict
import os
import joblib

class RestaurantRecommender:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        self.model_path = os.path.join(os.path.dirname(__file__), 'models')
        os.makedirs(self.model_path, exist_ok=True)

    def prepare_features(self, restaurants: List[Dict]) -> pd.DataFrame:
        """Prepare features for the recommendation model"""
        df = pd.DataFrame(restaurants)
        # Combine relevant text features
        df['text_features'] = df.apply(
            lambda x: f"{x['name']} {x['cuisine']} {x['description'] if 'description' in x else ''}",
            axis=1
        )
        return df

    def train(self, restaurants: List[Dict]):
        """Train the recommendation model"""
        df = self.prepare_features(restaurants)
        # Create TF-IDF matrix
        tfidf_matrix = self.vectorizer.fit_transform(df['text_features'])
        # Save the model
        joblib.dump(self.vectorizer, os.path.join(self.model_path, 'vectorizer.joblib'))
        return tfidf_matrix

    def get_recommendations(self, restaurant_id: str, restaurants: List[Dict], n_recommendations: int = 5):
        """Get restaurant recommendations"""
        # Load the model
        self.vectorizer = joblib.load(os.path.join(self.model_path, 'vectorizer.joblib'))

        # Prepare features
        df = self.prepare_features(restaurants)
        tfidf_matrix = self.vectorizer.transform(df['text_features'])

        # Find the index of the input restaurant
        restaurant_idx = df[df['_id'] == restaurant_id].index[0]

        # Calculate similarity scores
        similarity_scores = cosine_similarity(tfidf_matrix[restaurant_idx], tfidf_matrix).flatten()

        # Get top N recommendations (excluding the input restaurant)
        similar_indices = similarity_scores.argsort()[::-1][1:n_recommendations+1]

        # Return recommended restaurants
        recommendations = df.iloc[similar_indices].to_dict('records')
        return recommendations

    def save_model(self):
        """Save the model to disk"""
        joblib.dump(self.vectorizer, os.path.join(self.model_path, 'vectorizer.joblib'))

    def load_model(self):
        """Load the model from disk"""
        self.vectorizer = joblib.load(os.path.join(self.model_path, 'vectorizer.joblib'))
