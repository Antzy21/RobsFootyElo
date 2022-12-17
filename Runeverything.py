from helpers.csvHelpers import *
from helpers.classes import *
from helpers.manipulateData import *
from generateCsvs import runallcsvs
from Evaluation import logscore
from calculateAdjustmentValues import calculateadjustment

startingElo = 1000
print("Starting Elo:", startingElo)

kWeight = 32
print("Weight K:", kWeight)

csvDicts = readCsvs()
seasons, teams = runCalculations(csvDicts, startingElo, kWeight)

runallcsvs(seasons,teams)

logscore(seasons,kWeight)

calculateadjustment(seasons)
