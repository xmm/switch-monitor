from math import sqrt
from timeit import default_timer as timer

from search import Problem, depth_limited_search, \
    breadth_first_tree_search, breadth_first_graph_search, \
    depth_first_graph_search, iterative_deepening_search


def to_coord(idx, n):
    return idx // n, idx % n


def change_elements(idx, n):
    x, y = to_coord(idx, n)
    return tuple(a * n + b for a, b in (
        (x - 1, y),
        (x, y - 1),
        (x, y),
        (x, y + 1),
        (x + 1, y),
    ) if 0 <= a < n and 0 <= b < n)


def build_transform_map(n):
    return tuple(change_elements(action, n) for action in range(n * n))


def toggle(state, elements):
    return bytes(
        v if i not in elements else (0 if state[i] else 1)
        for i, v in enumerate(state)
    )


class MonitorToggleProblem(Problem):
    def __init__(self, initial):
        size = len(initial)
        Problem.__init__(self, initial, goal=bytes((1,) * size))
        self.transform_map = build_transform_map(int(sqrt(size)))
        self._actions = tuple(range(size))

    def actions(self, state):
        return self._actions

    def result(self, state, action):
        return toggle(state, self.transform_map[action])

    def goal_test(self, state):
        return state == self.goal


def get_prettify_state(state):
    return bytes([e + 48 for e in state])


def get_node_list(result_node):
    current = result_node
    while current:
        yield current
        current = current.parent
        if not current:
            raise StopIteration


def pretty_print_node(node, n):
    print(
        node.action and to_coord(node.action, n) or 'start',
        get_prettify_state(node.state),
    )


def run(problem, initial, searcher):
    last_node = searcher(
        problem(initial),
        # 9,
    )
    n = int(sqrt(len(initial)))
    for node in reversed(list(get_node_list(last_node))):
        pretty_print_node(node, n)


def compare_searchers(problem, initial, searchers):
    results = []
    for searcher in searchers:
        start = timer()
        node = searcher(
            problem(initial),
        )
        duration = timer() - start
        results.append((searcher, node, duration))
    for s, node, d in sorted(results, key=lambda e: e[2]):
        print(
            s.__name__,
            len(list(get_node_list(node))),
            d,
            get_prettify_state(node.state),
        )


def main():
    initial_state = bytes((1, 1, 1, 0, 0, 1, 0, 0, 0,))

    searchers = (
        breadth_first_tree_search,
        breadth_first_graph_search,
        depth_first_graph_search,
        iterative_deepening_search,
        depth_limited_search,
    )

    run(MonitorToggleProblem, initial_state, breadth_first_graph_search)

    compare_searchers(
        MonitorToggleProblem,
        initial_state,
        searchers,
    )


if __name__ == '__main__':
    main()
