from surprise import Dataset, Reader, SVD, dump
from surprise.model_selection import GridSearchCV

# Paths
RATINGS_PATH = './data/ratings.csv'
MODEL_PATH = './model/Recommender_Model'


# Process ratings with Surprise Scikit
reader = Reader(line_format='user item rating timestamp', sep=',', rating_scale = (0.5,5.0), skip_lines=1)
ratings = Dataset.load_from_file(RATINGS_PATH, reader=reader)
trainset = ratings.build_full_trainset()

# Find the best hyperparameters for an SVD model via grid search cross-validation
param_grid = {
    'n_factors': [5], #[10, 100, 500],
    'n_epochs': [5], #[5, 20, 50], 
    'lr_all': [0.005], #[0.001, 0.005, 0.02],
    'reg_all': [0.02]} #[0.005, 0.02, 0.1]}

gs_model = GridSearchCV(
    algo_class = SVD,
    param_grid = param_grid,
    n_jobs = 1,
    joblib_verbose = 5)

gs_model.fit(ratings)

# Train the SVD model with the parameters that minimise the root mean squared error
print(f"Best SVD parameters: {gs_model.best_params}")
print(f"Test RMSE = {gs_model.cv_results['mean_test_rmse'][0].round(3)}")
best_SVD = gs_model.best_estimator['rmse']
best_SVD.fit(trainset)

# Predict ratings for all pairs (u, i) that are NOT in the training set.
print('Making predictions ...')
testset = trainset.build_anti_testset()
full_predictions = best_SVD.test(testset)

# Save model and predictions
print('Saving model ...')
dump.dump(MODEL_PATH, algo=best_SVD, predictions=full_predictions)
print(f"Model & predictions saved in {MODEL_PATH}")
