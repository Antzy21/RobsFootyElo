from helpers.eloMath import *

class Team:
    def __init__(self, name) -> None:
        self.name = name
        self.elo = None
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
    def placeBet(self, H, D, A, score: tuple[int, int], size = 1):
        if score[0] > score[1]:
            self.result = self.homeBet * H
        elif score[0] < score[1]:
            self.result = self.awayBet * A
        elif score[0] == score[1]:
            self.result = self.drawBet * D

class Game:
    def __init__(self, season, date, home, away, score, bet) -> None:
        self.season = season
        self.date = date
        self.home : Team = home
        self.away : Team = away
        self.score : tuple[int, int] = score
        self.bet : Bet = bet
        self.homeEloBefore = None
        self.homeEloAfter = None
        self.awayEloBefore = None
        self.awayEloAfter = None
    def playMatch(self, K = 20):
        self.homeEloBefore = self.home.elo
        self.awayEloBefore = self.away.elo
        k = 20
        try:
           if self.home.matchesPlayed[self.season] < 5:
               k = K
        except:
           k = K
        H, D, A = eloPrediction(self.home.elo, self.away.elo)
        self.homeWinProb = H
        self.drawProb = D
        self.awayWinProb = A
        self.bet.placeBet(H, D, A, self.score)
        homeNew, awayNew = eloCalculation(self.home.elo, self.away.elo, self.score, k)
        self.home.updateElo(homeNew, self.season)
        self.away.updateElo(awayNew, self.season)
        self.homeEloAfter = homeNew
        self.awayEloAfter = awayNew
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
