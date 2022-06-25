import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

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
model = RandomForestClassifier()
model.fit(X_train, y_train.values.ravel())

# save the model
filename = 'rfc_finalized_model.sav'
pickle.dump(model, open(filename, 'wb'))

# test loading model
loaded_model = pickle.load(open(filename, 'rb'))
score = loaded_model.score(X_test, y_test)
print(score)