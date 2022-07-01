import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import StratifiedKFold
from sklearn.feature_selection import RFECV
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier
from sklearn.model_selection import train_test_split

df = pd.read_csv('../data.0/DataPaper/Combined_Activity_Classifier_data_without_mental_transformed.csv')
df_rest = df.loc[df['Activity'] == 'Rest']
df_physical = df.loc[df['Activity'] == 'Physical Stress']
df_rest = df_rest.sample(n=df_physical.shape[0])
df = pd.concat([df_rest,df_physical])
df.index = pd.RangeIndex(len(df.index))
print("Reduced")
X = df.drop(columns=['Activity'])
y = df[['Activity']]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3,random_state=42)

# show feature importance map
reg = ExtraTreesClassifier()
reg.fit(X_train, y_train)
feat_importances = pd.Series(reg.feature_importances_, index=X_train.columns)
feat_importances.nlargest(10).plot(kind='barh')
plt.show()

# perform recursive feature elimination and show the graph
min_features_to_select = 1  # Minimum number of features to consider
rfecv = RFECV(
    estimator=RandomForestClassifier(),
    step=1,
    cv=StratifiedKFold(2),
    scoring="accuracy",
    min_features_to_select=min_features_to_select,
)
rfecv.fit(X, y)

print("Optimal number of features : %d" % rfecv.n_features_)

# Plot number of features VS. cross-validation scores
plt.figure()
plt.xlabel("Number of features selected")
plt.ylabel("Cross validation score (accuracy)")
plt.plot(
    range(min_features_to_select, len(rfecv.grid_scores_) + min_features_to_select),
    rfecv.grid_scores_,
)
plt.show()