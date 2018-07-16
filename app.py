import os
import json
import pickle
import datetime
import numpy as np
import pandas as pd
from sklearn.preprocessing import scale
from sklearn.linear_model import LogisticRegression
from flask import Flask, render_template, request, jsonify, url_for

from transformers import process_pipeline

app = Flask(__name__)

with open('static/dat/logos.json') as f:
    LOGOS = json.load(f)

DATA = pd.read_csv('static/dat/combined-with-spreads.csv', index_col=0)
DATA = process_pipeline.transform(DATA)

with open('static/dat/win_model_v2.pkl', 'rb') as f:
    win_est = pickle.load(f)
    
with open('static/dat/spread_model_v2.pkl', 'rb') as f:
    spread_est = pickle.load(f)
    
with open('static/dat/total_model_v2.pkl', 'rb') as f:
    total_est = pickle.load(f)
    
def predict_games_df(df):
    if len(df) == 0:
        return {}
    df['win_pred_proba'] = list(win_est.predict_proba(df)[:, 1])
    df['spread_pred_proba'] = list(spread_est.predict_proba(df)[:, 1])
    df['total_pred_proba'] = list(total_est.predict_proba(df)[:, 1])
    df['win_pred'] = list(win_est.predict(df))
    df['spread_pred'] = list(spread_est.predict(df))
    df['total_pred'] = list(total_est.predict(df))
    return df[['team', 'home_abrv', 'visitor_abrv', 'pts', 'pts_a', 'win', 'moneyline', 'moneyline_a', 'spread', 'total', 'spread_cover', 'total_cover', 'win_pred', 'spread_pred', 'total_pred', 'win_pred_proba', 'spread_pred_proba', 'total_pred_proba']].round(2).to_dict('index')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/performance/')
def performance():
    return render_template('performance.html')

@app.route('/insights/')
def insights():
    return render_template('insights.html')

@app.route('/games/', defaults={'date': '2018-06-08'})
@app.route('/games/<date>/')
def games(date='2018-06-08'):
    df = DATA[(DATA['date']==date) & (DATA['home']==1)].copy()
    games = predict_games_df(df)
    return render_template('games.html', date=date)

@app.route('/games-legacy/', defaults={'date': '2018-06-08'})
@app.route('/games-legacy/<date>/')
def games_legacy(date='2018-06-08'):
    return render_template('games-legacy.html', games=games, date=date, logos=LOGOS)

@app.route('/get-games/', defaults={'date': '2018-06-08'})
@app.route('/get-games/<date>/')
def get_games(date='2018-06-08'):
    df = DATA[(DATA['date']==date) & (DATA['home']==1)].copy()
    games = list(predict_games_df(df).values())
    return jsonify(games=games)

@app.route('/get-logos/')
def get_logos():
    return jsonify(logos=LOGOS)

@app.route('/play/')
def play():
    return render_template('play.html')

@app.route('/random-game/')
def random_game():
    game = DATA[(DATA['season']==2018) & (DATA['home']==1)].sample()
    game['win_pred'] = list(win_est.predict(game))
    game['spread_pred'] = list(spread_est.predict(game))
    game['total_pred'] = list(total_est.predict(game))
    game['win_pred_proba'] = list(win_est.predict_proba(game)[:, 1])
    game['spread_pred_proba'] = list(spread_est.predict_proba(game)[:, 1])
    game['total_pred_proba'] = list(total_est.predict_proba(game)[:, 1])
    game = game[['date', 'home_abrv', 'visitor_abrv', 'pts', 'pts_a', 'win', 'spread', 'total', 'spread_cover', 'total_cover', 'win_pred', 'spread_pred', 'total_pred', 'win_pred_proba', 'spread_pred_proba', 'total_pred_proba']]
    logos = [LOGOS.get(game.home_abrv.values[0]), LOGOS.get(game.visitor_abrv.values[0])]
    date = game['date'].astype(str).values[0]
    return jsonify(info=game.to_dict('index'), logos=logos, date=date)

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