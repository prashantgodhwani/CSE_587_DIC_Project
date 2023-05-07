import pandas as pd
from collections import Counter
import math
import numpy as np
import pandas as pd
from lightfm import LightFM
import scipy
import time
import math
from lightfm.data import Dataset
from tqdm import tqdm

class Hybrid_rec():
    def __init__(self, data1, data2):
        self.data1 = pd.read_csv(data1)
        self.data2 = pd.read_csv(data2)
        self.data_set = Dataset()
        self.data_set.fit(self.data2.user_id, self.data1.business_id)
        self.data_set.fit_partial(items=self.data1.business_id,
                                  item_features=['stars', 'review_count'])
        item_cols = [x for x in self.data1.columns[21:]]
        self.data_set.fit_partial(items=self.data1.business_id, item_features=item_cols)
        user_1 = [x for x in self.data2.columns[29:]]
        self.data_set.fit_partial(users=self.data2.user_id,
                                  user_features=user_1)
        (self.interactions, weights) = self.data_set.build_interactions(
            [(x['user_id'], x['business_id'], x[['stars_x']]) for index, x in self.data2.iterrows()])

        star_max = self.data1.stars.max()
        max_item = self.data1.review_count.max()
        max_u_rc = self.data2.review_count.max()
        max_useful = self.data2.useful.max()
        item_features_data = []
        for index, x in self.data1.iterrows():
            feature_dict = {
                'stars': 0.8 * x['stars'] / star_max,
                'review_count': 0.2 * x['review_count'] / max_item,
            }
            feature_dict.update(
                self.item(x, item_cols, [0.5 * x['stars'] / star_max, 0.5 * x['review_count'] / max_item]))
            item_features_data.append((x['business_id'], feature_dict))
        self.item_features = self.data_set.build_item_features(tqdm(item_features_data, desc="Building item features"))
        user_features_data = []
        for index, x in self.data2.iterrows():
            feature_dict = {
                'user_rc': 0.7 * x['user_rc'] / max_u_rc,
                'user_useful': 0.3 * x['user_useful'] / max_useful,
            }
            feature_dict.update(
                self.user_dict(x, user_1, [0.7 * x['user_rc'] / max_u_rc, 0.3 * x['user_useful'] / max_useful]))
            user_features_data.append((x['user_id'], feature_dict))
        self.user_features = self.data_set.build_user_features(tqdm(user_features_data, desc="Building user features"))
        num_threads = 5
        num_components = 50
        learning_rate = 0.1
        num_epochs = 1
        item_alpha = 1e-05
        self.model = LightFM(loss='logistic', item_alpha=item_alpha, random_state=69, no_components=num_components,
                             learning_rate=learning_rate)
        self.model = self.model.fit(self.interactions, user_features=self.user_features,
                                    item_features=self.item_features, epochs=num_epochs, num_threads=num_threads)

    def item(self, df, item_cols, values):
        output = {}
        for col in item_cols:
            output.update({col: df[col]})
        sum_val = sum(float(value) for value in output.values())  # get sum of all the tfidf values

        if (sum_val == 0):
            return output
        else:
            for key, value in output.items():
                output[key] = value / sum_val
        return output

    def user_dict(self, df, item_cols, values):
        output = {}
        for col in item_cols:
            output.update({col: df[col]})
        sum_val = sum(list(output.values()))

        if (sum_val == 0):
            return output
        else:
            for key, value in output.items():
                output[key] = value / sum_val
        return output

    def recommend(self, user_ids, k, columns=['name', 'latitude', 'longitude','categories', 'business_id'], num_threads=2):
        user_index = [self.data_set.mapping()[0][user_ids]]
        user_features = self.user_features
        item_features = self.item_features
        # mapping = self.data_set.mapping()[2]
        data_meta = self.data1
        train = self.interactions
        n_users, n_items = train.shape
        model = self.model

        for user_id in user_index:
            scores = model.predict(user_id, np.arange(n_items), user_features=user_features,
                                   item_features=item_features, num_threads=num_threads)
            item_ids = np.argsort(-scores)[:k]
            top_items = data_meta.iloc[item_ids][columns]
            min_score = np.min(scores)
            max_score = np.max(scores)
            scaled_scores = np.round((scores - min_score) / (max_score - min_score) * 100,2)
            top_items['scores']=scaled_scores[item_ids]
            top_items['scores'] = top_items['scores'].apply(lambda x: round(x, 2))

        return pd.DataFrame(top_items)








