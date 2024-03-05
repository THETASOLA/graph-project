def is_cyclic(graph):
    def dfs(node, visited, stack):
        visited.add(node)
        stack.add(node)
        for neighbor in graph.get(node, []):
            if neighbor in stack:
                return True
            if neighbor not in visited:
                if dfs(neighbor, visited, stack):
                    return True
        stack.remove(node)
        return False

    visited = set()
    stack = set()
    for node in graph.keys():
        if node not in visited:
            if dfs(node, visited, stack):
                return True
    return False

