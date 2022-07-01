import pandas as pd
import pickle

# for each user
for i in range(1,23):
    df = pd.read_csv('../data.0/DataPaper/user_' + str(i) + '/Actigraph_with_label_new.csv')
    
    # count number of samples where activity class is physical stress
    count_physical_original = 0
    for row in range(df.shape[0]):
        if df['Activity'][row] == '4' or df['Activity'][row] == '5' or df['Activity'][row] == '6':
            count_physical_original += 1

    df = df.loc[df['Activity'] == 'missing']

    # load developed random forest classifier model
    filename = 'rfc_finalized_model.sav'
    loaded_model = pickle.load(open(filename, 'rb'))

    # drop output label and unnecessary columns
    df_predicted_activity = loaded_model.predict(df.drop(columns=['Activity','Unnamed: 0','day','time']))

    # predict activity class of samples with missing output label 
    # count samples with physical stress as class and samples with rest as class
    count_physical = 0
    count_rest = 0
    for row in range(df_predicted_activity.shape[0]):
        if df_predicted_activity[row] == 'Physical Stress':
            count_physical += 1
        elif df_predicted_activity[row] == 'Rest':
            count_rest += 1
        else:
            print("Error: ", df_predicted_activity[row])
            quit()

    # print(f"User {i}: {count_physical_original} + {count_physical} = {count_physical_original + count_physical}")
    # print(f"User {i}: {count_physical_original + count_physical}")
    print((count_physical_original + count_physical) / 60)