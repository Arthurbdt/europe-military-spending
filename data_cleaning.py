''' Clean, prepare and merge all 3 datasets into one for visualization '''
import pandas as pd
import numpy as np

# establish list of countries to be included in the analysis
country_list = ['Albania', 'Austria', 'Belarus', 'Belgium', 
    'Bosnia and Herzegovina', 'Bulgaria', 'Croatia', 'Cyprus',
    'Czechia', 'Denmark', 'Estonia', 'Finland', 'France', 'Germany',
    'Greece', 'Hungary', 'Ireland', 'Italy', 'Kosovo', 'Latvia',
    'Lithuania', 'Luxembourg', 'Malta', 'Moldova', 'Montenegro',
    'Netherlands', 'North Macedonia', 'Norway',  'Poland', 'Portugal',
    'Romania', 'Russia', 'Serbia', 'Slovakia', 'Slovenia', 'Spain',
    'Sweden', 'Switzerland', 'Ukraine', 'United Kingdom', 'Iceland']
    
# record names of variables, datasets and labels
path = '.\\datasets\\'
measures = ['Percent_gdp', 'constant_usd', 'usd_per_capita']
files = ['share_of_gdp.csv', 'constant_usd.csv', 'usd_per_capita.csv']
replacements = {'xxx': np.nan, '...': np.nan}

def clean_dataframe(file_name, measure_name):
    '''
    Applies cleaning rules to input dataset
    '''
    data = pd.read_csv(path + file_name)
    # pivot year columns into rows
    data = data.melt(    
        id_vars = ['Area', 'Country'],
        var_name = 'Year',
        value_name = measure_name)
    # apply cleaning rules to columns
    data = data.replace(replacements) # replace special characters
    data = data[data['Country'].isin(country_list)].reset_index(drop=True) # restrict list of countries
    # convert percentage string into float
    if measure_name == 'Percent_gdp':
        data[measure_name] = data[measure_name].str.rstrip("%").astype(float)
    # convert millions into billions
    elif measure_name == 'constant_usd':
        data[measure_name] = data[measure_name].astype(float) / 1000.
    # convert data to numeric
    elif measure_name == 'usd_per_capita':
        data[measure_name] = data[measure_name].astype(float)
    return data

# clean and merge datasets
df = pd.DataFrame()
for file, measure in zip(files, measures):
    dataset = clean_dataframe(file, measure)
    if df.empty:
        df = dataset
    else:
        df = pd.merge(df, dataset[['Country', 'Year', measure]], how = 'left', on = ['Country', 'Year'])

# save final dataset
df.to_csv('.\datasets\clean_data.csv')




