import os
import numpy as np
import pandas as pd
from flask import Flask, render_template, request, jsonify, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/team-stats/')
def team_stats():
    return render_template('team-stats.html')

@app.route('/get-stats/', defaults={'year': 2017})
@app.route('/get-stats/<int:year>/')
def get_stats(year=2017):
    df = pd.read_csv('static/dat/1983-2017.csv')
    season_id = float('2'+str(year))
    teams_2017 = df.loc[df['SEASON_ID']==season_id].groupby('TEAM_ABBREVIATION').mean()
    return(jsonify(year=year, stats=teams_2017[['TOTAL_WINS', 'PYE_PROJ', 'PTS', 'PTS_A', 'FGM', 'FGA', 'FG_PCT', 'FG2M', 'FG2A', 'FG2_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT']].to_json()))

@app.route('/get-pye-error/')
def get_pye_error():
    df = pd.read_csv('static/dat/1983-2017.csv')
    mean = df.groupby('GP').mean()['PYE_WINS_ERROR_ABS']
    std = df.groupby('GP').std()['PYE_WINS_ERROR_ABS']
    return(jsonify(mean=mean.to_json(), std=std.to_json()))

@app.route('/get-proj-pye-error/')
def get_proj_pye_error():
    df = pd.read_csv('static/dat/1983-2017.csv')
    mean = df.groupby('GP').mean()['PYE_PROJ_ERROR_ABS']
    std = df.groupby('GP').std()['PYE_PROJ_ERROR_ABS']
    return(jsonify(mean=mean.to_json(), std=std.to_json()))