from helpers.csvHelpers import readCsvs, parseSeasonsAndTeams
from helpers.manipulateData import getLowestElo
from generateCsvs import runallcsvs
from datetime import datetime
from Evaluation import printLogScore, meanSquaredError
from calculateAdjustmentValues import calculateadjustment
from helpers.eloMath import eloPrediction

startingElo = 1000
print("Starting Elo:", startingElo)

kWeight = 12
print("Weight K:", kWeight)

csvDicts = readCsvs()

def run(k):
    seasons, teams = parseSeasonsAndTeams(csvDicts)
    lowestElo = startingElo
    capital = 10
    for season in seasons:
        capital = season.playMatches(k, defaultElo=lowestElo, capital=capital, betAfterDate=datetime(2005,6,1))
        lowestElo = getLowestElo(teams)
        input(f"Next Season: {season.name}")
    return seasons
for k in range(1,20,2):
    seasons = run(k)
    M = meanSquaredError(seasons)
    print(k, M)


#runallcsvs(seasons,teams)
#printLogScore(seasons)

M = meanSquaredError(seasons)
print(M)

#calculateadjustment(seasons)

h, d, a = eloPrediction(teams["Everton"].elo, teams["Wolves"].elo)
print(h, d, a)
