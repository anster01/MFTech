import pandas as pd
import math
from openpyxl import load_workbook
from hrvanalysis import remove_outliers, remove_ectopic_beats, interpolate_nan_values, plot_poincare
from statistics import mode

DURATION = 5 # in minutes

# calculate 5 minutes after start time
def calculateEndTime(startTime):
	startTime = startTime.split(":")
	minute = int(startTime[1]) + DURATION
	hour = int(startTime[0])
	if minute >= 60:
		minute -= 60
		hour += 1
	return f"{hour if hour >= 10 else str(0)+str(hour)}:{minute if minute >= 10 else str(0)+str(minute)}:{startTime[2]}"

# return true if time1 is before time2
def before(time1, time2):
	time1 = time1.split(":")
	if time2 == "24:00:00" and int(time1[0]) == 0:
		return False
	time2 = time2.split(":")
	if int(time1[0]) < int(time2[0]) or int(time1[0]) == int(time2[0]) and int(time1[1]) < int(time2[1]) or int(time1[0]) == int(time2[0]) and int(time1[1]) == int(time2[1]) and int(time1[2]) < int(time2[2]):
		return True
	return False

# compare the start time of RR and Actigraph and choose the later one as start time
# return the first time after the start time where the minutes are a multiple of 5
# to conveniently divide the dataset into 5-minute time frame
def findStartTime(rrStart, actigraphStart):
	rrStart = rrStart.split(':')
	actigraphStart = actigraphStart.split(':')
	rrStart[0] = int(rrStart[0])
	actigraphStart[0] = int(actigraphStart[0])
	if rrStart[0] > actigraphStart[0]:
		hour = rrStart[0]
		minute = int(rrStart[1])
		second = int(rrStart[2])
	elif rrStart[0] == actigraphStart[0]:
		hour = rrStart[0]
		rrStart[1] = int(rrStart[1])
		actigraphStart[1] = int(actigraphStart[1])
		if rrStart[1] > actigraphStart[1]:
			minute = rrStart[1]
			second = int(rrStart[2])
		elif rrStart[1] == actigraphStart[1]:
			minute = rrStart[1]
			second = max(int(rrStart[2]), int(actigraphStart[2]))
		else:
			minute = actigraphStart[1]
			second = int(actigraphStart[2])
	else:
		hour = actigraphStart[0]
		minute = int(actigraphStart[1])
		second = int(actigraphStart[2])
	minute = minute + 5 - (minute % 5) if minute % 5 != 0 or second != 0 else minute
	return f"{hour if hour >= 10 else str(0)+str(hour)}:{minute if minute >= 10 else str(0)+str(minute)}:00"

# compare the end time of RR and Actigraph and choose the earlier one as end time
# return the last time before the end time where the minutes are a multiple of 5
# to conveniently divide the dataset into 5-minute time frame
def findEndTime(rrEnd, actigraphEnd):
	rrEnd = rrEnd.split(':')
	actigraphEnd = actigraphEnd.split(':')
	rrEnd[0] = int(rrEnd[0])
	actigraphEnd[0] = int(actigraphEnd[0])
	if rrEnd[0] < actigraphEnd[0]:
		hour = rrEnd[0]
		minute = int(rrEnd[1])
	elif rrEnd[0] == actigraphEnd[0]:
		hour = rrEnd[0]
		rrEnd[1] = int(rrEnd[1])
		actigraphEnd[1] = int(actigraphEnd[1])
		if rrEnd[1] < actigraphEnd[1]:
			minute = rrEnd[1]
		elif rrEnd[1] == actigraphEnd[1]:
			minute = rrEnd[1]
		else:
			minute = actigraphEnd[1]
	else:
		hour = actigraphEnd[0]
		minute = int(actigraphEnd[1])
	minute = minute - (minute % 5) if minute % 5 != 0 else minute
	return f"{hour if hour >= 10 else str(0)+str(hour)}:{minute if minute >= 10 else str(0)+str(minute)}:00"

