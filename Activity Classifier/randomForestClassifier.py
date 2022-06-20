import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import RandomizedSearchCV

# With HRV
# df = pd.read_csv('../data.0/DataPaper/Combined_Activity_Classifier_data.csv', index_col=0)
# X = df[['Steps','HR','Inclinometer Off','Inclinometer Standing','Inclinometer Sitting', 'Short Term HRV']]

# Without HRV
df = pd.read_csv('../data.0/DataPaper/Combined_Activity_Classifier_data_without_hrv.csv', index_col=0)
X = df[['Axis1','Axis2','Axis3','Vector Magnitude','HR']]

y = df[['Activity']]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3,random_state=42)
"""
rfc = RandomForestClassifier(n_estimators=1000, random_state=42)
rfc.fit(X_train,y_train)
y_predict = rfc.predict(X_test)
errors = abs(y_predict - y_test)
print(f"Mean absolute errors: {round(errors.mean(),2)} degrees")
rfc_cv_score = cross_val_score(rfc, X, y, cv=10, scoring='neg_mean_squared_error')

print("=== Confusion Matrix ===")
print(confusion_matrix(y_test, y_predict))
print('\n')
print("=== Classification Report ===")
print(classification_report(y_test, y_predict))
print('\n')
print("=== All Negative MSE Scores ===")
print(rfc_cv_score)
print('\n')
print("=== Mean Negative MSE Score ===")
print("Mean AUC Score - Random Forest: ", rfc_cv_score.mean())

print(f"Score on training set: {rfc.score(X_train,y_train)}")
print(f"Score on test set: {rfc.score(X_test,y_test)}")
"""

# Hyperparameter Tuning
n_estimators = [*range(200,2000,200)]
max_features = ['auto','sqrt']
max_depth = [None,*range(10,100,10)]
min_samples_split = [2,5,10]
min_samples_leaf = [*range(2,10,2)]

random_grid = {'n_estimators': n_estimators,
               'max_features': max_features,
               'max_depth': max_depth,
               'min_samples_split': min_samples_split,
               'min_samples_leaf': min_samples_leaf}

# randomized search 100 times cross validation 9 times
rf_random = RandomizedSearchCV(estimator = RandomForestClassifier(), param_distributions = random_grid, n_iter = 100, cv = 9, verbose=2, random_state=42, n_jobs = -1)
# Fit the random search model
rf_random.fit(X_train, y_train)
print(rf_random.best_params_)