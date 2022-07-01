import pickle
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

filename = 'svm_finalized_model.sav'
loaded_model = pickle.load(open(filename, 'rb'))

test_input = pd.read_csv('testSubject.csv')

predicted_output = loaded_model.predict(test_input) #run model

if predicted_output[0] == -1: #output to website using pyscript
    pyscript.write("mytext2","Low")
else:
    pyscript.write("mytext2","High")
