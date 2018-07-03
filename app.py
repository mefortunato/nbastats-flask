import os
import json
import pickle
import datetime
import numpy as np
import pandas as pd
from sklearn.preprocessing import scale
from sklearn.linear_model import LogisticRegression
from flask import Flask, render_template, request, jsonify, url_for

from pipeline import read_data, TRAIN_STATS, process_pipeline, fit_pipeline

app = Flask(__name__)

def prepare_data():
    data = read_data('static/dat/br-raw_2007-2018.csv')
    totals = read_data('static/dat/totals.csv')
    spreads = read_data('static/dat/spreads.csv')
    moneylines = read_data('static/dat/moneylines.csv')
    data = data.merge(spreads[['abrv', 'date', 'spread']], how='outer', left_on=['team', 'date'], right_on=['abrv', 'date'])
    data = data.merge(totals[['abrv', 'date', 'total']], how='outer', left_on=['team', 'date'], right_on=['abrv', 'date'])
    data = data.merge(moneylines[['abrv', 'date', 'moneylines']], how='outer', left_on=['home_abrv', 'date'], right_on=['abrv', 'date'])
    data = data.merge(moneylines[['abrv', 'date', 'moneylines']], how='outer', left_on=['visitor_abrv', 'date'], right_on=['abrv', 'date'], suffixes=['_home', '_away'])
    return process_pipeline().transform(data)

DATA = prepare_data()

with open('static/dat/win_model.pkl', 'rb') as f:
    win_est = pickle.load(f)
    
with open('static/dat/spread_model.pkl', 'rb') as f:
    spread_est = pickle.load(f)
    
with open('static/dat/total_model.pkl', 'rb') as f:
    total_est = pickle.load(f)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/test')
def test():
    df = DATA[DATA['date']=='2018-03-26']
    return jsonify(df.sort_values('id')[['avg_pts', 'avg_pts_a', 'home_avg_pts', 'home_avg_pts_a', 'spread']].to_json())

@app.route('/games/', defaults={'date': '2018-03-26'})
@app.route('/games/<date>/')
def predict(date='2018-03-26'):
    df = DATA[(DATA['date']==date) & (DATA['home']==1)].copy()
    if len(df) == 0:
        return render_template('date-view.html', games={}, date=date)
    df['win_pred_proba'] = list(win_est.predict_proba(df[TRAIN_STATS])[:, 1])
    df['spread_pred_proba'] = list(spread_est.predict_proba(df[TRAIN_STATS])[:, 1])
    df['total_pred_proba'] = list(total_est.predict_proba(df[TRAIN_STATS])[:, 1])
    df['win_pred'] = list(win_est.predict(df[TRAIN_STATS]))
    df['spread_pred'] = list(spread_est.predict(df[TRAIN_STATS]))
    df['total_pred'] = list(total_est.predict(df[TRAIN_STATS]))
    games = df[['team', 'home_abrv', 'visitor_abrv', 'pts', 'pts_a', 'home_avg_pts', 'home_avg_pts_a', 'away_avg_pts_opp', 'away_avg_pts_a_opp', 'win', 'moneylines_home', 'moneylines_away', 'spread', 'total', 'spread_cover', 'total_cover', 'win_pred', 'spread_pred', 'total_pred', 'win_pred_proba', 'spread_pred_proba', 'total_pred_proba']].round(2).to_dict('index')
    return render_template('date-view.html', games=games, date=date)

@app.route('/team-stats/')
def team_stats():
    return render_template('team-stats.html')

@app.route('/get-stats/', defaults={'year': 2017})
@app.route('/get-stats/<int:year>/')
def get_stats(year=2017):
    df = pd.read_csv('static/dat/1983-2017.csv')
    season_id = float('2'+str(year))
    STATS = ['TOTAL_WINS', 'PTS', 'PTS_A', 'FGM', 'FGA', 'FG_PCT', 'FG2M', 'FG2A', 'FG2_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PLUS_MINUS']
    teams = df.loc[df['SEASON_ID']==season_id].groupby('TEAM_ABBREVIATION').mean()
    return(jsonify(year=year, stats=teams[STATS].to_json()))

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

if __name__ == '__main__':
    app.run(DEBUG=True)