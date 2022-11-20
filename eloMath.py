import math

# This is a function for caculating new elo scores based on current elo and the match result
# This can be modified to allow for a "thrashing" boost to the elo score changes, based on whatever model we would like to try!
# Inputs are t1, t2 (elo scores), match result (goals), K value
# Outputs the two new elo scores respectively.
def eloCalculation(
    t1,
    t2,
    result : tuple[int, int],
    weightK = 32
    ):
    
    # Step 1
    T1 = 10 ** (t1/400)
    T2 = 10 ** (t2/400)
    # Step 2
    E1 = T1/(T1+T2)
    E2 = T1/(T1+T2)
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


def eloPrediction(
    homeElo,
    awayElo,
    powerBase = math.e,
    homeAdvantage = 0.169,
    footballSeasonalAdjustment = 0.252
    ):
    
    eloDif = homeElo - awayElo
    H = 1 - (1/(1+powerBase**(eloDif/400+homeAdvantage-footballSeasonalAdjustment)))
    A = (1/(1+powerBase**(eloDif/400+homeAdvantage+footballSeasonalAdjustment)))
    D = 1 - (H + A)
    
    return (H, D, A)
