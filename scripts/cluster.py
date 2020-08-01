"""
Clustering analysis of regions.

Written by Ed Oughton

July 2020

"""
import os
import configparser
import pandas as pd
# k-means clustering
from numpy import unique
from numpy import where
from sklearn.datasets import make_classification
from sklearn.cluster import KMeans
from matplotlib import pyplot

CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(os.path.dirname(__file__), 'script_config.ini'))
BASE_PATH = CONFIG['file_locations']['base_path']

DATA_INTERMEDIATE = os.path.join(BASE_PATH, 'intermediate')

# define dataset
data = pd.read_csv(os.path.join(DATA_INTERMEDIATE, 'all_regional_data.csv'))#[:100]
# data['population_millions'] = data['population'] / 1e6

data = data[[
    'population_km2',
    'coverage_GSM_percent',
    'coverage_3G_percent',
    'coverage_4G_percent',
    'sites_estimated_km2',
    ]]#'population']]#,

# define the model
model = KMeans(n_clusters=10)

# fit the model
model.fit(data)

# assign clusters
yhat = model.predict(data)
yhat = pd.DataFrame(yhat)

# add cluster numbers back to original data
results = pd.concat([data, yhat], axis=1)
results.columns = [
    'population_km2',
    'coverage_GSM_percent',
    'coverage_3G_percent',
    'coverage_4G_percent',
    'sites_estimated_km2',
    'cluster'
]

# export results
path = os.path.join(DATA_INTERMEDIATE, 'clusters.csv')
results.to_csv(path, index=False)
