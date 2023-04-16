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
    df = pd.read_csv(f'{event}_{gender.upper()}.csv')
    df = df[[f'{age}', 'Points']]
    score_index = df.index[df[f'{age}'] == raw_score].tolist()
    if score_index == []:
        #if the raw score is not in the column, use the next highest value
        score_index = df.index[df[f'{age}'] > raw_score].tolist()
        score_index = score_index[2]
        points_earned = df.iloc[score_index]['Points']
    else:
        points_earned = df.iloc[score_index]['Points'].values[0]
    return int(points_earned)


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
        sprint_drag_carry = request.form.get('SDC_min') +":"+ request.form.get('SDC_sec')
        plank= request.form.get('PLK_min') +":"+ request.form.get('PLK_sec')
        two_mile_run = request.form.get('2MR_min') +":"+ request.form.get('2MR_sec')
        #convert the time to seconds
        sprint_drag_carry = str((int(sprint_drag_carry.split(':')[0]) * 60) + int(sprint_drag_carry.split(':')[1]))
        plank = str((int(plank.split(':')[0]) * 60) + int(plank.split(':')[1]))
        two_mile_run = str((int(two_mile_run.split(':')[0]) * 60) + int(two_mile_run.split(':')[1]))
        
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
        for i in range(len(EVENT_NAME)):
            FINAL_SCORE += get_event_score(age, gender, EVENT_NAME[i],RAW_SCORE[i])
        return render_template('calculator.html', total_score = FINAL_SCORE)
        
    # return render_template('calculator.html')

if __name__ == '__main__':
    app.run(host = "143.42.2.212", debug= True)