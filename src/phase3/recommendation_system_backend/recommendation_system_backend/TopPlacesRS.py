import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from geopy.distance import geodesic
from sklearn.preprocessing import LabelEncoder

def get_recommendations(uid, res, bus, lat, lon, cus = None):
    """
    This function generates restaurant recommendations based on user's location and their preferred cuisine.

    Args:
    - uid (str): user ID
    - res (pandas DataFrame): a DataFrame containing all restaurant data
    - bus (pandas DataFrame): a DataFrame containing all business data
    - lat (float): user's latitude
    - lon (float): user's longitude
    - cus (str): user's preferred cuisine

    Returns:
    - top_3_by_cuisine (pandas DataFrame): a DataFrame containing the top 3 recommended restaurants for each cuisine
    """
    if cus is not None:
        # if user specifies their preferred cuisine
        data=bus
        cus = cus.split(",")
        target_lat=lat
        target_long=lon
        distances = []
        # creating a column[Distance] in data which has the distances between restaurants and our location
        for j in range(len(data)):
            lat = data.iloc[j]['latitude']
            long = data.iloc[j]['longitude']
            dist = geodesic((float(target_lat), float(target_long)), (lat, long)).miles
            distances.append(dist)
        data['distance'] = distances
        # filtering restaurants by user's preferred cuisine
        result = data.sort_values('distance')
        result=result.loc[result['cuisines'].isin(cus)]
        # grouping by cuisine and returning top 3 recommendations for each cuisine
        top_3_by_cuisine = (result.groupby('cuisines').apply(lambda x: x.sort_values('distance').head(3)).reset_index(drop=True))
        return top_3_by_cuisine
    else:
        # if user does not specify their preferred cuisine, we use their past reviews to determine their preferred cuisine
        data = bus
        data1 = res
        df = data1[data1['user_id'] == uid]
        cus = df[df['stars_x'] >= 3].cuisines
        target_lat = lat
        target_long = lon
        distances = []
        # creating a column[Distance] in data which has the distances between restaurants and our location
        for j in range(len(data)):
            lat = data.iloc[j]['latitude']
            long = data.iloc[j]['longitude']
            dist = geodesic((float(target_lat), float(target_long)), (lat, long)).miles
            distances.append(dist)
        data['distance'] = distances

        # Sort the DataFrame by distance and return the top results
        result = data.sort_values('distance')
        result = result.loc[result['cuisines'].isin(cus)]
        # grouping by cuisine and returning top 3 recommendations for each cuisine
        top_3_by_cuisine = (
            result.groupby('cuisines').apply(lambda x: x.sort_values('distance').head(3)).reset_index(drop=True))
        return top_3_by_cuisine