def kellyformula(bet,prob):
    if bet == 1:
        return(1)
    result = ((bet*prob)-1)/(bet-1)
    return(result)

#print(kellyformula(2.12,0.7551))