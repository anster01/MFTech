import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle
from sklearn.model_selection import RandomizedSearchCV

# load the data file
df = pd.read_csv('../data.0/DataPaper/Combined_Activity_Classifier_data_without_mental_transformed.csv')

# undersample from Rest class so its sample count matches with that of Physical Stress class
df_rest = df.loc[df['Activity'] == 'Rest']
df_physical = df.loc[df['Activity'] == 'Physical Stress']
df_rest = df_rest.sample(n=df_physical.shape[0])
df = pd.concat([df_rest,df_physical])
df.index = pd.RangeIndex(len(df.index))

# divide the dataset into input and output
X = df.drop(columns=['Activity'])
y = df[['Activity']]

# divide into training and test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3,random_state=42)

# train a Random Forest Classifier model
model = RandomForestClassifier(n_estimators=900,min_samples_split=10,min_samples_leaf=2,max_features='sqrt',max_depth=80,criterion='entropy')
model.fit(X_train, y_train.values.ravel())

# save the model
filename = 'rfc_finalized_model.sav'
pickle.dump(model, open(filename, 'wb'))

# test loading model
loaded_model = pickle.load(open(filename, 'rb'))
print("Score on training set ", loaded_model.score(X_train, y_train))
score = loaded_model.score(X_test, y_test)
print("Score on test set ", score)


# Hyperparameter Tuning
n_estimators = [*range(100,1000,100)]
criterion = ['gini','entropy']
max_features = ['sqrt','log2']
max_depth = [None,*range(10,100,10)]
min_samples_split = [2,5,10]
min_samples_leaf = [*range(2,10,2)]

random_grid = {'n_estimators': n_estimators,
               'criterion': criterion,
               'max_features': max_features,
               'max_depth': max_depth,
               'min_samples_split': min_samples_split,
               'min_samples_leaf': min_samples_leaf}

# randomized search
rf_random = RandomizedSearchCV(estimator = RandomForestClassifier(), param_distributions = random_grid, n_iter = 100, cv = 5, verbose=2, random_state=42, n_jobs = -1)
# Fit the random search model
rf_random.fit(X_train, y_train.values.ravel())
print(rf_random.best_params_)