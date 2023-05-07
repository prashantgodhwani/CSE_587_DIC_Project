import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from geopy.distance import geodesic
from sklearn.preprocessing import LabelEncoder
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from geopy.distance import geodesic
import numpy as np

# Creating class contentrec_loc taking input arguments cosine_sim, latitude, longitude, restaurant review, business
class ContentBased_locRS():
    def __init__(self, data, bus):
        self.data = data
        self.bus = bus
        stop_words = set(stopwords.words('english'))
        self.bus['text'] = self.bus['text'].apply(
            lambda x: ' '.join([word for word in x.split() if word.lower() not in stop_words]))
        features = ["categories", "cuisines", "text", "stars_scaled"]

        self.bus['stars_scaled'] = (self.bus['stars'] - self.bus['stars'].min()) / (
                    self.bus['stars'].max() - self.bus['stars'].min())
        self.bus["combined_features"] = self.bus[features].apply(lambda x: " ".join(x.dropna().astype(str)), axis=1)

        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(self.bus["combined_features"])

        cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
        self.cosine_sim = cosine_sim

    def get_recommendations(self, bid, lat, lon, top_n=20):
        data = self.bus
        top_lst = []
        top_dict = {}
        for i in bid:
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
            result = data.sort_values('distance').head(30)
            # Get the index of the business that matches the title
            idx = data[data['business_id'] == i].index[0]
            sim_scores = list(enumerate(self.cosine_sim[idx]))
            sim_s = [i for i in sim_scores if i[0] in list(result.index)]
            sim_s = sorted(sim_s, key=lambda x: x[1], reverse=True)
            top_n_scores = sim_s[1: top_n + 1]
            top_n_indices = [i[0] for i in top_n_scores]

            # appending name and business_ids of tep recommended restaurts to top_res dictionry
            top_lst = data.iloc[top_n_indices][["name", "business_id", 'latitude', 'longitude', "distance","categories"]]
            scores = [i[1] for i in sim_s[1: top_n + 1]]
            min_score = np.min(scores)
            max_score = np.max(scores)
            scaled_scores = np.round((scores - min_score) / (max_score - min_score) * 100, 2)

            top_dict['scores']=scaled_scores
            top_dict['name'] = data.iloc[top_n_indices]["name"]
            top_dict['business_id'] = data.iloc[top_n_indices]["business_id"]
            top_dict['distance'] = data.iloc[top_n_indices]["distance"]
            top_dict['latitude'] = data.iloc[top_n_indices]["latitude"]
            top_dict['longitude'] = data.iloc[top_n_indices]["longitude"]
            top_dict['tags'] = data.iloc[top_n_indices]["categories"]
        return top_dict, top_lst

    def fit(self, uid, lat, lon):
        data = self.data
        user_data = data[(data['user_id'] == uid) & (data['stars_x'] >= 3)]
        user_data = user_data.sort_values(by='stars_x', ascending=False)
        bid = user_data['business_id'].tolist()[:1]
        output, rec = self.get_recommendations(bid, lat, lon)
        rec=pd.DataFrame(rec)
        rec['scores']=output['scores']
        return output, rec.head(10)

