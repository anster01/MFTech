import pandas as pd
import math

# return true if time is within start and end
def within_period(time, start, end):
	# time given in hh:mm:ss
	# start, end given in hh:mm
	hour, minute, second = time.split(':')
	startHour, startMinute = start.split(':')
	endHour, endMinute = end.split(':')
	if int(hour) > int(endHour) or int(hour) < int(startHour):
		return False
	elif int(minute) > int(endMinute) or int(minute) < int(startMinute):
		return False
	elif int(minute) == int(endMinute) and int(second) > 0:
		return False
	else:
		return True

for i in range(1,23):
	datapath = 'data.0/DataPaper/user_' + str(i) + '/actigraph.csv'
	df = pd.read_csv('data.0/DataPaper/user_' + str(i) + '/actigraph.csv')
	activityData = pd.read_csv('data.0/DataPaper/user_' + str(i) + '/activity.csv')
	activityLabel = []

	# add activityLabel
	for j in range(df.shape[0]):
		time = df.iloc[j][12] # time in actigraph
		activityFound = False
		for k in range(activityData.shape[0]):
			start = activityData.iloc[k][2] # start
			end = activityData.iloc[k][3] # end
			if type(end) == str and within_period(time,start,end):
				activityLabel.append(activityData.iloc[k][1])
				activityFound = True
				break
		if activityFound == False:
			activityLabel.append('-1')
		print(j)
	# insert activity label as a new column
	print(f"df row count: {df.shape[0]}")
	print(f"activityLabel row count: {len(activityLabel)}")
	df['Activity'] = activityLabel
	df = df.drop(columns=['Unnamed: 0'])
	
	df.to_csv('data.0/DataPaper/user_' + str(i) + '/actigraph_with_label.csv')