import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import RandomizedSearchCV
from sklearn import svm
from sklearn.svm import LinearSVC
from imblearn.over_sampling import SMOTE
import pickle

# d = [meanNN_, SDNN_, RMSSD_, SDSD_, pnn50_, pnn20_, lf_, hf_, lfhf_]
# export_data = zip_longest(*d, fillvalue = '')
# with open('X.csv', 'w', encoding="ISO-8859-1", newline='') as myfile:
#       wr = csv.writer(myfile)
#       wr.writerow(("meanNN", "SDNN", "RMSSD", "SDSD", "pnn50", "pnn20", "LF", "HF", "LF/HF"))
#       wr.writerows(export_data)
# myfile.close()
df_combined = pd.read_csv('final_HRV_stai.csv')

df_combined = pd.concat([X,y],axis=1)
df_combined.index = pd.RangeIndex(len(df_combined.index))
df_combined.drop([4],axis=0,inplace=True)
df_combined.reset_index(drop=True,inplace=True)

# display(df_combined)

X = df_combined.drop(columns=['STAI level'])
y = df_combined[['STAI level']]

oversample = SMOTE(sampling_strategy='minority', k_neighbors=3)
X, y = oversample.fit_resample(X, y)
(X_train, X_test, y_train, y_test) = train_test_split(X, y, train_size=0.7, random_state=1)

model = svm.SVC(kernel='poly', degree=1.2, gamma='auto', coef0=1, C=5)
model.fit(X_train, y_train)

filename = 'svm_finalized_model.sav'
pickle.dump(model, open(filename, 'wb'))

loaded_mod = pickle.load(open(filename, 'rb'))
score = loaded_mod.score(X_test, y_test)
