#Reading MLB data and cleaning it

mlb_df=pd.read_csv("assets/mlb.csv")
cities=pd.read_html("assets/wikipedia_data.html")[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]

#Renaming the teams in MLB data above to just teams suffixes

mlb_df=mlb_df[mlb_df['year']==2018]
mlb_df=mlb_df[['team','W','L','W-L%']]
mlb_df[['W','L','W-L%']]=mlb_df[['W','L','W-L%']].astype(float)
    
#Reading wiki file and cleaning it

cities=cities[['Metropolitan area','Population (2016 est.)[8]', 'MLB']].rename(columns={'Population (2016 est.)[8]':'Population'})
cities['MLB']=cities['MLB'].str.replace('\[.*\]','')
cities['Population']=cities['Population'].astype(float)

#Splitting wiki rows based on the teams listed in MLB column
    
mlb_teams = {}
for team in mlb_df['team']:
if team.split()[-1]=='Sox':
        mlb_teams[team]=team.split()[-2]+' '+team.split()[-1]
else:
        mlb_teams[team]=team.split()[-1]
mlb_df=mlb_df.set_index('team')
mlb_df=mlb_df.rename(index=mlb_teams)

cities["MLB"]=cities["MLB"].str.split("\s")
cities=cities.explode('MLB').reset_index(drop=True)
cities=cities.set_index('MLB')
cities=cities.drop('Sox',axis=0).rename(index={'White':'White Sox','Red':'Red Sox'})

#Merging both the data based on teams and then converting W-L% and populations to float
        
merged_mlb=mlb_df.merge(cities,right_index=True,left_index=True,how='inner')
merged_mlb=merged_mlb.groupby('Metropolitan area').mean()

#getting the population and mean of W-L% using groupby
    
population_by_region = list(merged_mlb['Population']) # pass in metropolitan area population from cities
win_loss_by_region = list(merged_mlb['W-L%']) # pass in win/loss ratio from mlb_df in the same order as cities["Metropolitan area"]

# Correlation

a,b = stats.pearsonr(population_by_region, win_loss_by_region)
return a