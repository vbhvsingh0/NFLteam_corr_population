# NFLteam_corr_population

The goal of this project is to find the correlation between the USA Sports teams' wins with respect to the population of the city. 

Note: This project was a part of the Coursera course, "Introduction to Data Science in Python" offered by University of Michigan.

A file of metropolitan regions and associated sports teams was taken from assets/wikipedia_data.html . Each of these regions may have one or more teams from the "Big 4": NFL (football) , MLB (Baseball), NBA (basketball) or NHL (Hockey). For each sport I would like to answer the question: what is the win/loss ratio's correlation with the population of the city it is in? Win/Loss ratio refers to the number of wins over the number of wins plus the number of losses. The data for the win-loss ratio for the four sports are provided as .csv files. To calculate the correlation with pearsonr, two ordered lists of values were involved, the populations from the wikipedia_data.html file and the win/loss ratio for a given sport in the same order. The win/loss ratios for those cities which have multiple teams of a single sport were averaged. 

Note: The analysis was done only for the data after the year 2018.

Correlations were calculated separately for each of the 4 sports. The scripts written to calculate correlations are in the files nhl_corr.py, nba_corr.py, mlb_corr.py, nfl_corr.py for NHL, NBA, MLB, and NFL respectively.

Observation: Interestingly, the NBA, NFL, and MLB showed a positive correlation, but the NHL had a negative correlation. 