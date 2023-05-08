import string
import pandas as pd
import random

class feedback():
    def __init__(self, bus, rest):
        # Initializing the class with the business and review dataset
        self.restaurants = pd.read_csv(bus)
        self.review = pd.read_csv(rest)
        self.rest = rest

    # Method to filter restaurants by cuisine
    def cusine(self, cuisine):
        cuisine_restaurants = self.restaurants[self.restaurants['cuisines'] == cuisine]
        return cuisine_restaurants

    # Method to add a new review to the dataset and update the content-based recommendations
    def add_to_df(self, uid, bid, date, stars, text):
        # Creating a new review dataframe
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

        # Adding the review to the review dataset and saving it to the csv file
        self.review = pd.concat([self.review, review])
        self.review.to_csv(self.rest, index=False)
        # Merging the review dataset with the restaurant dataset
        self.review = self.review.merge(self.restaurants, on='business_id', how='inner')
        self.review = self.review.drop(['Unnamed: 0_x', 'Unnamed: 0_y'], axis=1)
        # Grouping the reviews by business and merging them with the restaurant dataset
        grouped_bus = self.review.groupby('business_id')['text'].agg(lambda x: str(x))
        grouped_bus = pd.DataFrame(grouped_bus)
        grouped_bus = grouped_bus.reset_index()
        self.restaurants = self.restaurants.drop(
            ['Unnamed: 0', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'is_open'],
            axis=1)
        self.restaurants = self.restaurants.merge(grouped_bus, how='inner')
        # Dropping duplicates and resetting the index of the restaurant dataset
        self.restaurants.drop_duplicates(subset='business_id', keep="first", inplace=True)
        self.restaurants = self.restaurants.reset_index(drop=True)
        # Saving the updated restaurant dataset to the csv file
        self.restaurants.to_csv('static/business_content.csv', index=False)
        self.review.to_csv('static/rest_review_content.csv', index=False)