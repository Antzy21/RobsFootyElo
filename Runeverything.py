from helpers.csvHelpers import readCsvs, parseSeasonsAndTeams
from helpers.manipulateData import getLowestElo
from generateCsvs import runallcsvs
from datetime import datetime
from Evaluation import printLogScore
from calculateAdjustmentValues import calculateadjustment
from helpers.eloMath import eloPrediction

startingElo = 1000
print("Starting Elo:", startingElo)

kWeight = 32
print("Weight K:", kWeight)

csvDicts = readCsvs()
seasons, teams = parseSeasonsAndTeams(csvDicts)

lowestElo = startingElo
capital = 10
for season in seasons:
    capital = season.playMatches(kWeight, defaultElo=lowestElo, capital=capital, betAfterDate=datetime(2005,6,1))
    lowestElo = getLowestElo(teams)
    #input(f"Next Season: {season.name}")

#runallcsvs(seasons,teams)

#printLogScore(seasons)

#calculateadjustment(seasons)

h, d, a = eloPrediction(teams["Chelsea"].elo, teams["Chelsea"].elo)
print(h, d, a)
