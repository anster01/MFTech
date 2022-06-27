import pickle

filename = 'svm_finalized_model.sav'
loaded_model = pickle.load(open(filename, 'rb'))

test_input = pd.read_csv('testSubject.csv')

predicted_output = loaded_model.predict(test_input)

print(predicted_output)