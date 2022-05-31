import pandas as pd

from ctgan import CTGANSynthesizer
from sdv.constraints import Between
from sdv.tabular import CTGAN

data = pd.read_csv("dataset_all_columns.csv")

# set constraints for the attributes
BMI_constraint = Between(
	column='BMI = Weight / Height^2',
	low=10,
	high=60,
	handling_strategy='transform'
)

HRV_entire_constraint = Between(
	column='HRV entire',
	low=0,
	high=1000,
	handling_strategy='transform'
)

HRV_8to9_constraint = Between(
	column='HRV 8-9',
	low=10,
	high=300,
	handling_strategy='transform'
)

HRV_9to10_constraint = Between(
	column='HRV 9-10',
	low=10,
	high=300,
	handling_strategy='transform'
)

HRV_10to11_constraint = Between(
	column='HRV 10-11',
	low=10,
	high=300,
	handling_strategy='transform'
)

HRV_11to12_constraint = Between(
	column='HRV 11-12',
	low=10,
	high=300,
	handling_strategy='transform'
)

HRV_12to13_constraint = Between(
	column='HRV 12-13',
	low=10,
	high=300,
	handling_strategy='transform'
)

HRV_13to14_constraint = Between(
	column='HRV 13-14',
	low=10,
	high=300,
	handling_strategy='transform'
)

HRV_14to15_constraint = Between(
	column='HRV 14-15',
	low=10,
	high=300,
	handling_strategy='transform'
)

HRV_15to16_constraint = Between(
	column='HRV 15-16',
	low=10,
	high=300,
	handling_strategy='transform'
)

HRV_16to17_constraint = Between(
	column='HRV 16-17',
	low=10,
	high=300,
	handling_strategy='transform'
)

HRV_17to18_constraint = Between(
	column='HRV 17-18',
	low=10,
	high=300,
	handling_strategy='transform'
)

HRV_18to19_constraint = Between(
	column='HRV 18-19',
	low=10,
	high=300,
	handling_strategy='transform'
)

HRV_19to20_constraint = Between(
	column='HRV 19-20',
	low=10,
	high=300,
	handling_strategy='transform'
)

HRV_20to21_constraint = Between(
	column='HRV 20-21',
	low=10,
	high=300,
	handling_strategy='transform'
)

HRV_21to22_constraint = Between(
	column='HRV 21-22',
	low=10,
	high=300,
	handling_strategy='transform'
)

HRV_22to23_constraint = Between(
	column='HRV 22-23',
	low=10,
	high=300,
	handling_strategy='transform'
)

HRV_23to24_constraint = Between(
	column='HRV 23-24',
	low=10,
	high=300,
	handling_strategy='transform'
)

HRV_0to1_constraint = Between(
	column='HRV 0-1',
	low=10,
	high=300,
	handling_strategy='transform'
)

HRV_1to2_constraint = Between(
	column='HRV 1-2',
	low=10,
	high=300,
	handling_strategy='transform'
)

HRV_2to3_constraint = Between(
	column='HRV 2-3',
	low=10,
	high=300,
	handling_strategy='transform'
)

HRV_3to4_constraint = Between(
	column='HRV 3-4',
	low=10,
	high=300,
	handling_strategy='transform'
)

HRV_4to5_constraint = Between(
	column='HRV 4-5',
	low=10,
	high=300,
	handling_strategy='transform'
)

HRV_5to6_constraint = Between(
	column='HRV 5-6',
	low=10,
	high=300,
	handling_strategy='transform'
)

HRV_6to7_constraint = Between(
	column='HRV 6-7',
	low=10,
	high=300,
	handling_strategy='transform'
)

HRV_7to8_constraint = Between(
	column='HRV 7-8',
	low=10,
	high=300,
	handling_strategy='transform'
)

HRV_8to9_constraint = Between(
	column='HRV 8-9',
	low=10,
	high=300,
	handling_strategy='transform'
)

BISBAS_bis_constraint = Between(
	column='BISBAS_bis',
	low=4,
	high=28,
	handling_strategy='transform'
)

BISBAS_reward_constraint = Between(
	column='BISBAS_reward',
	low=4,
	high=28,
	handling_strategy='transform'
)

BISBAS_drive_constraint = Between(
	column='BISBAS_drive',
	low=4,
	high=16,
	handling_strategy='transform'
)

BISBAS_fun_constraint = Between(
	column='BISBAS_fun',
	low=4,
	high=16,
	handling_strategy='transform'
)

