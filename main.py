from graph import Graph


def main():
    graph = Graph("map.txt")
    x, y = graph.find_starting_point()
    graph.print_graph()
    print()
    print("Starting point: ", x, y)

    graph.dijkstra()


if __name__ == "__main__":
    main()
