def kellyformula(bet: int, prob: int) -> int:
    if bet == 1:
        return(1)
    result = ((bet*prob)-1)/(bet-1)
    return(result)

print(kellyformula(49/20,0.38))
