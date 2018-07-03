import pickle
from pipeline import read_data, TRAIN_STATS, process_pipeline, fit_pipeline

data = read_data('static/dat/br-raw_2007-2018.csv')
totals = read_data('static/dat/totals.csv')
spreads = read_data('static/dat/spreads.csv')
moneylines = read_data('static/dat/moneylines.csv')

data = data.merge(spreads[['abrv', 'date', 'spread']], how='outer', left_on=['team', 'date'], right_on=['abrv', 'date'])
data = data.merge(totals[['abrv', 'date', 'total']], how='outer', left_on=['team', 'date'], right_on=['abrv', 'date'])
data = data.merge(moneylines[['abrv', 'date', 'moneylines']], how='outer', left_on=['home_abrv', 'date'], right_on=['abrv', 'date'])
data = data.merge(moneylines[['abrv', 'date', 'moneylines']], how='outer', left_on=['visitor_abrv', 'date'], right_on=['abrv', 'date'], suffixes=['_home', '_away'])

p = process_pipeline().transform(data)

train = p.dropna(subset=TRAIN_STATS+['spread_cover', 'spread', 'total_cover', 'total', 'moneylines_home', 'moneylines_away'])

X = train[TRAIN_STATS]
win_y = train['win']
spread_y = train['spread_cover']
total_y = train['total_cover']

win_est = fit_pipeline(TRAIN_STATS)
win_est.fit(X, win_y)
win_est.score(X, win_y)

spread_est = fit_pipeline(TRAIN_STATS)
spread_est.fit(X, spread_y)
spread_est.score(X, spread_y)

total_est = fit_pipeline(TRAIN_STATS)
total_est.fit(X, total_y)
total_est.score(X, total_y)

with open('static/dat/win_model.pkl', 'wb') as f:
    pickle.dump(win_est, f)
    
with open('static/dat/spread_model.pkl', 'wb') as f:
    pickle.dump(spread_est, f)
    
with open('static/dat/total_model.pkl', 'wb') as f:
    pickle.dump(total_est, f)