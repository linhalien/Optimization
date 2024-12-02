import time


def Input():
    [n, k] = [int(x) for x in input().split()]
    distances = []
    for i in range(2 * n + 1):
        row = [int(x) for x in input().split()]
        distances.append(row)
    return n, k, distances


def calculate_distance(route, distances):
    return sum(distances[route[i]][route[i + 1]] for i in range(len(route) - 1))


def greedy_initial_route(n, k, distances):
    route = [0]  # Start (0)
    capacity = 0
    picked = set()
    dropped = set()

    while len(dropped) < n:
        current = route[-1]
        candidates = []

        for i in range(1, n + 1):
            if i not in picked and capacity < k:  # Pickup candidates
                candidates.append((i, distances[current][i]))
            if i in picked and i not in dropped:  # Drop-off candidates
                candidates.append((i + n, distances[current][i + n]))

        if candidates:
            # Select the nearest valid point
            next_point = min(candidates, key=lambda x: x[1])[0]
            route.append(next_point)
            if next_point <= n:  # pickup point
                picked.add(next_point)
                capacity += 1
            else:  # drop-off point
                dropped.add(next_point - n)
                capacity -= 1

    route.append(0)  # Return to 0
    return route


def is_valid_route(route, n, k):
    load = 0
    picked = set()

    for point in route:
        if point <= n:  # Pickup
            load += 1
            picked.add(point)
        else:  # Drop-off
            if (point - n) not in picked:
                return False
            load -= 1
        if load > k:
            return False
    return True


def local_search(n, k, distances, initial_route):
    """Optimize the route using local search (2-opt and relocation)."""
    best_route = initial_route[:]
    best_distance = calculate_distance(initial_route, distances)
    improved = True

    while improved:
        improved = False

        # 2-Opt Swap: Reverse a subsequence
        for i in range(1, len(best_route) - 2):
            for j in range(i + 1, len(best_route) - 1):
                new_route = best_route[:]
                new_route[i : j + 1] = reversed(
                    new_route[i : j + 1]
                )  # Reverse the subsequence

                if is_valid_route(new_route, n, k):
                    new_distance = calculate_distance(new_route, distances)
                    if new_distance < best_distance:
                        best_route = new_route
                        best_distance = new_distance
                        improved = True
        """
        # Relocation: Move a single node
        for i in range(1, len(best_route) - 1):
            for j in range(1, len(best_route) - 1):
                if i != j:
                    new_route = best_route[:]
                    node = new_route.pop(i)  # Remove node at position i
                    new_route.insert(j, node)  # Insert it at position j

                    if is_valid_route(new_route, n, k):
                        new_distance = calculate_distance(new_route, distances)
                        if new_distance < best_distance:
                            best_route = new_route
                            best_distance = new_distance
                            improved = True
        """

    return best_route, best_distance


if __name__ == "__main__":
    n, k, distances = Input()
    start = time.time()

    initial_route = greedy_initial_route(n, k, distances)
    #  local search
    optimized_route, optimized_distance = local_search(n, k, distances, initial_route)

    # Output the results
    print(n)
    print(*optimized_route[1:-1])
    print(optimized_distance)

    end = time.time()
    print(f"Execution Time: {end - start:.2f} seconds")