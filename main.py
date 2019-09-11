from graph import Graph


def main():
    dijkstra_graph = Graph("map.txt")
    dijkstra_path = dijkstra_graph.dijkstra()

    print()

    a_star_graph = Graph("map.txt")
    a_star_path = a_star_graph.a_star()

    print()
    print("Select 1 to see the Dijkstra's Algorithm path")
    print("Select 2 to see the A* Algorithm path")
    user_input = input("Selection: ")

    while user_input not in ('0', '1', '2'):
        user_input = input("Please select 0, 1 or 2: ")

    if user_input == '0':
        return
    else:
        graph = None
        path = []
        if user_input == '1':
            graph = dijkstra_graph
            path = dijkstra_path
        elif user_input == '2':
            graph = a_star_graph
            path = a_star_path

        i = 0
        current_vertex = path[i]
        graph.agent_position = (current_vertex[0], current_vertex[1])
        graph.agent_direction = current_vertex[2]

        user_input = ''
        while user_input != 'q':
            print(chr(27) + "[2J")
            print("Press ENTER to move forward, 'b' to move backwards and 'q' to quit")
            graph.print_graph()
            print()
            user_input = input()

            if user_input == '' and i < len(path) - 1:
                i += 1
            elif user_input == 'b' and i > 0:
                i -= 1
            elif user_input == 'q':
                return

            current_vertex = path[i]
            graph.agent_position = (current_vertex[0], current_vertex[1])
            graph.agent_direction = current_vertex[2]


if __name__ == "__main__":
    main()
