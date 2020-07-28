from json import JSONEncoder

DEFAULT_FITNESS = 0


class Individual(object):
    def __init__(self, solution, fitness=None):
        self.solution = solution
        self.fitness = fitness if fitness else DEFAULT_FITNESS


class IndividualEncoder(JSONEncoder):
    def default(self, obj):
        return obj.__dict__
