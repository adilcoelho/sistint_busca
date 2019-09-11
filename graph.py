from direction import Direction
from vertex import Vertex
import heapq
import time
from math import sqrt


class Graph:
    def __init__(self, file_name):
        self.file_lines = []
        self.x_size = 0
        self.y_size = 0
        self.vertices = {}
        self.agent_position = None
        self.agent_direction = None
        self.ending_point = None

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
        nodes_explored = 0
        self.find_starting_point()
        self.ending_point = self.find_ending_point()

        print("Beginning Dijkstra's algorithm")
        starting_sec = time.time()

        starting_vertex_coordinates = (self.agent_position[0], self.agent_position[0], self.agent_direction)
        starting_vertex = self.vertices[starting_vertex_coordinates]
        starting_vertex.distance = 0

        ending_vertex_coordinates = None
        ending_vertex = None

        self.create_neighboring_vertices()

        path_to_ending_point_found = False

        unvisited_queue = [(self.vertices[vertex_coordinates].distance, vertex_coordinates)
                           for vertex_coordinates in self.vertices.keys()]
        heapq.heapify(unvisited_queue)

        while not path_to_ending_point_found:
            nodes_explored += 1
            current_vertex_coordinates = heapq.heappop(unvisited_queue)
            current_vertex_coordinates = current_vertex_coordinates[1]

            self.move_agent(current_vertex_coordinates)
            self.create_neighboring_vertices()
            current_vertex = self.vertices[current_vertex_coordinates]
            current_vertex.visited = True

            current_vertex_x_y = (current_vertex_coordinates[0], current_vertex_coordinates[1])
            if current_vertex_x_y == self.ending_point:
                path_to_ending_point_found = True
                ending_vertex_coordinates = current_vertex_coordinates
                ending_vertex = current_vertex
                continue

            for next_vertex_coordinates in current_vertex.adjacent.keys():
                next_vertex = self.vertices[next_vertex_coordinates]
                if not next_vertex.visited:
                    new_distance = current_vertex.distance + current_vertex.get_weight(next_vertex_coordinates)
                    if new_distance < next_vertex.distance:
                        next_vertex.distance = new_distance
                        next_vertex.previous = current_vertex_coordinates

            unvisited_queue.clear()
            unvisited_queue = self.get_unvisited_vertices()
            heapq.heapify(unvisited_queue)

        current_vertex_coordinates = ending_vertex_coordinates
        current_vertex = ending_vertex
        path = []
        while current_vertex_coordinates != starting_vertex_coordinates:
            path.append(current_vertex_coordinates)
            current_vertex_coordinates = current_vertex.previous
            current_vertex = self.vertices[current_vertex_coordinates]

        path.append(starting_vertex_coordinates)
        path.reverse()

        ending_sec = time.time()
        print("Dijkstra's algorithm finished")
        print("Total path cost: ", ending_vertex.distance)
        print("Total nodes explored: ", nodes_explored)
        print("Total time taken (s): ", ending_sec - starting_sec)

        return path

    def a_star(self):
        nodes_explored = 0
        self.find_starting_point()
        self.ending_point = self.find_ending_point()

        print("Beginning A* algorithm")
        starting_sec = time.time()

        starting_vertex_coordinates = (self.agent_position[0], self.agent_position[0], self.agent_direction)
        starting_vertex = self.vertices[starting_vertex_coordinates]
        starting_vertex.distance = 0

        ending_vertex_coordinates = None
        ending_vertex = None

        self.create_neighboring_vertices()

        path_to_ending_point_found = False

        unvisited_queue = [(self.vertices[vertex_coordinates].distance
                            + self.get_euclidean_distance(vertex_coordinates, self.ending_point),
                            vertex_coordinates)
                           for vertex_coordinates in self.vertices.keys()]
        heapq.heapify(unvisited_queue)

        while not path_to_ending_point_found:
            nodes_explored += 1
            current_vertex_coordinates = heapq.heappop(unvisited_queue)
            current_vertex_coordinates = current_vertex_coordinates[1]

            self.move_agent(current_vertex_coordinates)
            self.create_neighboring_vertices()
            current_vertex = self.vertices[current_vertex_coordinates]
            current_vertex.visited = True

            current_vertex_x_y = (current_vertex_coordinates[0], current_vertex_coordinates[1])
            if current_vertex_x_y == self.ending_point:
                path_to_ending_point_found = True
                ending_vertex_coordinates = current_vertex_coordinates
                ending_vertex = current_vertex
                continue

            for next_vertex_coordinates in current_vertex.adjacent.keys():
                next_vertex = self.vertices[next_vertex_coordinates]
                if not next_vertex.visited:
                    new_distance = current_vertex.distance + current_vertex.get_weight(next_vertex_coordinates)
                    if new_distance < next_vertex.distance:
                        next_vertex.distance = new_distance
                        next_vertex.previous = current_vertex_coordinates

            unvisited_queue.clear()
            unvisited_queue = self.get_unvisited_vertices_a_star()
            heapq.heapify(unvisited_queue)

        current_vertex_coordinates = ending_vertex_coordinates
        current_vertex = ending_vertex
        path = []
        while current_vertex_coordinates != starting_vertex_coordinates:
            path.append(current_vertex_coordinates)
            current_vertex_coordinates = current_vertex.previous
            current_vertex = self.vertices[current_vertex_coordinates]

        path.append(starting_vertex_coordinates)
        path.reverse()

        ending_sec = time.time()
        print("A* algorithm finished")
        print("Total path cost: ", ending_vertex.distance)
        print("Total nodes explored: ", nodes_explored)
        print("Total time taken (s): ", ending_sec - starting_sec)

        return path

    def add_vertex(self, x, y, direction):
        new_vertex = Vertex(x, y, direction)
        self.vertices[(x, y, direction)] = new_vertex
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

    def find_ending_point(self):
        for y in range(0, self.y_size):
            for x in range(0, self.x_size):
                if self.file_lines[y][x] == 'x':
                    return x, y

        raise Exception("Ending point not found")

    def find_neighboring_vertices(self):
        found_vertices = []
        x = self.agent_position[0]
        y = self.agent_position[1]
        direction = self.agent_direction

        possible_vertex = self.check_movement_in_current_direction(x, y, direction)
        if possible_vertex:
            found_vertices.append(possible_vertex.copy())

        possible_vertex = {
            'x': self.agent_position[0],
            'y': self.agent_position[1],
            'direction': self.agent_direction.prev(),
            'weight': 1
        }
        found_vertices.append(possible_vertex.copy())

        possible_vertex['direction'] = self.agent_direction.next()
        found_vertices.append(possible_vertex.copy())

        return found_vertices

    def get_unvisited_vertices(self):
        unvisited_vertices = []
        for vertex_coordinates in self.vertices.keys():
            vertex = self.vertices[vertex_coordinates]
            if not vertex.visited:
                vertex_tuple = (vertex.distance, vertex_coordinates)
                unvisited_vertices.append(vertex_tuple)

        return unvisited_vertices

    def get_unvisited_vertices_a_star(self):
        unvisited_vertices = []
        for vertex_coordinates in self.vertices.keys():
            vertex = self.vertices[vertex_coordinates]
            if not vertex.visited:
                vertex_tuple = (vertex.distance + self.get_euclidean_distance(vertex_coordinates, self.ending_point),
                                vertex_coordinates)
                unvisited_vertices.append(vertex_tuple)

        return unvisited_vertices

    def get_euclidean_distance(self, source_vertex, destination_vertex):
        x = destination_vertex[0] - source_vertex[0]
        y = destination_vertex[1] - source_vertex[1]
        return sqrt((x ** 2) + (y ** 2))

    def check_movement_in_current_direction(self, x, y, direction):
        vertex = {
            'x': None,
            'y': None,
            'direction': None,
            'weight': 0
        }

        if direction == Direction.N and y - 1 >= 0:
            vertex['x'] = x
            vertex['y'] = y - 1
            vertex['direction'] = Direction.N
            vertex['weight'] = 1
        elif direction == Direction.S and self.agent_position[1] + 1 < self.y_size:
            vertex['x'] = x
            vertex['y'] = y + 1
            vertex['direction'] = Direction.S
            vertex['weight'] = 1
        elif direction == Direction.W and x - 1 >= 0:
            vertex['x'] = x - 1
            vertex['y'] = y
            vertex['direction'] = Direction.W
            vertex['weight'] = 1
        elif direction == Direction.E and x + 1 < self.x_size:
            vertex['x'] = x + 1
            vertex['y'] = y
            vertex['direction'] = Direction.E
            vertex['weight'] = 1
        elif direction == Direction.NW and x - 1 >= 0 and y - 1 >= 0:
            vertex['x'] = x - 1
            vertex['y'] = y - 1
            vertex['direction'] = Direction.NW
            vertex['weight'] = 1.5
        elif direction == Direction.NE and x + 1 < self.x_size and y - 1 >= 0:
            vertex['x'] = x + 1
            vertex['y'] = y - 1
            vertex['direction'] = Direction.NE
            vertex['weight'] = 1.5
        elif direction == Direction.SW and x - 1 >= 0 and y + 1 < self.y_size:
            vertex['x'] = x - 1
            vertex['y'] = y + 1
            vertex['direction'] = Direction.SW
            vertex['weight'] = 1.5
        elif direction == Direction.SE and x + 1 < self.x_size and y + 1 < self.y_size:
            vertex['x'] = x + 1
            vertex['y'] = y + 1
            vertex['direction'] = Direction.SE
            vertex['weight'] = 1.5
        else:
            return False

        if self.file_lines[vertex['y']][vertex['x']] == '*':
            return False

        return vertex

    def create_neighboring_vertices(self):
        found_vertices = self.find_neighboring_vertices()
        current_vertex_coordinates = (self.agent_position[0], self.agent_position[1], self.agent_direction)
        current_vertex = self.vertices[current_vertex_coordinates]

        for vertex in found_vertices:
            vertex_coordinates = (vertex['x'], vertex['y'], vertex['direction'])
            if vertex_coordinates not in self.vertices.keys():
                self.add_vertex(vertex['x'], vertex['y'], vertex['direction'])
            if vertex_coordinates not in current_vertex.get_connections():
                current_vertex.add_neighbor(vertex_coordinates, weight=vertex['weight'])

    def move_agent(self, coordinates):
        x_y = (coordinates[0], coordinates[1])
        direction = coordinates[2]

        self.agent_position = x_y
        self.agent_direction = direction

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
        elif self.file_lines[j][i] == '*':
            current_line += '*'
        elif self.file_lines[i][j] == 'x':
            current_line = ' x'
        else:
            current_line += " "
        current_line += " |"
        print(current_line, end='')
