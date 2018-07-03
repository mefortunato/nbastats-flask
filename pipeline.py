import numpy as np
import pandas as pd
from sklearn import base
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.feature_selection import RFECV
from sklearn.linear_model import RidgeClassifier, LogisticRegression

STATS = ['fg', 'fga', 'fg_pct', 'fg3', 'fg3a', 'fg3_pct', 'ft', 'fta', 'ft_pct', 'orb', 'drb', 'trb', 'ast', 'stl', 'blk', 'tov', 'pf', 'pts', 'ts_pct', 'efg_pct', 'fg3a_per_fga_pct', 'fta_per_fga_pct', 'orb_pct', 'drb_pct', 'trb_pct', 'ast_pct', 'stl_pct', 'blk_pct', 'tov_pct', 'usg_pct', 'off_rtg', 'def_rtg', 'fg_a', 'fga_a', 'fg_pct_a', 'fg3_a', 'fg3a_a', 'fg3_pct_a', 'ft_a', 'fta_a', 'ft_pct_a', 'orb_a', 'drb_a', 'trb_a', 'ast_a', 'stl_a', 'blk_a', 'tov_a', 'pf_a', 'pts_a', 'ts_pct_a', 'efg_pct_a', 'fg3a_per_fga_pct_a', 'fta_per_fga_pct_a', 'orb_pct_a', 'drb_pct_a', 'trb_pct_a', 'ast_pct_a', 'stl_pct_a', 'blk_pct_a', 'tov_pct_a', 'usg_pct_a', 'off_rtg_a', 'def_rtg_a', 'win', 'spread_cover', 'total_cover']

TRAIN_STATS = []
for stat in STATS:
    TRAIN_STATS.append('avg_{}'.format(stat))
    TRAIN_STATS.append('avg_{}_opp'.format(stat))
    TRAIN_STATS.append('home_avg_{}'.format(stat))
    TRAIN_STATS.append('away_avg_{}_opp'.format(stat))
    TRAIN_STATS.append('last_5_{}'.format(stat))
    TRAIN_STATS.append('last_5_{}_opp'.format(stat))
    TRAIN_STATS.append('home_last_5_{}'.format(stat))
    TRAIN_STATS.append('away_last_5_{}_opp'.format(stat))

class FeatureSelectionTransformer(base.BaseEstimator, base.TransformerMixin):
    def __init__(self, features):
        self.features = features
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        return X[self.features]
    
    
class DropNATransformer(base.BaseEstimator, base.TransformerMixin):
    def __init__(self, train_stats):
        self.train_stats = train_stats
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        return X.dropna(subset=self.train_stats+['spread_cover', 'spread', 'total_cover', 'total', 'moneylines_home', 'moneylines_away'])
    
    
class TeamSeasonSelector(base.BaseEstimator, base.TransformerMixin):
    def __init__(self, team, season):
        self.team = team
        self.season = season
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        return X.loc[(X['season']==self.season) & (X['team']==self.team)]
    
    
class GPTransformer(base.BaseEstimator, base.TransformerMixin):
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        X['gp'] = X.sort_values('date').groupby(['season', 'team'])['pts'].expanding().count().reset_index((0, 1))['pts']
        return X
    
    
    
class RestTransformer(base.BaseEstimator, base.TransformerMixin):
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        X['date'] = pd.to_datetime(X['date'])
        X['rest'] = X.sort_values('date').groupby(['season', 'team'])['date'].diff().dt.days-1
        return X
    
    
class CoverTransformer(base.BaseEstimator, base.TransformerMixin):
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        X['spread_cover'] = (X['plus_minus'] + X['spread'] > 0.0).astype(int)
        X.loc[(np.abs(X['plus_minus'] + X['spread']) < 1e-5), 'spread_cover'] = np.NaN
        
        X['total_cover'] = ((X['pts']+X['pts_a']) > X['total']).astype(int)
        X.loc[np.abs(X['pts']+X['pts_a'] - X['total']) < 1e-5, 'total_cover'] = np.NaN
        return X
    
    
class GetHomeTransformer(base.BaseEstimator, base.TransformerMixin):
    def __init__(self, home=True):
        self.home = home
        
    def fit(self, X, y):
        return self
    
    def transform(self, X):
        return X[X['home']==int(self.home)]
    
    
class LastNGamesTransformer(base.BaseEstimator, base.TransformerMixin):
    def __init__(self, stats, n):
        self.stats = stats
        self.avg_stats = ['last_{}_'.format(n)+stat for stat in self.stats]
        self.n = n
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        X[self.avg_stats] = X.sort_values('date').groupby(['season', 'team'])[self.stats].rolling(self.n, self.n).mean().reset_index((0,1))[self.stats]
        X[self.avg_stats] = X.sort_values('date').groupby(['season', 'team'])[self.avg_stats].shift(1)
        return X
    
    
