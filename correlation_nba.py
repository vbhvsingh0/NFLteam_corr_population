#Reading the teams in NBA and setting them to just team suffixes

nba_df= pd.read_csv('assets/nba.csv')
nba_df=nba_df[nba_df['year']==2018]
nba_df=nba_df[['team','W','L','W/L%']]
nba_df['team']=nba_df['team'].str.replace('\*.*','',regex=True).replace('\s\(.*','',regex=True)
nba_df[['W','L','W/L%']]=nba_df[['W','L','W/L%']].astype(float)
nba_df=nba_df.rename(columns={'W/L%':'W-L%'})
    
#Reading wiki file and cleaning it

cities=pd.read_html("assets/wikipedia_data.html")[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]
cities=cities[['Metropolitan area','Population (2016 est.)[8]', 'NBA']].rename(columns={'Population (2016 est.)[8]':'Population'})
cities['NBA']=cities['NBA'].str.replace('\[.*\]','')
cities['Population']=cities['Population'].astype(float)

#Splitting wiki rows based on the teams listed in NBA column
    
nba_teams = {}
for team in nba_df['team']:
     nba_teams[team]=team.split()[-1]
nba_df=nba_df.set_index('team')
nba_df=nba_df.rename(index=nba_teams)
    
cities["NBA"]=cities["NBA"].str.split("\s")
cities=cities.explode('NBA').reset_index(drop=True)

#Merging both the data based on teams and then converting W-L% and populations to float
        
merged_nba=nba_df.merge(cities,right_on='NBA',left_index=True,how='inner')
merged_nba=merged_nba.groupby('Metropolitan area').mean()

#getting the population and mean of W-L% using groupby
    
population_by_region = list(merged_nba['Population']) # pass in metropolitan area population from cities
win_loss_by_region = list(merged_nba['W-L%']) # pass in win/loss ratio from nba_df in the same order as cities["Metropolitan area"]

# Correlation

a,b = stats.pearsonr(population_by_region, win_loss_by_region)