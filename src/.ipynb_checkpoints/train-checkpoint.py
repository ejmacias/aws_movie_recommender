# Import libraries
simport numpy as np
import pandas as pd
from keras.callbacks import Callback, EarlyStopping, ModelCheckpoint
# Import CF Model Architecture
from model import CFModel

# Define constants
K_FACTORS = 100 # The number of dimensional embeddings for movies and users
TEST_USER = 2000 # A random test user (user_id = 2000)

# Reading ratings file
ratings = pd.read_csv('data/ratings.csv', sep='\t', encoding='latin-1', 
                      usecols=['user_id', 'movie_id', 'user_emb_id', 'movie_emb_id', 'rating'])
max_userid = ratings['user_id'].drop_duplicates().max()
max_movieid = ratings['movie_id'].drop_duplicates().max()

# Reading users file
users = pd.read_csv('data/users.csv', sep='\t', encoding='latin-1', 
                    usecols=['user_id', 'gender', 'zipcode', 'age_desc', 'occ_desc'])

# Reading movies file
movies = pd.read_csv('data/movies.csv', sep='\t', encoding='latin-1', 
                     usecols=['movie_id', 'title', 'genres'])

# Create training set
shuffled_ratings = ratings.sample(frac=1., random_state=RNG_SEED)

# Shuffling users
Users = shuffled_ratings['user_emb_id'].values
print(f"Users: {Users}, shape: {Users.shape}")

# Shuffling movies
Movies = shuffled_ratings['movie_emb_id'].values
print(f"Movies: {Movies}, shape: {Movies.shape}")

# Shuffling ratings
Ratings = shuffled_ratings['rating'].values
print(f"Ratings: {Ratings}, shape: {Ratings.shape}")

# Define model
model = CFModel(max_userid, max_movieid, K_FACTORS)
# Compile the model using MSE as the loss function and the AdaMax learning algorithm
model.compile(loss='mse', optimizer='adamax')

# Callbacks monitor the validation loss
# Save the model weights each time the validation loss has improved
callbacks = [EarlyStopping('val_loss', patience=2), 
             ModelCheckpoint('models/weights.h5', save_best_only=True)]

# Use 30 epochs, 90% training data, 10% validation data 
model.fit([Users, Movies], Ratings, nb_epoch=30, validation_split=.1, verbose=2, callbacks=callbacks)