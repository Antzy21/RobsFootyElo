from datetime import datetime
import time
import helpers.eloMath
from helpers.csvHelpers import *
from helpers.classes import *
from helpers.manipulateData import *

def runallcsvs(seasons,teams):
    constructDateCsv("EloRatings", eloByDate(seasons), teams)
    constructDateCsv("Probabilities", winProbabilityByDate(seasons, teams), teams)
    constructGameCsv("EloRatingsByGame", eloByMatchWeek(seasons), teams)
    constructGameCsv("ProbabilitiesByGame", winProbByMatchWeek(seasons), teams)
    constructGameCsv("LogEvalByGame", logEvalByMatchWeek([seasons[-1]], teams), teams)
    constructGameCsv("GoalDifByGame", goalDifByMatchWeek([seasons[-1]], teams), teams)
    constructBetCsv("BettingResult", seasons)
    constructkellybetcsv("kellyBettingResult", seasons)
