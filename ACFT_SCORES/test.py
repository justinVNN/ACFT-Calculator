import pandas as pd
import numpy as np

MDL_frame = pd.read_csv('MDL_MALE.csv')
age = 22
deadlift = "300"
MDL_frame = MDL_frame[[f'{age}', 'Points']]
# deadlift_score = MDL_frame.loc[MDL_frame[f'{age}'] == int(deadlift)]['Points'].values[0]
# find the index of the row that contains the deadlift value
score_index = MDL_frame.index[MDL_frame[f'{age}'] == deadlift].tolist()
if score_index == []:
        #if the raw score is not in the column, use the next highest value
        score_index = MDL_frame.index[MDL_frame[f'{age}'] > deadlift].tolist()
        score_index = score_index[2]
        points_earned = MDL_frame.iloc[score_index]['Points']
# print the score from the "Points" column at the index of the deadlift value
else:
    points_earned = MDL_frame.iloc[score_index]['Points'].values[0]


# print(MDL_frame)
# print(score_index)
points_earned = int(points_earned)
print(type(points_earned))
print(points_earned)