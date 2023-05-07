import string
import pandas as pd
import random

class feedback():
    def __init__(self, bus, rest):
        self.restaurants = pd.read_csv(bus)
        self.review = pd.read_csv(rest)
        self.rest = rest

    def cusine(self, cuisine):
        cuisine_restaurants = self.restaurants[self.restaurants['cuisines'] == cuisine]
        return cuisine_restaurants

    def add_to_df(self, uid, bid, date, stars, text):
        review = pd.DataFrame({
            'business_id': bid,
            'user_id': uid,
            'stars': stars,
            'review_id': ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)),
            'date': date,
            'text': text,
            'useful': random.randint(0, 5),
            'funny': random.randint(0, 5),
            'cool': random.randint(0, 5),
        }, index=[0])

        self.review = pd.concat([self.review, review])
        self.review.to_csv(self.rest, index=False)
        self.review = self.review.merge(self.restaurants, on='business_id', how='inner')
        self.review = self.review.drop(['Unnamed: 0_x', 'Unnamed: 0_y'], axis=1)
        grouped_bus = self.review.groupby('business_id')['text'].agg(lambda x: str(x))
        grouped_bus = pd.DataFrame(grouped_bus)
        grouped_bus = grouped_bus.reset_index()
        self.restaurants = self.restaurants.drop(
            ['Unnamed: 0', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'is_open'],
            axis=1)
        self.restaurants = self.restaurants.merge(grouped_bus, how='inner')
        self.restaurants.drop_duplicates(subset='business_id', keep="first", inplace=True)
        self.restaurants = self.restaurants.reset_index(drop=True)
        self.restaurants.to_csv('static/business_content.csv', index=False)
        self.review.to_csv('static/rest_review_content.csv', index=False)