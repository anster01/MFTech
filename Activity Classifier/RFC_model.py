import pickle

filename = 'rfc_finalized_model.sav'
loaded_model = pickle.load(open(filename, 'rb'))

test_input = [[0, 0, 0, 0, 83, 0, 0, 1, 0, 0], [23, 10, 56, 1, 81, 0, 1, 0, 0, 61.36]]

predicted_output = loaded_model.predict(test_input)

print(predicted_output)