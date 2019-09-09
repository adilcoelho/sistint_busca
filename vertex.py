import sys
from direction import Direction


class Vertex:
    id = None
    adjacent = {}
    distance = sys.maxsize
    visited = False
    previous = None
    direction = None

    def __init__(self, x, y, direction):
        self.id = (x, y, direction)

    def add_neighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight

    def get_id(self):
        return self.id

    def get_connections(self):
        return self.adjacent.keys()

    def get_weight(self, neighbor):
        return self.adjacent[neighbor]

    def set_distance(self, dist):
        self.distance = dist

    def set_previous(self, prev):
        self.previous = prev

    def set_visited(self):
        self.visited = True
