import pandas as pd

# list where dataframe from each user will be stored to be concatenated
dataframes = []

# loop for each user
for i in range(1,23):
    df = pd.read_csv('../data.0/DataPaper/user_' + str(i) + '/Actigraph_with_label_new.csv')
    
    # remove samples with missing activity label
    missing_rows = []
    for row in range(df.shape[0]):
        if df['Activity'][row] == 'missing':
            missing_rows.append(row)
    df.drop(missing_rows, axis=0, inplace=True)
    df.drop(['day','time'], axis=1, inplace=True)

    # min-max normalise accelerometer and heart rate data
    columns_to_normalise = ['Axis1','Axis2','Axis3','Vector Magnitude','HR']
    for attr in columns_to_normalise:
        df[attr] = (df[attr]-df[attr].min())/(df[attr].max()-df[attr].min())
    dataframes.append(df)
    print(f"User {i} complete")

# combine dataframes and reset index
combined_dataframe = pd.concat(dataframes)
combined_dataframe = combined_dataframe.drop(columns=['Unnamed: 0'])
combined_dataframe.index = pd.RangeIndex(len(combined_dataframe.index))

combined_dataframe.to_csv('../data.0/DataPaper/Combined_Activity_Classifier_data_all.csv',index=False)
print(f"All data length: {combined_dataframe.shape[0]}")

# remove mental stress activities
combined_dataframe_without_mental = combined_dataframe.copy()
mental_rows = []
for row in range(combined_dataframe_without_mental.shape[0]):
    if int(combined_dataframe_without_mental['Activity'][row]) >= 8:
        mental_rows.append(row)
combined_dataframe_without_mental.drop(mental_rows, axis=0, inplace=True)
combined_dataframe_without_mental.reset_index(inplace = True, drop = True)
combined_dataframe_without_mental.to_csv('../data.0/DataPaper/Combined_Activity_Classifier_data_without_mental.csv',index=False)
print(f"Without mental stress length: {combined_dataframe_without_mental.shape[0]}")

# categorise activity labels into activity classes (Rest, Physical Stress, Mental Stress)
activities = combined_dataframe['Activity'].astype(int).to_list()
for row in range(len(activities)):
    if activities[row] >= 1 and activities[row] <= 3 or activities[row] == 7:
        activities[row] = 'Rest'
    elif activities[row] >= 8:
        activities[row] = 'Mental Stress'
    elif activities[row] >= 4 and activities[row] <= 6:
        activities[row] = 'Physical Stress'
combined_dataframe['Activity'] = pd.Series(activities)
combined_dataframe.to_csv('../data.0/DataPaper/Combined_Activity_Classifier_data_all_transformed.csv',index=False)
print(f"All data transformed length: {combined_dataframe.shape[0]}")

# similarly, categorise activity labels into activity classes
# here without mental stress
activities = combined_dataframe_without_mental['Activity'].astype(int).to_list()
for row in range(len(activities)):
    if activities[row] >= 1 and activities[row] <= 3 or activities[row] == 7:
        activities[row] = 'Rest'
    elif activities[row] >= 4 and activities[row] <= 6:
        activities[row] = 'Physical Stress'
combined_dataframe_without_mental['Activity'] = pd.Series(activities)
combined_dataframe_without_mental.to_csv('../data.0/DataPaper/Combined_Activity_Classifier_data_without_mental_transformed.csv',index=False)
print(f"Without mental stress transformed length: {combined_dataframe_without_mental.shape[0]}")