from datetime import datetime
import time
import helpers.eloMath
from helpers.csvHelpers import *
from helpers.classes import *
from helpers.manipulateData import *

def logscore(seasons,kWeight):
    logValues, logTotal = logEvaluationForSeason(seasons[-1])
    print("optimum K:", kWeight, " - Log total: ", logTotal)
    for key in logValues:
        print(f"S~W: {key} - Log: {round(logValues[key], 3)}")

