import pandas as pd
import numpy as np

age = 22
gender = "Male"
standing_power_throw = "11.8"
deadlift = "350"
points_earned = 0
hand_release_push_up = "50"
sprint_drag_carry = "1:25"
plank = "3:30"
two_mile_run = "18:25"

sprint_drag_carry = sprint_drag_carry.replace(':','')
plank = plank.replace(':','')
two_mile_run = two_mile_run.replace(':','')

def get_event_score(age,gender,event,raw_score):
    df = pd.read_csv(f'{event}_{gender.upper()}.csv')
    points_earned = 0
    raw_score = float(raw_score)
    if raw_score > float(df[f'{age}'][len(df)-1]):
        return df['Points'][len(df)-1]
    if event == "SDC" or event == "2MR":
        #if the event is the sprint drag carry or the two mile run, the scores are in reverse order
        if raw_score <= float(df[f'{age}'][len(df)-1]):
            return df['Points'][len(df)-1]
        for i in range(len(df)):
            try:
                age_score = float(df[f'{age}'][i])
            except:
                continue
            if age_score == raw_score:
                points_earned = df['Points'][i]
                break
            elif age_score < raw_score:
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
SCORE_LIST = []
for i in range(len(EVENT_NAME)):
    SCORE_LIST.append(get_event_score(age,gender,EVENT_NAME[i],RAW_SCORE[i]))
FINAL_SCORE = sum(SCORE_LIST)
print(FINAL_SCORE)
for i in range(len(EVENT_NAME)):
    print(f'{EVENT_NAME[i]}: {RAW_SCORE[i]}: {SCORE_LIST[i]}')