import pickle
import warnings
warnings.filterwarnings("ignore")

filename = 'rfc_finalized_model.sav'
loaded_model = pickle.load(open(filename, 'rb'))

#test_input = [[23, 10, 56, 1, 81, 0, 1, 0, 0, 61.36]]
Axis1_min_max = [0, 490]
Axis2_min_max = [0, 576]
Axis3_min_max = [0, 496]
HR_min_max = [32, 251]
Vector_Magnitude_min_max = [0, 626.15]

test_input = [[17, 0, 0, 0, 85, 0, 1,0, 0, 17], [108, 87, 40, 1, 96, 0, 1, 0, 0, 144.34]]

pyscript.write("axis-1",test_input[0][0])
pyscript.write("axis-2",test_input[0][1])
pyscript.write("axis-3",test_input[0][2])
pyscript.write("vec-mg",test_input[0][9])
pyscript.write("heart-rate",test_input[0][4])

test_input_normalised = test_input
for i in range(len(test_input_normalised)):
    k = 0
    test_input_normalised[i][0] = (test_input_normalised[i][0] - Axis1_min_max[0]) / (Axis1_min_max[1] - Axis1_min_max[0])
    test_input_normalised[i][1] = (test_input_normalised[i][1] - Axis2_min_max[0]) / (Axis2_min_max[1] - Axis2_min_max[0])
    test_input_normalised[i][2] = (test_input_normalised[i][2] - Axis3_min_max[0]) / (Axis3_min_max[1] - Axis3_min_max[0])
    test_input_normalised[i][4] = (test_input_normalised[i][4] - HR_min_max[0]) / (HR_min_max[1] - HR_min_max[0])
    test_input_normalised[i][9] = (test_input_normalised[i][9] - Vector_Magnitude_min_max[0]) / (Vector_Magnitude_min_max[1] - Vector_Magnitude_min_max[0])

predicted_output = loaded_model.predict(test_input_normalised)

predicted_output = loaded_model.predict(test_input) #run model

pyscript.write("mytext",predicted_output[0]) #output to website

#print(predicted_output)
