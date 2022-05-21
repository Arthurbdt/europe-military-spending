import pandas as pd
import numpy as np

# establish list of countries to be included in the analysis
country_list = ['Albania', 'Austria', 'Belarus', 'Belgium', 
    'Bosnia and Herzegovina', 'Bulgaria', 'Croatia', 'Cyprus',
    'Czechia', 'Denmark', 'Estonia', 'Finland', 'France', 'Germany',
    'Greece', 'Hungary', 'Ireland', 'Italy', 'Kosovo', 'Latvia'
    'Lithuania', 'Luxembourg', 'Malta', 'Moldova', 'Montenegro',
    'Netherlands', 'North Macedonia', 'Norway',  'Poland', 'Portugal',
    'Romania', 'Russia', 'Serbia', 'Slovakia', 'Slovenia', 'Spain',
    'Sweden', 'Switzerland', 'Ukraine', 'United Kingdom']

# load raw data
data = pd.read_csv('share_of_gdp.csv')

# pivot yera columns into rows
data = data.melt(
    id_vars = ['Area', 'Country'],
    var_name = 'Year',
    value_name = 'Pct_gdp')

dict_replace = {'xxx': np.nan, '...': np.nan}

data = data.replace(dict_replace)
data = data[data['Country'].isin(country_list)].reset_index(drop=True)

data.to_csv('clean_data.csv')




