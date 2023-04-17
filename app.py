import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
from os import path
import hashlib
import pandas as pd
import sys

app = Flask(__name__)
ROOT = path.dirname(path.realpath(__file__))

with open(path.join(ROOT, "secrets.txt"),'r') as f:
    s = f.readlines()
app.secret_key = s[0].strip()


def hash(data):
    return hashlib.sha224(data.replace('\n', '').encode('ascii')).hexdigest()

# @app.route('/')
# def index():
#     conn = get_db_connection()
#     posts = conn.execute('SELECT * FROM posts').fetchall()
#     conn.close()
#     return render_template('index.html', posts=posts)

@app.route('/')
def index():
    return render_template('welcome.html')


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))

def get_event_score(age,gender,event,raw_score):
    df = pd.read_csv(f'ACFT_SCORES/{event}_{gender.upper()}.csv')
    points_earned = 0
    raw_score = float(raw_score.strip())
    if raw_score >= float(df[f'{age}'][len(df)-1]):
        return df['Points'][len(df)-1]
    
    if event == "SDC" or event == "2MR":
        #if the event is the sprint drag carry or the two mile run, the scores are in reverse order
        for i in reversed(range(len(df))):
            try:
                age_score = float(df[f'{age}'][i])
            except:
                continue
            if age_score == raw_score:
                points_earned = df['Points'][i]
                break
            elif age_score > raw_score:
                points_earned = df['Points'][i+1]
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


@app.route('/calculator', methods=('GET', 'POST'))
def calculator():
    #read in the csv file
    if request.method == 'GET':
        return render_template('calculator.html')
    elif request.method == 'POST':
        age = request.form.get('age')
        gender = request.form.get('gender')
        deadlift = request.form.get('MDL')  
        standing_power_throw = request.form.get('SPT')
        hand_release_push_up = request.form.get('HRP')
        
        #combine the minutes and seconds into one value and convert to seconds
        sprint_drag_carry = request.form.get('SDC_min')
        plank= request.form.get('PLK_min')
        two_mile_run = request.form.get('2MR_min')
        if request.form.get('SDC_sec') == '0':
            sprint_drag_carry = sprint_drag_carry + '00'
        else:
            sprint_drag_carry = sprint_drag_carry + request.form.get('SDC_sec')
        if request.form.get('PLK_sec') == '0':
            plank = plank + '00'
        else:
            plank = plank + request.form.get('PLK_sec')
        if request.form.get('2MR_sec') == '0':
            two_mile_run = two_mile_run + '00'
        else:
            two_mile_run = two_mile_run + request.form.get('2MR_sec')
        
        
        EVENT_NAME = ["MDL", "SPT", "HRP", "SDC", "PLK", "2MR"]
        RAW_SCORE = [deadlift, standing_power_throw, hand_release_push_up, sprint_drag_carry, plank, two_mile_run]
        
        #use only the columns that contain the age and score
        age = int(age)
        if age >= 17 and age <= 21:
            age = 17
        elif age >= 22 and age <= 26:
            age = 22
        elif age >= 27 and age <= 31:
            age = 27
        elif age >= 32 and age <= 36:
            age = 32
        elif age >= 37 and age <= 41:
            age = 37
        elif age >= 42 and age <= 46:
            age = 42
        elif age >= 47 and age <= 51:
            age = 47
        elif age >= 52 and age <= 56:
            age = 52
        elif age >= 57 and age <= 61:
            age = 57
        elif age >= 62:
            age = 62
        
        #RAW_SCORE is stored strings
        #get the score for each event
        FINAL_SCORE = 0
        SCORE_LIST = []
        for i in range(len(EVENT_NAME)):
            SCORE_LIST.append(get_event_score(age,gender,EVENT_NAME[i],RAW_SCORE[i]))
        FINAL_SCORE = sum(SCORE_LIST)
    
        
        return render_template('calculator.html', total_score=FINAL_SCORE, MDL_score = SCORE_LIST[0], SPT_score = SCORE_LIST[1], HRP_score = SCORE_LIST[2], SDC_score = SCORE_LIST[3], PLK_score = SCORE_LIST[4], TWOMR_score = SCORE_LIST[5])
        

if __name__ == '__main__':
    app.run(host = "143.42.2.212", debug= True)