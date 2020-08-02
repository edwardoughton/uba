"""
Visualize data

"""
import os
import configparser
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
import contextily as ctx

CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(os.path.dirname(__file__), '..', 'scripts', 'script_config.ini'))
BASE_PATH = CONFIG['file_locations']['base_path']

DATA_RAW = os.path.join(BASE_PATH, 'raw')
DATA_INTERMEDIATE = os.path.join(BASE_PATH, 'intermediate')
VIS = os.path.join(BASE_PATH, '..', 'vis', 'figures')

def plot_median_per_user_cost(data):
    """

    """
    sns.set(font_scale=1.5)
    plot = sns.catplot(
        x='Decile', y='Cost Per User ($)', col="Scenario",
        col_order=['Low', 'Baseline', 'High'],
        row="Strategy", kind='bar', data=data, sharex=False
        )
    plot.set_xticklabels(rotation=30)
    plt.tight_layout()
    plot.savefig(os.path.join(VIS, 'per_user_cost_numeric.png'), dpi=300)

    return 'Complete'


def get_regional_shapes():
    """

    """
    output = []

    for item in os.listdir(DATA_INTERMEDIATE):#[:15]:
        if len(item) == 3: # we only want iso3 code named folders

            filename_gid2 = 'regions_2_{}.shp'.format(item)
            path_gid2 = os.path.join(DATA_INTERMEDIATE, item, 'regions', filename_gid2)

            filename_gid1 = 'regions_1_{}.shp'.format(item)
            path_gid1 = os.path.join(DATA_INTERMEDIATE, item, 'regions', filename_gid1)

            if os.path.exists(path_gid2):
                data = gpd.read_file(path_gid2)
                data['GID_id'] = data['GID_2']
                data = data.to_dict('records')

            elif os.path.exists(path_gid1):
                data = gpd.read_file(path_gid1)
                data['GID_id'] = data['GID_1']
                data = data.to_dict('records')
            else:
               print('No shapefiles for {}'.format(item))
               continue

            for datum in data:
                output.append({
                    'geometry': datum['geometry'],
                    'properties': {
                        'GID_id': datum['GID_id'],
                    },
                })

    output = gpd.GeoDataFrame.from_features(output, crs='epsg:4326')

    return output


def plot_regions_by_geotype(data, regions):
    """

    """
    data['population_km2'] = round(data['population_km2'])
    data = data[['GID_id', 'population_km2']]
    regions = regions[['GID_id', 'geometry']]#[:10]

    regions = regions.merge(data, left_on='GID_id', right_on='GID_id')
    regions.reset_index(drop=True, inplace=True)

    metric = 'population_km2'

    bins = [-1, 20, 43, 69, 109, 171, 257, 367, 541, 1104, 111607]
    labels = ['<20','20-43','43-69','69-109','109-171','171-257','257-367','367-541','541-1104','>1104']
    regions['bin'] = pd.cut(
        regions[metric],
        bins=bins,
        labels=labels
    )#.fillna('<20')

    fig, ax = plt.subplots(1, 1, figsize=(8,12))

    regions.plot(column='bin', ax=ax, cmap='inferno', linewidth=0, legend=True)

    #we probably need to fine tune the zoom level to bump up the resolution of the tiles
    ctx.add_basemap(ax, crs=regions.crs)

    fig.savefig(os.path.join(VIS, 'region_by_pop_density.pdf'))


