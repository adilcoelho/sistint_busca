import sys


class Vertex:
    def __init__(self, x, y, direction):
        self.id = (x, y, direction)
        self.adjacent = {}
        self.distance = sys.maxsize
        self.distance_from_start = sys.maxsize
        self.visited = False
        self.previous = None
        self.direction = None

    def add_neighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight

    def get_connections(self):
        return self.adjacent.keys()

    def get_weight(self, neighbor):
        return self.adjacent[neighbor]
