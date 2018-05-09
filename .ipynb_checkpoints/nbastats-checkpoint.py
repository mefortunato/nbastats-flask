import json
import requests
import numpy as np
import pandas as pd

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}

def team_stats(year='2017-18'):    
    game_log_url = 'https://stats.nba.com/stats/leaguegamefinder?Conference=&DateFrom=&DateTo=&Division=&DraftNumber=&DraftRound=&DraftYear=&GB=N&LeagueID=00&Location=&Outcome=&PlayerOrTeam=T&Season={year}&SeasonType=Regular+Season&StatCategory=PTS&TeamID=&VsConference=&VsDivision=&VsTeamID='.format(year=year)
    resp = requests.get(game_log_url, headers=HEADERS)
    games = json.loads(resp.text)
    df = pd.DataFrame(data=games['resultSets'][0]['rowSet'], columns=games['resultSets'][0]['headers'])
    def get_pts_against(row):
        return df.loc[(df.GAME_ID == row.GAME_ID) & (df.TEAM_ABBREVIATION != row.TEAM_ABBREVIATION)].PTS.values[0]
    df['PTS_A'] = df.apply(get_pts_against, axis=1)
    df['FG2M'] = df['FGM']-df['FG3M']
    df['FG2A'] = df['FGA']-df['FG3A']
    df['FG2_PCT'] = df['FG2M']/df['FG2A']
    teams = np.array_split(df.sort_values(['TEAM_ABBREVIATION', 'GAME_DATE']), len(set(df['TEAM_ABBREVIATION'])))
    for team in teams:
        team['WINS'] = team['WL'].map({'W': 1, 'L': 0}).expanding().sum()
        team['PTS_AVG'] = team['PTS'].expanding().mean()
        team['PTS_A_AVG'] = team['PTS_A'].expanding().mean()
        team['TOTAL_GAMES'] = len(team['PTS'])
        team['TOTAL_WINS'] = team['WINS'].values[-1]
        team['GP'] = range(1, 1+len(team['PTS']))
    df2 = pd.concat(teams)
    df2['PYE'] = np.power(df2['PTS_AVG'], 13.91)/(np.power(df2['PTS_AVG'], 13.91) + np.power(df2['PTS_A_AVG'], 13.91))
    df2['PYE_WINS'] = df2['PYE']*df2['GP']
    df2['PYE_WINS_ERROR'] = df2['WINS'] - df2['PYE_WINS']
    df2['PYE_WINS_ERROR_ABS'] = np.abs(df2['WINS'] - df2['PYE_WINS'])
    df2['PYE_PROJ'] = df2['WINS'] + df2['PYE']*(df2['TOTAL_GAMES']-df2['GP'])
    df2['PYE_PROJ_ERROR'] = df2['TOTAL_WINS'] - df2['PYE_PROJ']
    df2['PYE_PROJ_ERROR_ABS'] = np.abs(df2['TOTAL_WINS'] - df2['PYE_PROJ'])
    
    return df2