def plot_regions_by_cost(data, regions):
    """

    """
    data = data.loc[data['scenario'] == 'Baseline']
    data = data.loc[data['strategy'] == '4G(MW)']
    data = data.loc[data['confidence'] == 50]

    data['total_cost'] = data['total_cost'] / 1e6
    data = data[['GID_id', 'total_cost']]
    regions = regions[['GID_id', 'geometry']]#[:10]

    regions = regions.merge(data, left_on='GID_id', right_on='GID_id')
    regions.reset_index(drop=True, inplace=True)

    metric = 'total_cost'

    bins = [-1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 10000]
    labels = ['<$10m', '$10-20m', '$20-30m','$30-40m','$40-50m','$50-60m',
        '$60-70m','$70-80m','$80-90m','$90-100m','>$100m']
    regions['bin'] = pd.cut(
        regions[metric],
        bins=bins,
        labels=labels
    )#.fillna('<20')

    fig, ax = plt.subplots(1, 1, figsize=(8,12))

    regions.plot(column='bin', ax=ax, cmap='inferno', linewidth=0, legend=True)

    #we probably need to fine tune the zoom level to bump up the resolution of the tiles
    ctx.add_basemap(ax, crs=regions.crs)

    fig.savefig(os.path.join(VIS, 'region_by_total_cost.pdf'))


def plot_national_costs(national_costs):
    """

    """
    countries = [
        'NGA',
        'COD',
        'ETH',
        'SDN',
        'ZAF',
        'TZA',
        'EGY',
        'AGO',
        'KEN',
        'DZA',
        'MOZ',
        'ZMB',
        'MLI',
        'TCD',
        'MDG',
        'CMR',
        'MAR',
        'SSD',
        'UGA',
    ]

    national_costs = national_costs[national_costs['Country'].isin(countries)]
    plot = sns.FacetGrid(
        national_costs, row="Strategy", col="Scenario", sharex=False,
        row_order=['4G(MW)', '4G(FB)', '3G(MW)', '3G(FB)'],
        col_order=['Low', 'Baseline', 'High'])
    plot.map(sns.barplot, 'Country', "Cost ($Bn)", order=countries)
    plot.set_xticklabels(rotation=90)
    plot.set(xlabel=None)
    plt.tight_layout()
    plot.savefig(os.path.join(VIS, 'national_cost_estimates.png'), dpi=300)


def plot_total_costs(total_costs):
    """

    """
    plot = sns.FacetGrid(
        total_costs, col="Scenario", height=4, aspect=.5,
        col_order=['Low', 'Baseline', 'High'])
    plot.map(sns.barplot, "Strategy", "Cost ($Bn)")
    plot.set_xticklabels(rotation=30)
    plot.set(xlabel=None)
    plt.tight_layout()
    plot.savefig(os.path.join(VIS, 'total_cost_estimates.png'), dpi=300)


if __name__ == '__main__':

    print('Loading median cost by pop density geotype')
    path = os.path.join(DATA_INTERMEDIATE, 'median_per_user_cost_by_pop_density.csv')
    data = pd.read_csv(path)

    print('Plotting using numerically labelled geotypes')
    plot_median_per_user_cost(data)

    print('Loading regional data by pop density geotype')
    path = os.path.join(DATA_INTERMEDIATE, 'all_regional_data.csv')
    data = pd.read_csv(path)

    print('Loading shapes')
    path = os.path.join(DATA_INTERMEDIATE, 'all_regional_shapes.shp')
    if not os.path.exists(path):
        shapes = get_regional_shapes()
        shapes.to_file(path)
    else:
        shapes = gpd.read_file(path, crs='epsg:4326')

    print('Plotting regions by geotype')
    plot_regions_by_geotype(data, shapes)

    print('Loading regional results data')
    path = os.path.join(BASE_PATH, '..', 'results', 'regional_cost_estimates.csv')
    regional_costs = pd.read_csv(path)

    print('Plotting regions by geotype')
    plot_regions_by_cost(regional_costs, shapes)

    print('Loading national results data')
    path = os.path.join(BASE_PATH, '..', 'results', 'national_cost_estimates.csv')
    national_costs = pd.read_csv(path)

    print('Plotting cost estimates')
    plot_national_costs(national_costs)

    print('Loading total results data')
    path = os.path.join(BASE_PATH, '..', 'results', 'total_cost_estimates.csv')
    total_costs = pd.read_csv(path)

    print('Plotting cost estimates')
    plot_total_costs(total_costs)

    print('Complete')
