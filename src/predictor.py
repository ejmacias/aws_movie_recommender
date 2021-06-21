import pandas as pd
from collections import defaultdict
from surprise import dump

# TO BE REMOVED =====================
USER_ID = '2'
# ===================================

# Paths
MOVIES_PATH = './data/movies.csv'
MODEL_PATH = './model/Recommender_Model'


# Dictionary with movie Ids and titles
movies = pd.read_csv(MOVIES_PATH, usecols=[0,1], index_col=0, squeeze=True).to_dict()

# Function that returns the top-n recommended movies given a list of predictions
def get_top_n(predictions, n=10):
    # First map the predictions to each user.
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        top_n[uid].append((movies[int(iid)], est))

    # Then sort the predictions for each user and retrieve the k highest ones.
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]

    return top_n


# Load recommender system model and predictions
print('Loading model ...')
full_predictions, recommender_model = dump.load(MODEL_PATH)

# Filter predictions for the given user
user_predictions = [prediction for prediction in full_predictions if prediction.uid == USER_ID]

# Get top recommended movies
top_ratings = get_top_n(user_predictions, n=10)
recommended_movies = [movie[0] for movie in top_ratings[USER_ID]]

print(f'Top recommendations: {recommended_movies}')
