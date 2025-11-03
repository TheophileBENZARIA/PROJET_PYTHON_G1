
class UniteTerm:
    def __init__(self, lettre : str, teams : int, vie : int):
        self.lettre = lettre
        self.teams = teams
        self.vie = vie

    def __str__(self):
        return self.lettre

    def __repr__(self):
        return f"{self.lettre} {self.teams} {self.vie}"

