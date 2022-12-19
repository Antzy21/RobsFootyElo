from helpers.csvHelpers import readCsvs, parseSeasonsAndTeams
from generateCsvs import runallcsvs
from Evaluation import logscore
from calculateAdjustmentValues import calculateadjustment

startingElo = 1000
print("Starting Elo:", startingElo)

kWeight = 32
print("Weight K:", kWeight)

csvDicts = readCsvs()
seasons, teams = parseSeasonsAndTeams(csvDicts)

lowestElo = startingElo
for season in seasons:
    season.run(startingElo=lowestElo)
    eloList = [teams[team].elo for team in teams if (teams[team].elo is not None)]
    eloList.sort()
    lowestElo = eloList[0]

runallcsvs(seasons,teams)

logscore(seasons,kWeight)

calculateadjustment(seasons)
