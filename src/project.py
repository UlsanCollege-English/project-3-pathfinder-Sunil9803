from __future__ import annotations

from collections import deque
import heapq
import json
from pathlib import Path


Graph = dict[str, dict[str, int]]


def load_graph(path: str) -> Graph:
    """Load a weighted graph from a JSON file.

    The JSON file must contain a dictionary of dictionaries:

        {
            "A": {"B": 3, "C": 5},
            "B": {"A": 3},
            "C": {"A": 5}
        }

    Requirements:
    - Return the loaded graph.
    - Raise ValueError if the JSON top level is not a dictionary.
    - Raise ValueError if any neighbor list is not a dictionary.
    - Raise ValueError if any weight is not a positive integer.
    - Raise ValueError if any weight is 0 or negative.

    Note:
    This project uses an undirected graph. Your own map should include both
    directions for every edge, such as A -> B and B -> A.
    """

    with open(path, "r", encoding="utf-8") as file:
        graph = json.load(file)

    if not isinstance(graph, dict):
        raise ValueError("Graph must be a dictionary")

    for node, neighbors in graph.items():

        if not isinstance(neighbors, dict):
            raise ValueError("Neighbors must be dictionaries")

        for neighbor, weight in neighbors.items():

            if not isinstance(weight, int):
                raise ValueError("Weights must be integers")

            if weight <= 0:
                raise ValueError("Weights must be positive")

    return graph


def get_neighbors(graph: Graph, node: str) -> dict[str, int]:
    """Return the neighbors and weights for node.

    If node is missing, return an empty dictionary.

    Example:
        graph = {"A": {"B": 4}}
        get_neighbors(graph, "A") -> {"B": 4}
        get_neighbors(graph, "Z") -> {}
    """

    return graph.get(node, {})


def bfs_order(graph: Graph, start: str) -> list[str]:
    """Return nodes in breadth-first traversal order.

    Requirements:
    - If start is missing, return [].
    - Use a queue.
    - Use a visited set.
    - Follow the neighbor order from the dictionary.
    - Ignore weights for BFS traversal.

    Complexity target:
    - Time: O(V + E)
    - Space: O(V)
    """

    if start not in graph:
        return []

    visited = set()
    queue = deque([start])
    order = []

    visited.add(start)

    while queue:

        current = queue.popleft()
        order.append(current)

        for neighbor in graph[current]:

            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return order


def dijkstra_distances(graph: Graph, start: str) -> dict[str, float]:
    """Return shortest distances from start to every reachable node.

    Requirements:
    - Use Dijkstra's algorithm.
    - Use heapq as the priority queue.
    - If start is missing, return {}.
    - Ignore unreachable nodes; they should not appear in the result.
    - All edge weights must be positive integers.
    - Raise ValueError if a zero or negative weight is found.

    Example:
        graph = {
            "A": {"B": 4, "C": 2},
            "B": {"A": 4},
            "C": {"A": 2}
        }

        dijkstra_distances(graph, "A") -> {"A": 0, "B": 4, "C": 2}

    Complexity target:
    - Time: O((V + E) log V)
    - Space: O(V)
    """

    if start not in graph:
        return {}

    for neighbors in graph.values():
        for weight in neighbors.values():

            if weight <= 0:
                raise ValueError("Weights must be positive")

    distances = {start: 0}
    priority_queue = [(0, start)]

    while priority_queue:

        current_distance, current_node = heapq.heappop(priority_queue)

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node].items():

            distance = current_distance + weight

            if neighbor not in distances or distance < distances[neighbor]:

                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances


def shortest_path(graph: Graph, start: str, target: str) -> list[str]:
    """Return the shortest path from start to target.

    Requirements:
    - Use Dijkstra's algorithm with path reconstruction.
    - Return a list of node names in path order.
    - If start or target is missing, return [].
    - If target is unreachable from start, return [].
    - If start == target and start exists, return [start].
    - Raise ValueError if a zero or negative weight is found.

    Example:
        shortest_path(graph, "A", "D") -> ["A", "C", "D"]

    Complexity target:
    - Dijkstra portion: O((V + E) log V)
    - Path reconstruction: O(P), where P is the number of nodes in the path
    """

    if start not in graph or target not in graph:
        return []

    if start == target:
        return [start]

    priority_queue = [(0, start)]
    distances = {start: 0}
    previous = {}

    while priority_queue:

        current_distance, current_node = heapq.heappop(priority_queue)

        if current_node == target:
            break

        for neighbor, weight in graph[current_node].items():

            if weight <= 0:
                raise ValueError("Weights must be positive")

            distance = current_distance + weight

            if neighbor not in distances or distance < distances[neighbor]:

                distances[neighbor] = distance
                previous[neighbor] = current_node

                heapq.heappush(priority_queue, (distance, neighbor))

    if target not in distances:
        return []

    path = []
    current = target

    while current != start:
        path.append(current)
        current = previous[current]

    path.append(start)
    path.reverse()

    return path


def demo() -> None:
    """Print a short demonstration of your project.

    Your demo should:
    1. Load your graph from data/map.json.
    2. Print the number of locations.
    3. Print BFS order from one location.
    4. Print shortest distances from one location.
    5. Print one shortest path.

    This function is not directly graded by the public tests, but it is useful
    for your presentation/demo.
    """

    map_path = Path("data/map.json")

    graph = load_graph(map_path)

    print("Campus Pathfinder Demo")
    print()

    print(f"Locations loaded: {len(graph)}")
    print()

    start = "Main Gate"
    target = "Dormitory"

    print(f"BFS from {start}:")
    print(bfs_order(graph, start))
    print()

    print(f"Shortest distances from {start}:")
    print(dijkstra_distances(graph, start))
    print()

    print(f"Shortest path from {start} to {target}:")
    print(shortest_path(graph, start, target))


if __name__ == "__main__":
    demo()