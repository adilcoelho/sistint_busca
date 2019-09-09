from elements import Elements
from direction import Direction
from vertex import Vertex


class Graph:
    file_lines = []
    x_size = 0
    y_size = 0
    vertices = {}
    agent_position = None
    agent_direction = None

    def __init__(self, file_name):
        map_file = open(file_name, 'r')

        # Read x dimension of map
        line = map_file.readline()
        self.x_size = int(line)

        # Read y dimension of map
        line = map_file.readline()
        self.y_size = int(line)

        # Get the lines in file
        self.file_lines = map_file.readlines()

        map_file.close()

    def dijkstra(self):
        print("Beginning Dijkstra's algorithm")

    def add_vertex(self, x, y, direction):
        new_vertex = Vertex(x, y, direction)
        self.vertices[(x, y)] = new_vertex
        return new_vertex

    def find_starting_point(self):
        for y in range(0, self.y_size):
            for x in range(0, self.x_size):
                if self.file_lines[y][x] == '>':
                    self.add_vertex(x, y, Direction.E)
                    self.agent_position = (x, y)
                    self.agent_direction = Direction.E
                    return x, y

        raise Exception("Starting point not found")

    def print_graph(self):
        self.print_first_line()
        self.print_line_separator()

        # Print rest of map
        for i in range(0, self.y_size):
            # Print line information
            print()
            if i < 10:
                print(" " + str(i) + " |", end='')
            else:
                print(str(i) + " |", end='')

            for j in range(0, self.x_size):
                self.print_line(i, j)

            self.print_line_separator()

    def print_line_separator(self):
        print()
        print("   +", end='')
        for j in range(0, self.x_size):
            print("---+", end='')

    def print_first_line(self):
        print("    ", end='')
        for i in range(0, self.x_size):
            if i < 10:
                print(" " + str(i) + "  ", end='')
            else:
                print(" " + str(i) + " ", end='')

    def print_line(self, i, j):
        current_line = " "
        if (j, i) == self.agent_position:
            current_line += str(self.agent_direction.value)
        else:
            current_line += " "
        current_line += " |"
        print(current_line, end='')
