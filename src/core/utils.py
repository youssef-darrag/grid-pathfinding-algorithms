def reconstruct_path(parent, current):
    path = []
    while current is not None:
        path.append(current)
        current = parent[current]

    return path[::-1]
