from enum import Enum


class Direction(Enum):
    N = '^'
    S = 'v'
    E = '>'
    W = '<'
    NE = '/'
    NW = '#'
    SW = '%'
    SE = '\\'

    def __lt__(self, other):
        return False

    def __le__(self, other):
        return False

    def prev(self):
        if self.name == self.N.name:
            return self.NW
        elif self.name == self.NW.name:
            return self.W
        elif self.name == self.W.name:
            return self.SW
        elif self.name == self.SW.name:
            return self.S
        elif self.name == self.S.name:
            return self.SE
        elif self.name == self.SE.name:
            return self.E
        elif self.name == self.E.name:
            return self.NE
        elif self.name == self.NE.name:
            return self.N
        else:
            raise Exception("Invalid direction")

    def next(self):
        if self.name == self.N.name:
            return self.NE
        elif self.name == self.NE.name:
            return self.E
        elif self.name == self.E.name:
            return self.SE
        elif self.name == self.SE.name:
            return self.S
        elif self.name == self.S.name:
            return self.SW
        elif self.name == self.SW.name:
            return self.W
        elif self.name == self.W.name:
            return self.NW
        elif self.name == self.NW.name:
            return self.N
        else:
            raise Exception("Invalid direction")
