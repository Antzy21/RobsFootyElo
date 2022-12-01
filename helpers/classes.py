from helpers.eloMath import *

class Team:
    def __init__(self, name, initialElo) -> None:
        self.name: str = name
        self.elo: int = initialElo
        self.matchesPlayed: dict[int, int] = {}
    def updateElo(self, elo, season):
        self.elo = elo
        try:
            self.matchesPlayed[season] += 1
        except:
            self.matchesPlayed[season] = 0

class Bet:
    def __init__(self, home, draw, away):
        self.homeBet = home
        self.drawBet = draw
        self.awayBet = away
    def betResult(self, H, D, A, score: tuple[int, int], size = 1):
        if score[0] > score[1]:
            self.result = self.homeBet * H
        elif score[0] < score[1]:
            self.result = self.awayBet * A
        elif score[0] == score[1]:
            self.result = self.drawBet * D

class Probabilities:
    def __init__(self, home, draw, away):
        self.homeWin = home
        self.draw = draw
        self.awayWin = away

class Game:
    def __init__(self, season, date, home, away, bet) -> None:
        self.season = season
        self.date = date
        self.home : Team = home
        self.away : Team = away
        self.score : tuple[int, int] = None
        self.bet : Bet = bet
        self.probs: Probabilities = None
        self.homeEloBefore = None
        self.homeEloAfter = None
        self.awayEloBefore = None
        self.awayEloAfter = None
    def setElos(self, score, k):
        homeNew, awayNew = eloCalculation(self.home.elo, self.away.elo, score, k)
        self.home.updateElo(homeNew, self.season)
        self.away.updateElo(awayNew, self.season)
        self.homeEloAfter = homeNew
        self.awayEloAfter = awayNew
    def playMatch(self, score, K = 540):
        k = 540
        try:
           if self.home.matchesPlayed[self.season] < 5:
               k = K
        except:
           k = K
        
        self.homeEloBefore = self.home.elo
        self.awayEloBefore = self.away.elo
        
        H, D, A = eloPrediction(self.homeEloBefore, self.homeEloBefore)
        self.probs: Probabilities = Probabilities(H, D, A)
        self.bet.betResult(H, D, A, score)

        self.score = score
        self.setElos(score, k)
        self.week = self.home.matchesPlayed[self.season]

class Season:
    def __init__(self, name, number) -> None:
        self.number = number
        self.name = name
        self.games : list[Game] = []
        self.homeWins = 0
        self.awayWins = 0
        self.draws = 0
    def addGame(self, game: Game):
        self.games.append(game)
        if game.score[0] > game.score[1]:
            self.homeWins += 1
        elif game.score[0] < game.score[1]:
            self.awayWins += 1
        elif game.score[0] == game.score[1]:
            self.draws += 1
