import json
import requests
import pandas as pd

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}

game_log_url = 'https://stats.nba.com/stats/leaguegamefinder?Conference=&DateFrom=&DateTo=&Division=&DraftNumber=&DraftRound=&DraftYear=&GB=N&LeagueID=00&Location=&Outcome=&PlayerOrTeam=T&Season=2017-18&SeasonType=Regular+Season&StatCategory=PTS&TeamID=&VsConference=&VsDivision=&VsTeamID='

def get_attendance(game_id):
    attendance_url = 'https://stats.nba.com/stats/boxscoresummaryv2?GameID={}'.format(game_id)
    resp = requests.get(attendance_url, headers=HEADERS)
    game = json.loads(resp.text)
    return game['resultSets'][4]['rowSet'][0][1]

resp = requests.get(game_log_url, headers=HEADERS)
games_2017=json.loads(resp.text)
df = pd.DataFrame(data=games_2017['resultSets'][0]['rowSet'], columns=games_2017['resultSets'][0]['headers'])
