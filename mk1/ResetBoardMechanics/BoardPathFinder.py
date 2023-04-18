import heapq


def astar(start, goal, grid):
    """
    Find the shortest path from start to goal in a 2D grid using A* algorithm.
    :param start: tuple representing the starting point (x, y)
    :param goal: tuple representing the goal point (x, y)
    :param grid: 2D list representing the grid where 0 represents a clear path and 1 represents an obstacle
    :return: the path as a list of tuples [(x1, y1), (x2, y2), ...] or None if no path exists
    """

    # Define the heuristic function (Euclidean distance)
    def heuristic(a, b):
        return ((a[0] - b[0])**2 + (a[1] - b[1])**2)**0.5

    # Define the cost function (Euclidean distance)
    def cost(current, neighbor):
        return ((current[0] - neighbor[0])**2 +
                (current[1] - neighbor[1])**2)**0.5

    # Initialize the frontier, visited set, and parent dictionary
    frontier = [(0, start)]
    visited = set()
    parent = {}

    # Define the g and f values for the starting point
    g = {start: 0}
    f = {start: heuristic(start, goal)}

    # Loop until the frontier is empty
    while frontier:
        # Get the current node from the frontier
        current_cost, current_node = heapq.heappop(frontier)

        # Check if the current node is the goal
        if current_node == goal:
            # Reconstruct the path and return it
            path = [current_node]
            while path[-1] != start:
                path.append(parent[path[-1]])
            return path[::-1]

        # Add the current node to the visited set
        # print(f"Current Node: {current_node}")
        visited.add(current_node)

        # Loop through the neighbors of the current node
        for neighbor in [
            (i, j) for i in range(current_node[0] - 1, current_node[0] + 2)
                for j in range(current_node[1] - 1, current_node[1] + 2)
        ]:
            # print(f"Neighbor: {neighbor}")

            # Check if the neighbor is inside the grid and not an obstacle
            if 0 <= neighbor[1] < len(grid) and 0 <= neighbor[0] < len(
                    grid[0]) and grid[neighbor[1]][neighbor[0]] == "":
                # Calculate the new g value for the neighbor
                # print(f"Neighbor: {neighbor}, passed if statement")
                new_g = g[current_node] + cost(current_node, neighbor)

                # Check if the neighbor is already in the visited set and has a lower g value
                if neighbor in visited and new_g >= g.get(
                        neighbor, float('inf')):
                    continue

                # Add the neighbor to the frontier and update its g and f values and parent
                heapq.heappush(frontier,
                               (new_g + heuristic(neighbor, goal), neighbor))
                g[neighbor] = new_g
                f[neighbor] = new_g + heuristic(neighbor, goal)
                parent[neighbor] = current_node

    # No path found
    return None