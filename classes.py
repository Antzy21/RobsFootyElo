from eloMath import eloCalculation

class Team:
    def __init__(self, name) -> None:
        self.name = name
        self.elo = None
        self.matchesPlayed = 0
    def updateElo(self, elo):
        self.elo = elo
        self.matchesPlayed += 1

class Game:
    def __init__(self, season, date, home, away, score) -> None:
        self.season = season
        self.date = date
        self.home : Team = home
        self.away : Team = away
        self.score : tuple[int, int] = score
        self.homeEloBefore = None
        self.homeEloAfter = None
        self.awayEloBefore = None
        self.awayEloAfter = None
    def playMatch(self):
        self.homeEloBefore = self.home.elo
        self.awayEloBefore = self.away.elo
        homeNew, awayNew = eloCalculation(self.home.elo, self.away.elo, self.score)
        self.home.updateElo(homeNew)
        self.away.updateElo(awayNew)
        self.homeEloAfter = homeNew
        self.awayEloAfter = awayNew

class Season:
    def __init__(self, name) -> None:
        self.name = name
        self.games : list[Game] = []
    def addGame(self, game: Game):
        self.games.append(game)
