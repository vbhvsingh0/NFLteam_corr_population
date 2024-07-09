import pandas as pd
import numpy as np
import scipy.stats as stats
import re

#Correlation for NHL



nhl_df=pd.read_csv("assets/nhl.csv")
cities=pd.read_html("assets/wikipedia_data.html")[1]

#cleaning and filtering data

cities=cities.iloc[:-1,[0,3,5,6,7,8]]
nhl_df=nhl_df[nhl_df['year']==2018]
nhl_df=nhl_df[['team','W','L']]
nhl_df['team']=nhl_df['team'].apply(lambda x: x.replace('*','').replace('+',''))
nhl_df.drop([0,9,18,26],inplace=True)
nhl_df[['W','L']]=nhl_df[['W','L']].astype(float)

#Calculating win-loss ratio
nhl_df['W-L%'] = nhl_df['W'].div(nhl_df['W']+nhl_df['L'])

#cleaning cities dataframe    
cities=cities[['Metropolitan area','Population (2016 est.)[8]', 'NHL']].rename(columns={'Population (2016 est.)[8]':'Population'})
cities['NHL']=cities['NHL'].str.replace('\[.*\]','')
cities['Population']=cities['Population'].astype(float)
    
nhl_teams = {}

# let's define team names with their last name

for team in nhl_df['team']:
    nhl_teams[team]=team.split()[-1]
nhl_df=nhl_df.set_index('team')
nhl_df=nhl_df.rename(index=nhl_teams)

# Separating the teams from the same city into two rows
    
cities["NHL"]=cities["NHL"].str.split("\s")
cities=cities.explode('NHL').reset_index(drop=True)

# Merging cities and NHL dataframes
    
merged_nhl=nhl_df.merge(cities,right_on='NHL',left_index=True,how='inner')

# Taking the mean W-L % for the teams from the same city

merged_nhl=merged_nhl.groupby('Metropolitan area').mean()
    
    
population_by_region = list(merged_nhl['Population']) # pass in metropolitan area population from cities
win_loss_by_region = list(merged_nhl['W-L%']) # pass in win/loss ratio from nhl_df in the same order as cities["Metropolitan area"]

# Finally calculating the correlation
    
a,b = stats.pearsonr(population_by_region, win_loss_by_region)