Exercise_constraint = Between(
	column='Exercises (minutes) = Activity 4,5,6',
	low=30,
	high=200,
	handling_strategy='transform'
)

AlcoholSmoking_constraint = Between(
	column='Alcohol + smoking (minutes) = Activity 11,12',
	low=0,
	high=200,
	handling_strategy='transform'
)

PANAS_pos_10_constraint = Between(
	column='panas_pos_10',
	low=5,
	high=50,
	handling_strategy='transform'
)

PANAS_neg_10_constraint = Between(
	column='panas_neg_10',
	low=5,
	high=50,
	handling_strategy='transform'
)

PANAS_pos_14_constraint = Between(
	column='panas_pos_14',
	low=5,
	high=50,
	handling_strategy='transform'
)

PANAS_neg_14_constraint = Between(
	column='panas_neg_14',
	low=5,
	high=50,
	handling_strategy='transform'
)

PANAS_pos_18_constraint = Between(
	column='panas_pos_18',
	low=5,
	high=50,
	handling_strategy='transform'
)

PANAS_neg_18_constraint = Between(
	column='panas_neg_18',
	low=5,
	high=50,
	handling_strategy='transform'
)

PANAS_pos_22_constraint = Between(
	column='panas_pos_22',
	low=5,
	high=50,
	handling_strategy='transform'
)

PANAS_neg_22_constraint = Between(
	column='panas_neg_22',
	low=5,
	high=50,
	handling_strategy='transform'
)

PANAS_pos_9_constraint = Between(
	column='panas_pos_9+1',
	low=5,
	high=50,
	handling_strategy='transform'
)

PANAS_neg_9_constraint = Between(
	column='panas_neg_9+1',
	low=5,
	high=50,
	handling_strategy='transform'
)

STAI2_constraint = Between(
	column='STAI2',
	low=20,
	high=80,
	handling_strategy='transform'
)

Melatonin_before_constraint = Between(
	column='Melatonin NORM (before sleep)',
	low=1e-9,
	high=3e-8,
	handling_strategy='transform'
)

Melatonin_after_constraint = Between(
	column='Melatonin NORM (wake up)',
	low=5e-10,
	high=3e-8,
	handling_strategy='transform'
)

Sleep_efficiency_constraint = Between(
	column='Sleep Efficiency',
	low=0,
	high=100,
	handling_strategy='transform'
)

Sleep_fragmentation_constraint = Between(
	column='Sleep Fragmentation Index',
	low=5,
	high=50,
	handling_strategy='transform'
)

Pittsburgh_constraint = Between(
	column='Pittsburgh',
	low=0,
	high=21,
	handling_strategy='transform'
)

Cortisol_before_constraint = Between(
	column='Cortisol NORM (before sleep)',
	low=0.001,
	high=0.2,
	handling_strategy='transform'
)

Cortisol_after_constraint = Between(
	column='Cortisol NORM (wake up)',
	low=0.01,
	high=0.2,
	handling_strategy='transform'
)

Daily_stress_constraint = Between(
	column='Daily_stress',
	low=0,
	high=406,
	handling_strategy='transform'
)

constraints = [BMI_constraint,
			   BISBAS_bis_constraint,
			   BISBAS_drive_constraint,
			   BISBAS_fun_constraint,
			   BISBAS_reward_constraint,
			   Exercise_constraint,
			   AlcoholSmoking_constraint,
			   PANAS_pos_10_constraint,
			   PANAS_neg_10_constraint,
			   PANAS_pos_14_constraint,
			   PANAS_neg_14_constraint,
			   PANAS_pos_18_constraint,
			   PANAS_neg_18_constraint,
			   PANAS_pos_22_constraint,
			   PANAS_neg_22_constraint,
			   PANAS_pos_9_constraint,
			   PANAS_neg_9_constraint,
			   STAI2_constraint,
			   Melatonin_before_constraint,
			   Melatonin_after_constraint,
			   Sleep_efficiency_constraint,
			   Sleep_fragmentation_constraint,
			   Pittsburgh_constraint,
			   Cortisol_before_constraint,
			   Cortisol_after_constraint,
			   Daily_stress_constraint]

ctgan = CTGAN(epochs=10, constraints=constraints)

ctgan.fit(data)


# Synthetic copy
samples = ctgan.sample(1000)

samples.to_csv("dataset_generated.csv")