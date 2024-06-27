import heapq


class Graph:
    def __init__(self, input_list):
        self.graph = {}
        self.heuristic = {}
        self.input_list = input_list

    def create_heuristics(self):
        for i in self.input_list:
            self.heuristic[i[0]] = int(i[1])
        return self.heuristic

    def create_edges(self):
        for sub_list in self.input_list:
            self.graph[sub_list[0]] = {}
            for j in range(2, len(sub_list), 2):
                self.graph[sub_list[0]][sub_list[j]] = int(sub_list[j + 1])
        return self.graph


class AStarAlgo:
    def __init__(self, heuristics, adjacency_list, source, destination):
        self.heuristics = heuristics
        self.adjacency_list = adjacency_list
        self.source = source
        self.destination = destination
        self.parent = {key: None for key in self.heuristics}
        self.visited = {key: False for key in self.heuristics}
        self.frontier = []
        self.act_distance = {key: float("inf") for key in self.heuristics}
        self.act_distance[self.source] = 0
        self.path = []
        self.total_distance = 0
        self.path_found = False

    def search(self):
        heapq.heappush(self.frontier, (self.h_n(self.source), self.source))
        while self.frontier:
            _, current_node = heapq.heappop(self.frontier)

            if self.goal_test(current_node):  # Check if the goal has been reached
                self.total_distance = self.act_distance[self.destination]
                self.path = self.reconstruct_path()
                self.path_found = True
                return

            self.visited[current_node] = True
            for neighbor, distance in self.adjacency_list[current_node].items():
                if not self.visited[neighbor]:
                    new_distance = self.act_distance[current_node] + distance
                    if new_distance < self.act_distance[neighbor]:
                        self.act_distance[neighbor] = new_distance
                        self.parent[neighbor] = current_node
                        heapq.heappush(self.frontier, (new_distance + self.h_n(neighbor), neighbor))

    def h_n(self, area):
        return self.heuristics[area]

    def goal_test(self, current_node):
        return current_node == self.destination

    def reconstruct_path(self):
        path, current_node = [], self.destination
        while current_node is not None and current_node in self.parent:
            path.append(current_node)
            current_node = self.parent[current_node]
        path.reverse()
        return path

    def __repr__(self):
        self.search()
        if self.path_found:
            return f"Path: {' -> '.join(self.path)}\nTotal distance: {self.total_distance} km"
        else:
            return "NO PATH FOUND"


with open("22101667_Sakib_Rayhan_Yeasin_CSE422_07_Lab_Assignment01_InputFile_Spring2024.txt", "r") as input_file, open("output_file", "w") as output_file:
    graph_list = []
    for i in input_file.readlines():
        graph_list.append(i.split())
    graph_instance = Graph(graph_list)
    heuristics = graph_instance.create_heuristics()
    adjacency_list = graph_instance.create_edges()

    source = input("Start node: ")
    if source not in adjacency_list:
        print("NO PATH FOUND", file=output_file)
    else:
        destination = "Bucharest"
        implement_Astar = AStarAlgo(heuristics, adjacency_list, source, destination)
        print(implement_Astar, file=output_file)
