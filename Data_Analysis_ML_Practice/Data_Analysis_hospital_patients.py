# Importing data
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df1 = pd.read_csv('test/general.csv')
df2 = pd.read_csv('test/prenatal.csv')
df3 = pd.read_csv('test/sports.csv')

# Setting display
pd.set_option('display.max_columns', 15)

# Change the column names
df2.rename(columns={'HOSPITAL': 'hospital', 'Sex': 'gender'}, inplace=True)
df3.rename(columns={'Hospital': 'hospital', 'Male/female': 'gender'}, inplace=True)

# Merge the data frames to one
total_set = pd.concat([df1, df2, df3], ignore_index=True)

# Delete the data column
total_set.drop(columns=['Unnamed: 0'], inplace=True)

# Delete the all missing data column
total_set.dropna(axis='index', how='all', inplace=True)

# Replace gender to 'f' and 'm'
total_set.replace(to_replace='man', value='m', inplace=True)
total_set.replace(to_replace='male', value='m', inplace=True)
total_set.replace(to_replace='woman', value='f', inplace=True)
total_set.replace(to_replace='female', value='f', inplace=True)

# Replace NaN from prenatal to 'f'
total_set.loc[total_set.hospital == 'prenatal', 'gender'] = 'f'

change_list = ['bmi', 'diagnosis', 'blood_test', 'ecg', 'ultrasound', 'mri', 'xray', 'children', 'months']
for x in change_list:
    total_set[x].fillna(0, inplace=True)


# 1. What is the most common age of a patient among all hospitals?
# Plot a histogram and choose one of the following age ranges: 0-15, 15-35, 35-55, 55-70, or 70-80

fig, axs = plt.subplots()

axs.set_xlabel('Age')
axs.set_ylabel('Number of patients')

axs.hist(total_set.age, bins=[0, 15, 35, 55, 70, 80], ec="black")
axs.set_title('Age distribution')

print("The answer to the 1st question: 15-35")

# 2. What is the most common diagnosis among patients in all hospitals? Create a pie chart

diagnosing = []
for diagnose in total_set.diagnosis.unique():
    diagnosing.append(diagnose)

diagnosed_numbers = []
for x in diagnosing:
    diagnosed_numbers.append(total_set.groupby('diagnosis').get_group(x).diagnosis.count())

fig1, ax1 = plt.subplots()
ax1.pie(diagnosed_numbers, labels=diagnosing, autopct='%1.1f%%')
ax1.axis('equal')
ax1.set_title('Diagnosis distribution')

print("The answer to the 2nd question: pregnancy")

# 3. Build a violin plot of height distribution by hospitals. Try to answer the questions.
# What is the main reason for the gap in values?
# Why there are two peaks, which correspond to the relatively small and big values?
# No special form is required to answer this question

general = total_set.groupby('hospital').get_group('general')
sports = total_set.groupby('hospital').get_group('sports')
prenatal = total_set.groupby('hospital').get_group('prenatal')

fig2, ax2 = plt.subplots(figsize=(7, 10))

ax2.violinplot(general.height)
ax2.violinplot(sports.height)
ax2.violinplot(prenatal.height)
ax2.set_title('Height distribution')

print("The answer to the 3rd question: It's because of the different units of the height. Some is in inches"
      "and some is in cm. Two peaks exists because of the different population distribution of hospitals.")

plt.show()
