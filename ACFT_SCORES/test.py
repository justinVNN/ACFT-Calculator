import pandas as pd
import numpy as np

MR = pd.read_csv('2MR_MALE.csv')
print(MR)
age = 22
gender = "Male"
standing_power_throw = "9.0"
deadlift = "300"
points_earned = 0
hand_release_push_up = "50"
sprint_drag_carry = "140"
plank = "300"
two_mile_run = "1800"

def get_event_score(age,gender,event,raw_score):
    df = pd.read_csv(f'{event}_{gender.upper()}.csv')
    points_earned = 0
    raw_score = float(raw_score.strip())
    if event == "SDC" or event == "2MR":
        for i in reversed(range(len(df))):
            try:
                age_score = float(df[f'{age}'][i])
            except:
                continue
            if age_score == raw_score:
                points_earned = df['Points'][i]
                break
            elif age_score > raw_score:
                points_earned = df['Points'][i-1]
                break
        return points_earned
    for i in range(len(df)):
        try:
            age_score = float(df[f'{age}'][i])
        except:
            continue
        if age_score == raw_score:
            points_earned = df['Points'][i]
            break
        elif age_score > raw_score:
            points_earned = df['Points'][i-1]
            break
    return points_earned


EVENT_NAME = ["MDL", "SPT", "HRP", "SDC", "PLK", "2MR"]
RAW_SCORE = [deadlift, standing_power_throw, hand_release_push_up, sprint_drag_carry, plank, two_mile_run]
FINAL_SCORE = 0
for i in range(len(EVENT_NAME)):
    print(f"EVENT_NAME[{i}]: ", EVENT_NAME[i])
    FINAL_SCORE = FINAL_SCORE + get_event_score(age, gender, EVENT_NAME[i], RAW_SCORE[i])
    
print(FINAL_SCORE)

""" MDL_frame = MDL_frame[[f'{age}', 'Points']]
# deadlift_score = MDL_frame.loc[MDL_frame[f'{age}'] == int(deadlift)]['Points'].values[0]
# find the index of the row that contains the deadlift value
score_index = MDL_frame.index[MDL_frame[f'{age}'] == standing_power_throw].tolist()
if score_index == []:
        #if the raw score is not in the column, use the next highest value
        score_index = MDL_frame.index[MDL_frame[f'{age}'] > standing_power_throw].tolist()
        score_index = score_index[2]
        points_earned = MDL_frame.iloc[score_index]['Points']
# print the score from the "Points" column at the index of the deadlift value
else:
    points_earned = MDL_frame.iloc[score_index]['Points'].values[0]


EVENT_NAME = ["MDL", "SPT", "HRP", "SDC", "PLK", "2MR"]
RAW_SCORE = [deadlift, standing_power_throw, hand_release_push_up, sprint_drag_carry, plank, two_mile_run]

# for item in list(zip(EVENT_NAME, RAW_SCORE)):
#     print(item)

# print(MDL_frame)
print(score_index)
points_earned = int(points_earned)
print(type(points_earned))
print(points_earned) """