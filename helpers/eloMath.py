import math

# This is a function for caculating new elo scores based on current elo and the match result
# This can be modified to allow for a "thrashing" boost to the elo score changes, based on whatever model we would like to try!
# Inputs are t1, t2 (elo scores), match result (goals), K value
# Outputs the two new elo scores respectively.
def eloCalculation(
    t1,
    t2,
    homeGoals,
    awayGoals,
    weightK = 32
    ):
    
    # Step 1
    T1 = 10 ** (t1/400)
    T2 = 10 ** (t2/400)
    # Step 2
    E1 = T1/(T1+T2)
    E2 = T2/(T1+T2)
    # Step 3
    if homeGoals > awayGoals:
        # if team1 wins (scores more goals)
        S1 = 1
        S2 = 0
    elif homeGoals < awayGoals:
        # if team2 wins (scores more goals)
        S1 = 0
        S2 = 1
    elif homeGoals == awayGoals:
        # if draw (scores same amount of goals)
        S1 = 1/2
        S2 = 1/2
    # Step 4
    t1_ = round(t1 + weightK * (S1 - E1))
    t2_ = round(t2 + weightK * (S2 - E2))
    
    return(t1_, t2_)

def meanSquaredErrorForGame(game):

    # Step 1
    T1 = 10 ** (game.homeEloBefore/400)
    T2 = 10 ** (game.awayEloBefore/400)
    # Step 2
    expectedHome = T1/(T1+T2)
    expectedAway = T2/(T1+T2)
    # Step 3
    if game.homeGoals > game.awayGoals:
        # if team1 wins (scores more goals)
        observedHome = 1
        observedAway = 0
    elif game.homeGoals < game.awayGoals:
        # if team2 wins (scores more goals)
        observedHome = 0
        observedAway = 1
    elif game.homeGoals == game.awayGoals:
        # if draw (scores same amount of goals)
        observedHome = 1/2
        observedAway = 1/2
    return ((expectedHome-observedHome)**2+(expectedAway-observedAway)**2)

def eloCalculationWithGoalDif(
    t1,
    t2,
    homeGoals,
    awayGoals,
    weightK = 32,
    weightGd = 32,
    ):

    t1_, t2_ = eloCalculation(t1, t2, homeGoals, awayGoals, weightK)

    c = 200

    # Step 1
    E1 = (t1-t2)/c
    E2 = (t2-t1)/c
    # Step 2
    goalDifference = homeGoals-awayGoals

    # Add to exisiting elo changes
    t1_ += round(weightGd * (goalDifference - E1))
    t2_ += round(weightGd * (-goalDifference - E2))
    
    return(t1_, t2_)


def eloPrediction(
    homeElo,
    awayElo,
    powerBase = math.e,
    homeAdvantage = 0.362,
    drawAdjustment = 0.526
    ):
    
    eloDif = homeElo - awayElo
    H = 1 - (1/(1+powerBase**(eloDif/400+homeAdvantage-drawAdjustment)))
    A = (1/(1+powerBase**(eloDif/400+homeAdvantage+drawAdjustment)))
    D = 1 - (H + A)
    
    return (H, D, A)

def logEvaluationValue(homeElo, awayElo, matchResult) -> int:
    (H, D, A) = eloPrediction(homeElo, awayElo)
    if matchResult == "H":
        return math.log(H)
    elif matchResult == "A":
        return math.log(A)
    elif matchResult == "D":
        return math.log(D)