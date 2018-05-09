import os
import numpy as np
import pandas as pd
from flask import Flask, render_template, request, jsonify, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/get-stats/', defaults={'year': 2017})
@app.route('/get-stats/<int:year>/')
def get_stats(year=2017):
    df = pd.read_csv('static/dat/1983-2017.csv')
    season_id = float('2'+str(year))
    teams_2017 = df.loc[df['SEASON_ID']==season_id].groupby('TEAM_ABBREVIATION').mean()
    return(jsonify(year=year, stats=teams_2017[['TOTAL_WINS', 'PYE_PROJ', 'PTS', 'PTS_A', 'FGM', 'FGA', 'FG_PCT', 'FG2M', 'FG2A', 'FG2_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT']].to_json()))