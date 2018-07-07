import numpy as np
import pandas as pd
from sklearn import base
from sklearn.pipeline import Pipeline

BASIC_STATS = [
    'fg', 'fga', 'fg_pct', 'fg3', 'fg3a', 'fg3_pct', 'ft', 'fta', 'ft_pct', 
    'orb', 'drb', 'trb', 'ast', 'stl', 'blk', 'tov', 'pf', 'pts'
]
BASIC_STATS += [stat+'_a' for stat in BASIC_STATS]

ADV_STATS = [
    'ts_pct', 'efg_pct', 'fg3a_per_fga_pct', 'fta_per_fga_pct', 'orb_pct', 'drb_pct', 
    'trb_pct', 'ast_pct', 'stl_pct', 'blk_pct', 'tov_pct', 'usg_pct', 'off_rtg', 'def_rtg'
]
ADV_STATS += [stat+'_a' for stat in ADV_STATS]

META_STATS = [
    'home', 'rest'
]

BET_STATS = [
    'moneyline', 'moneyline_a', 'win', 'spread', 'spread_cover', 'total', 'total_cover'
]

class FeatureSelectionTransformer(base.BaseEstimator, base.TransformerMixin):
    def __init__(self, features):
        self.features = features
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        return X[self.features]
    

class DropNATransformer(base.BaseEstimator, base.TransformerMixin):
    def __init__(self, features):
        self.features = features
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        return X.dropna(subset=self.features)
    
    
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
    
    
class ExpandingAverageTransformer(base.BaseEstimator, base.TransformerMixin):
    def __init__(self, stats):
        self.stats = stats
        self.avg_stats = ['avg_'+stat for stat in self.stats]
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        X[self.avg_stats] = X.sort_values('date').groupby(['season', 'team'])[self.stats].expanding().mean().reset_index((0,1))[self.stats]
        X[self.avg_stats] = X.sort_values('date').groupby(['season', 'team'])[self.avg_stats].shift(1)
        return X
    
    
class LastNTransformer(base.BaseEstimator, base.TransformerMixin):
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
    def __init__(self, stats):
        self.stats = stats
        
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        if X.index.name != 'id':
            X = X.set_index('id')
        home = X.loc[X['home']==1]
        away = X.loc[X['home']==0]
        home_n = home.merge(away[self.stats], left_index=True, right_index=True, suffixes=('', '_opp'))
        away_n = away.merge(home[self.stats], left_index=True, right_index=True, suffixes=('', '_opp'))
        home_away = pd.concat([home_n, away_n])
        return home_away
    

class EstimatorProbTransformer(base.BaseEstimator, base.TransformerMixin):
    
    def __init__(self, estimator):
        self.estimator = estimator
    
    def fit(self, X, y):
        self.estimator.fit(X, y)
        return self
    
    def transform(self, X):
        return self.estimator.predict_proba(X)[:, 1].reshape(-1, 1)
    
    
class EstimatorBinaryTransformer(base.BaseEstimator, base.TransformerMixin):
    
    def __init__(self, estimator):
        self.estimator = estimator
    
    def fit(self, X, y):
        self.estimator.fit(X, y)
        return self
    
    def transform(self, X):
        return self.estimator.predict(X).reshape(-1, 1)
    
    
class EstimatorDecisionTransformer(base.BaseEstimator, base.TransformerMixin):
    
    def __init__(self, estimator):
        self.estimator = estimator
    
    def fit(self, X, y):
        self.estimator.fit(X, y)
        return self
    
    def transform(self, X):
        return self.estimator.decision_function(X).reshape(-1, 1)
    

TRANSFORM_STATS = ['avg_'+stat for stat in BASIC_STATS+ADV_STATS+META_STATS+BET_STATS]
TRAIN_STATS = TRANSFORM_STATS+[stat+'_opp' for stat in TRANSFORM_STATS]

process_pipeline = Pipeline([
    ('cover', CoverTransformer()),
    ('gp', GPTransformer()),
    ('rest', RestTransformer()),
    ('exp_avg', ExpandingAverageTransformer(BASIC_STATS+ADV_STATS+META_STATS+BET_STATS)),
    ('opp_stat', OpponentStatsTransformer(TRANSFORM_STATS)),
    ('dropna', DropNATransformer(TRAIN_STATS))
])