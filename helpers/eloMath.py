import math

# This is a function for caculating new elo scores based on current elo and the match result
# This can be modified to allow for a "thrashing" boost to the elo score changes, based on whatever model we would like to try!
# Inputs are t1, t2 (elo scores), match result (goals), K value
# Outputs the two new elo scores respectively.
def eloCalculation(
    t1,
    t2,
    result : tuple[int, int],
    weightK = 20
    ):
    
    # Step 1
    T1 = 10 ** (t1/400)
    T2 = 10 ** (t2/400)
    # Step 2
    E1 = T1/(T1+T2)
    E2 = T2/(T1+T2)
    # Step 3
    if result[0] > result[1]:
        # if team1 wins (scores more goals)
        S1 = 1
        S2 = 0
    elif result[0] < result[1]:
        # if team2 wins (scores more goals)
        S1 = 0
        S2 = 1
    elif result[0] == result[1]:
        # if draw (scores same amount of goals)
        S1 = 1/2
        S2 = 1/2
    # Step 4
    t1_ = round(t1 + weightK * (S1 - E1))
    t2_ = round(t2 + weightK * (S2 - E2))
    
    return(t1_, t2_)

def eloCalculationWithGoalDif(
    t1,
    t2,
    result : tuple[int, int],
    weightK = 20,
    weightGd = 20,
    ):

    t1, t2 = eloCalculation(t1, t2, result, weightK)

    # Step 1
    E1 = (T1-T2)/weightGd
    E2 = (T2-T1)/weightGd
    # Step 2
    S1 = result[0]-result[1]
    S2 = result[1]-result[0]
    # Step 4
    t1_ = round(t1 + weightGd * (S1 - E1))
    t2_ = round(t2 + weightGd * (S2 - E2))
    
    return(t1_, t2_)


def eloPrediction(
    homeElo,
    awayElo,
    powerBase = math.e,
    homeAdvantage = 0.33,
    drawAdjustment = 0.504
    ):
    
    eloDif = homeElo - awayElo
    H = 1 - (1/(1+powerBase**(eloDif/400+homeAdvantage-drawAdjustment)))
    A = (1/(1+powerBase**(eloDif/400+homeAdvantage+drawAdjustment)))
    D = 1 - (H + A)
    
    return (H, D, A)

def logEvaluationValue(homeElo, awayElo, matchResult: tuple[int, int]) -> int:
    (H, D, A) = eloPrediction(homeElo, awayElo)
    if matchResult[0] > matchResult[1]:
        return math.log(H)
    elif matchResult[0] < matchResult[1]:
        return math.log(A)
    elif matchResult[0] == matchResult[1]:
        return math.log(D)