# loop for every user
for i in range(1,23):

	# clean RR data
	rrData = pd.read_csv('data.0/DataPaper/user_' + str(i) + '/RR.csv')
	rr_intervals_list = rrData['ibi_s'].to_list()
	# This remove outliers from signal
	rr_intervals_without_outliers = remove_outliers(rr_intervals=rr_intervals_list, low_rri=0.2, high_rri=2)
	# This replace outliers nan values with linear interpolation
	interpolated_rr_intervals = interpolate_nan_values(rr_intervals=rr_intervals_without_outliers,
													interpolation_method="linear")
	# This remove ectopic beats from signal
	nn_intervals_list = remove_ectopic_beats(rr_intervals=interpolated_rr_intervals, method="malik")
	# This replace ectopic beats nan values with linear interpolation
	interpolated_nn_intervals = interpolate_nan_values(rr_intervals=nn_intervals_list)
	print(f"interpolated_nn intervals length: {len(interpolated_nn_intervals)}")
	print(f"dataframe length: {rrData.shape[0]}")
	rrData['ibi_s'] = pd.Series(interpolated_nn_intervals)

	actigraphData = pd.read_csv('data.0/DataPaper/user_' + str(i) + '/actigraph_with_label.csv')
	
	# create data list for a new dataframe
	data = []

	# variables for rr
	rr_row = 0

	# variables for actigraph
	actigraph_row = 0
	actigraph_count_entire = 0
	actigraph_axis1_total_entire = 0
	actigraph_axis2_total_entire = 0
	actigraph_axis3_total_entire = 0
	actigraph_vector_magnitude_total_entire = 0
	actigraph_hr_total_entire = 0

	# find start and end time
	start_time = findStartTime(rrData.iloc[0][3], actigraphData.iloc[0][12])
	end_time = findEndTime(rrData.iloc[rrData.shape[0]-1][3], actigraphData.iloc[actigraphData.shape[0]-1][12])
	hour, minute, second = end_time.split(':')
	end_time = f"{int(hour)+24}:{minute}:{second}"
	after_duration = calculateEndTime(start_time)
	print(f"User {i} start time: {start_time}, end time: {end_time}")

	# discard data before start time
	while before(rrData.iloc[rr_row][3], start_time):
		rr_row += 1
	while before(actigraphData.iloc[actigraph_row][12], start_time):
		actigraph_row += 1

	while True:

		rr_total = 0
		rr_count = 0
		actigraph_axis1_total = 0
		actigraph_axis2_total = 0
		actigraph_axis3_total = 0
		actigraph_steps_total = 0
		actigraph_hr_total = 0
		actigraph_inclinometer_off_total = 0
		actigraph_inclinometer_standing_total = 0
		actigraph_inclinometer_sitting_total = 0
		actigraph_inclinometer_lying_total = 0
		actigraph_vector_magnitude_total = 0
		actigraph_count = 0
		activityLabels = []

		# calculate hrv (rmssd)
		while before(rrData.iloc[rr_row][3], after_duration):
			rr_total += (rrData.iloc[rr_row][1]*1000 - rrData.iloc[rr_row+1][1]*1000) ** 2
			if math.isnan(rr_total):
				print(f"first value: {rrData.iloc[rr_row][1]}, second value: {rrData.iloc[rr_row+1][1]}")
				quit()
			rr_count += 1
			rr_row += 1
		
		while before(actigraphData.iloc[actigraph_row][12], after_duration):
			actigraph_axis1_total += actigraphData.iloc[actigraph_row][1]
			actigraph_axis2_total += actigraphData.iloc[actigraph_row][2]
			actigraph_axis3_total += actigraphData.iloc[actigraph_row][3]
			actigraph_steps_total += actigraphData.iloc[actigraph_row][4]
			actigraph_hr_total += actigraphData.iloc[actigraph_row][5]
			actigraph_inclinometer_off_total += actigraphData.iloc[actigraph_row][6]
			actigraph_inclinometer_standing_total += actigraphData.iloc[actigraph_row][7]
			actigraph_inclinometer_sitting_total += actigraphData.iloc[actigraph_row][8]
			actigraph_inclinometer_lying_total += actigraphData.iloc[actigraph_row][9]
			actigraph_vector_magnitude_total += actigraphData.iloc[actigraph_row][10]
			activityLabels.append(actigraphData.iloc[actigraph_row][13])
			actigraph_count += 1
			actigraph_row += 1
		
		# store short term HRV result
		rr_result = "missing" if rr_count == 0 else math.sqrt(rr_total / rr_count)
		print(f"{start_time}-{after_duration} short term HRV: {rr_result} from {rr_count} number of data")

		# store actigraph result
		actigraph_axis1_result = "missing" if actigraph_count == 0 else actigraph_axis1_total / actigraph_count
		actigraph_axis2_result = "missing" if actigraph_count == 0 else actigraph_axis2_total / actigraph_count
		actigraph_axis3_result = "missing" if actigraph_count == 0 else actigraph_axis3_total / actigraph_count
		actigraph_steps_result = "missing" if actigraph_count == 0 else actigraph_steps_total / actigraph_count
		actigraph_hr_result = "missing" if actigraph_count == 0 else actigraph_hr_total / actigraph_count
		actigraph_inclinometer_off_result = "missing" if actigraph_count == 0 else actigraph_inclinometer_off_total / actigraph_count
		actigraph_inclinometer_standing_result = "missing" if actigraph_count == 0 else actigraph_inclinometer_standing_total / actigraph_count
		actigraph_inclinometer_sitting_result = "missing" if actigraph_count == 0 else actigraph_inclinometer_sitting_total / actigraph_count
		actigraph_inclinometer_lying_result = "missing" if actigraph_count == 0 else actigraph_inclinometer_lying_total / actigraph_count
		actigraph_vector_magnitude_result = "missing" if actigraph_count == 0 else actigraph_vector_magnitude_total / actigraph_count
		activity = mode(activityLabels) if len(activityLabels) != 0 else "missing"
		print(f"{start_time}-{after_duration} Avg axis1: {actigraph_axis1_result} from {actigraph_count} number of data")
		print(f"{start_time}-{after_duration} Avg axis2: {actigraph_axis2_result} from {actigraph_count} number of data")
		print(f"{start_time}-{after_duration} Avg axis3: {actigraph_axis3_result} from {actigraph_count} number of data")
		print(f"{start_time}-{after_duration} Avg steps: {actigraph_steps_result} from {actigraph_count} number of data")
		print(f"{start_time}-{after_duration} Avg hr: {actigraph_hr_result} from {actigraph_count} number of data")
		print(f"{start_time}-{after_duration} Avg inclinometer off: {actigraph_inclinometer_off_result} from {actigraph_count} number of data")
		print(f"{start_time}-{after_duration} Avg inclinometer standing: {actigraph_inclinometer_standing_result} from {actigraph_count} number of data")
		print(f"{start_time}-{after_duration} Avg inclinometer sitting: {actigraph_inclinometer_sitting_result} from {actigraph_count} number of data")
		print(f"{start_time}-{after_duration} Avg inclinometer lying: {actigraph_inclinometer_lying_result} from {actigraph_count} number of data")
		print(f"{start_time}-{after_duration} Avg vector magnitude: {actigraph_vector_magnitude_result} from {actigraph_count} number of data")
		print(f"{start_time}-{after_duration} Activity: {activity}")
		actigraph_axis1_total_entire += actigraph_axis1_total
		actigraph_axis2_total_entire += actigraph_axis2_total
		actigraph_axis3_total_entire += actigraph_axis3_total
		actigraph_vector_magnitude_total_entire += actigraph_vector_magnitude_total
		actigraph_hr_total_entire += actigraph_hr_total
		actigraph_count_entire += actigraph_count

		data.append([actigraph_axis1_result,actigraph_axis2_result,actigraph_axis3_result,actigraph_steps_result,actigraph_hr_result,actigraph_inclinometer_off_result,actigraph_inclinometer_standing_result,actigraph_inclinometer_sitting_result,actigraph_inclinometer_lying_result,actigraph_vector_magnitude_result,rr_result,activity,start_time])

		# go to the next time interval
		start_time = after_duration
		if start_time == "24:00:00":
			start_time = "00:00:00"
			hour, minute, second = end_time.split(':')
			end_time = f"{int(hour)-24 if int(hour)-24 >= 10 else '0' + str(int(hour)-24)}:{minute}:{second}"
		elif start_time == end_time:
			break
		after_duration = calculateEndTime(start_time)
	
	new_dataframe = pd.DataFrame(data, columns=['Axis1', 'Axis2', 'Axis3', 'Steps', 'HR', 'Inclinometer Off', 'Inclinometer Standing', 'Inclinometer Sitting', 'Inclinometer Lying', 'Vector Magnitude', 'Short Term HRV','Activity','Start Time'])
	
	actigraph_axis1_result_entire = actigraph_axis1_total_entire / actigraph_count_entire
	actigraph_axis2_result_entire = actigraph_axis2_total_entire / actigraph_count_entire
	actigraph_axis3_result_entire = actigraph_axis3_total_entire / actigraph_count_entire
	actigraph_vector_magnitude_result_entire = actigraph_vector_magnitude_total_entire / actigraph_count_entire
	actigraph_hr_result_entire = actigraph_hr_total_entire / actigraph_count_entire

	for row in range(new_dataframe.shape[0]):
		new_dataframe.iloc[row][0] = float(new_dataframe.iloc[row][0]) / actigraph_axis1_result_entire if new_dataframe.iloc[row][0] != "missing" else "missing"
		new_dataframe.iloc[row][1] = float(new_dataframe.iloc[row][1]) / actigraph_axis2_result_entire if new_dataframe.iloc[row][1] != "missing" else "missing"
		new_dataframe.iloc[row][2] = float(new_dataframe.iloc[row][2]) / actigraph_axis3_result_entire if new_dataframe.iloc[row][2] != "missing" else "missing"
		new_dataframe.iloc[row][9] = float(new_dataframe.iloc[row][9]) / actigraph_vector_magnitude_result_entire if new_dataframe.iloc[row][9] != "missing" else "missing"
		new_dataframe.iloc[row][10] = float(new_dataframe.iloc[row][10]) / actigraph_hr_result_entire if new_dataframe.iloc[row][10] != "missing" else "missing"
	
	# dataset with missing activity label
	new_dataframe.to_csv('data.0/DataPaper/user_' + str(i) + '/Activity_Classifier_data_with_missing.csv')
	
	# remove samples with missing activity label
	missing_rows = []
	for row in range(new_dataframe.shape[0]):
		if new_dataframe.iloc[row][11] == -1 or new_dataframe.iloc[row][11] == "missing":
			missing_rows.append(row)
	new_dataframe.drop(missing_rows, axis=0, inplace=True)
	new_dataframe.to_csv('data.0/DataPaper/user_' + str(i) + '/Activity_Classifier_data.csv')
