import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score,classification_report,confusion_matrix
from sklearn.ensemble import ExtraTreesClassifier, RandomForestRegressor
from sklearn.metrics import mean_squared_error as mse
from sklearn.model_selection import GridSearchCV
from datetime import datetime

df = pd.read_csv('data.0/DataPaper/Combined_Activity_Classifier_data.csv', index_col=0)
df.drop(columns=['Start Time'], inplace=True)
# sns.countplot(df['Activity'])
# plt.show()
# sns.scatterplot(data=df, x='Activity', y='Inclinometer Off')
# plt.show()
# print(df.describe())

#X = df.drop('Activity', axis=1)
X = df[['Steps','Inclinometer Standing','HR','Inclinometer Off','Inclinometer Sitting','Short Term HRV']]
y = df[['Activity']]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3,random_state=42)

"""
reg = ExtraTreesClassifier()
reg.fit(X_train, y_train)
feat_importances = pd.Series(reg.feature_importances_, index=X_train.columns)
feat_importances.nlargest(11).plot(kind='barh')
plt.show()
"""

# constructing a model and checking its accuracy
classifier_model = DecisionTreeClassifier(criterion='entropy',max_depth=6,max_features='sqrt',max_leaf_nodes=10,min_samples_leaf=2,splitter='best')
classifier_model.fit(X_train,y_train)
y_predict = classifier_model.predict(X_test)
# sns.distplot(y_test.to_numpy()-y_predict)
# plt.show()
# plt.scatter(y_test,y_predict)
classifier_model = DecisionTreeClassifier(max_depth=20)
classifier_model.fit(X_train,y_train)
print(f"Score on training set: {classifier_model.score(X_train,y_train)}")
print(f"Score on test set: {classifier_model.score(X_test,y_test)}")

# Hyperparameter tuning
parameters={
            "criterion": ["gini","entropy","log_loss"],
            "splitter":["best","random"],
            "max_depth" : [None,*range(1,100)],
           "min_samples_leaf":[1,2,3,4,5,6,7,8,9,10],
           "max_features":["log2","sqrt",None],
           "max_leaf_nodes":[None,10,20,30,40,50,60,70,80,90] }

tuning_model=GridSearchCV(DecisionTreeClassifier(),param_grid=parameters,cv=5,verbose=3)

def timer(start_time=None):
    if not start_time:
        start_time=datetime.now()
        return start_time
    elif start_time:
        thour,temp_sec=divmod((datetime.now()-start_time).total_seconds(),3600)
        tmin,tsec=divmod(temp_sec,60)
        print(thour,":",tmin,':',round(tsec,2))

start_time=timer(None)

tuning_model.fit(X,y)

timer(start_time)

print(tuning_model.best_params_)