#Reading NFL data and cleaning it
nfl= pd.read_csv('assets/nfl.csv')
nfl=nfl[nfl['year']==2018]
nfl=nfl[['team','L','W','W-L%']]
nfl['team']=nfl['team'].apply(lambda x: x.replace('*','').replace('+',''))
nfl.drop([0,5,10,15,20,25,30,35],inplace=True)
    
#Renaming the teams in NFL data above to just teams suffixes
nfl_teams = {}
for team in nfl['team']:
     nfl_teams[team]=team.split()[-1]
nfl=nfl.set_index('team')
nfl=nfl.rename(index=nfl_teams)
    
#Reading wiki file and cleaning it
wiki=pd.read_html('assets/wikipedia_data.html')
wiki=wiki[1]
wiki=wiki[['Metropolitan area','Country','Population (2016 est.)[8]', 'NFL']].rename(columns={'Population (2016 est.)[8]':'Population'})
wiki['NFL']=wiki['NFL'].str.replace('\[.*\]','')
    
#Splitting wiki rows based on the teams listed in NFL column
wiki["NFL"]=wiki["NFL"].str.split("\s")
wiki=wiki.explode('NFL').reset_index(drop=True)
    
#Merging both the data based on teams and then converting W-L% and populations to float
merged_nfl=nfl.merge(wiki,right_on='NFL',left_index=True,how='inner')
merged_nfl['W-L%']=merged_nfl['W-L%'].astype(float)
merged_nfl['Population']=merged_nfl['Population'].astype(float)
    
#getting the population and mean of W-L% using groupby
merged_nfl=merged_nfl.groupby('Metropolitan area').mean()
    
population_by_region = list(merged_nfl['Population']) # pass in metropolitan area population from cities
win_loss_by_region = list(merged_nfl['W-L%']) # pass in win/loss ratio from nfl_df in the same order as cities["Metropolitan area"]

# Correlation
a,b = stats.pearsonr(population_by_region, win_loss_by_region)
return a