import pickle
import warnings
warnings.filterwarnings("ignore")

filename = 'rfc_finalized_model.sav'
loaded_model = pickle.load(open(filename, 'rb'))

#test_input = [[23, 10, 56, 1, 81, 0, 1, 0, 0, 61.36]]
test_input = [[0, 0, 0, 0, 0.01, 0, 0, 1, 0, 0]]

pyscript.write("axis-1",test_input[0][0])
pyscript.write("axis-2",test_input[0][1])
pyscript.write("axis-3",test_input[0][2])
pyscript.write("vec-mg",test_input[0][9])
pyscript.write("heart-rate",test_input[0][4])

predicted_output = loaded_model.predict(test_input)

pyscript.write("mytext",predicted_output[0])

#print(predicted_output)
