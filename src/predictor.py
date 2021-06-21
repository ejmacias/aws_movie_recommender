import io
import os
#import pickle
import flask
from flask.wrappers import Response

import pandas as pd
from collections import defaultdict
from surprise import dump

# Path where SageMaker mounts data in our container
prefix = '/opt/ml/'
model_path = os.path.join(prefix, 'model', 'recommender_system')
max_user_id = 611


# Function that returns the top-n recommended movies given a list of predictions
def get_top_n(predictions, n=10):
    # First map the predictions to each user.
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        top_n[uid].append((int(iid), est))
    # Then sort the predictions for each user and retrieve the k highest ones.
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]
    return top_n


class ScoringService(object):
    # Where we keep the recommendation model and full predictions when they're loaded
    model = None
    predictions = None

    @classmethod
    def get_model(cls):
        """Get the model and predictions for this instance if not already loaded."""
        if cls.model == None:
            print('Loading model ...')
            cls.predictions, cls.model = dump.load(model_path)
            #with open(os.path.join(model_path, "decision-tree-model.pkl"), "rb") as inp:
            #    cls.model = pickle.load(inp)
        return cls.model, cls.predictions

    @classmethod
    def predict(cls, user_id):
        """For the input, do the predictions and return them.
        Args:
            input (a pandas dataframe): The data on which to do the predictions. There will be
                one prediction per row in the dataframe"""
        _, full_predictions = cls.get_model()
        user_predictions = [prediction for prediction in full_predictions if prediction.uid == user_id]
        top_recommendations = get_top_n(user_predictions, n=10)
        print(f'Top recommendations for user {user_id}: {top_recommendations}')
        return top_recommendations


# TO BE REMOVED =====================
#USER_ID = '2'
# ===================================

# Paths
#MOVIES_PATH = './data/movies.csv'
#model_path = './model/Recommender_Model'


# Dictionary with movie Ids and titles
#movies = pd.read_csv(MOVIES_PATH, usecols=[0,1], index_col=0, squeeze=True).to_dict()
# >>>>>> This must go to the Lambda function


# Load recommender system model and predictions
#print('Loading model ...')
#full_predictions, recommender_model = dump.load(model_path)

# Filter predictions for the given user
#user_predictions = [prediction for prediction in full_predictions if prediction.uid == USER_ID]

# Get top recommended movies
#top_ratings = get_top_n(user_predictions, n=10)
#recommended_movies = [movie[0] for movie in top_ratings[USER_ID]]


# The flask app for serving predictions
app = flask.Flask(__name__)


@app.route("/recommend/<user_id>', methods=["GET"])
def recommend(user_id):
    """Determine if the user is known and if so, get the predictions."""
    status = 200 if user_id in range(1, max_user_id + 1) else 404
    response = ScoringService.predict(user_id) if status == 200 else ""
    return flask.Response(response=response, status=status, mimetype="application/json")