class AverageStatsTransformer(base.BaseEstimator, base.TransformerMixin):
    def __init__(self, stats):
        self.stats = stats
        self.avg_stats = ['avg_'+stat for stat in self.stats]
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        X[self.avg_stats] = X.sort_values('date').groupby(['season', 'team'])[self.stats].expanding().mean().reset_index((0,1))[self.stats]
        X[self.avg_stats] = X.sort_values('date').groupby(['season', 'team'])[self.avg_stats].shift(1)
        return X
    
    
class HomeAwayLastNTransformer(base.BaseEstimator, base.TransformerMixin):
    def __init__(self, stats, n):
        self.stats = stats
        self.n = n
        self.home_avg_stats = ['home_last_{}_'.format(n)+stat for stat in self.stats]
        self.away_avg_stats = ['away_last_{}_'.format(n)+stat for stat in self.stats]
        
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        home = X.loc[X['home']==1].sort_index()
        home[self.home_avg_stats] = home.sort_values('date').groupby(['season', 'team'])[self.stats].rolling(self.n, self.n).mean().reset_index((0,1))[self.stats]
        home[self.home_avg_stats] = home.sort_values('date').groupby(['season', 'team'])[self.home_avg_stats].shift(1)
        
        away = X.loc[X['home']==0].sort_index()
        away[self.away_avg_stats] = away.sort_values('date').groupby(['season', 'team'])[self.stats].rolling(self.n, self.n).mean().reset_index((0,1))[self.stats]
        away[self.away_avg_stats] = away.sort_values('date').groupby(['season', 'team'])[self.away_avg_stats].shift(1)
        
        home_away = pd.concat([home, away], sort=True)
        return home_away
        
    
    
class HomeAwaySplitsTransformer(base.BaseEstimator, base.TransformerMixin):
    def __init__(self, stats):
        self.stats = stats
        self.home_avg_stats = ['home_avg_'+stat for stat in self.stats]
        self.away_avg_stats = ['away_avg_'+stat for stat in self.stats]
        
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        home = X.loc[X['home']==1].set_index('id', drop=True).sort_index()
        home[self.home_avg_stats] = home.sort_values('date').groupby(['season', 'team'])[self.stats].expanding().mean().reset_index((0,1))[self.stats]
        home[self.home_avg_stats] = home.sort_values('date').groupby(['season', 'team'])[self.home_avg_stats].shift(1)
        
        away = X.loc[X['home']==0].set_index('id', drop=True).sort_index()
        away[self.away_avg_stats] = away.sort_values('date').groupby(['season', 'team'])[self.stats].expanding().mean().reset_index((0,1))[self.stats]
        away[self.away_avg_stats] = away.sort_values('date').groupby(['season', 'team'])[self.away_avg_stats].shift(1)
        
        home_away = pd.concat([home, away], sort=True)
        return home_away
    
    
class OpponentStatsTransformer(base.BaseEstimator, base.TransformerMixin):
    def __init__(self, home_away='home'):
        self.home_away = home_away
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        home = X.loc[X['home']==1]
        away = X.loc[X['home']==0]
        home_n = home.merge(away, left_index=True, right_index=True, suffixes=('', '_opp'))
        away_n = away.merge(home, left_index=True, right_index=True, suffixes=('', '_opp'))
        home_away = pd.concat([home_n, away_n])
        return home_away
        #if self.home_away == 'home':
        #    return home_n
        #else:
        #    return away_n

def read_data(fname):
    return pd.read_csv(fname, index_col=0)

def process_pipeline(stats=STATS, train_stats=TRAIN_STATS, n_last_games=5):
    return Pipeline([
        ('cover', CoverTransformer()),
        ('gp', GPTransformer()),
        ('avg', AverageStatsTransformer(stats)),
        ('last_{}'.format(n_last_games), LastNGamesTransformer(stats, n_last_games)),
        ('home_away', HomeAwaySplitsTransformer(stats)),
        ('home_away_last_{}'.format(n_last_games), HomeAwayLastNTransformer(stats, n_last_games)),
        ('opp_stat', OpponentStatsTransformer()),
        ('home', GetHomeTransformer(True)),
        ('dropna', DropNATransformer(train_stats))
    ])

def fit_pipeline(train_stats=TRAIN_STATS):
    return Pipeline([
        ('feature_selection', FeatureSelectionTransformer(train_stats)),
        ('scale', StandardScaler()),
        ('logreg', LogisticRegression())
    ])