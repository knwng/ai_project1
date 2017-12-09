import numpy as np
from queue import PriorityQueue


class Agent(object):

    def __init__(self, puzzle_map, cat_init, mouse_init):
        self.puzzle_map = puzzle_map
        self.cat_init = cat_init
        self.mouse_init = mouse_init
        return

    class NextNode(object):
        def __init__(self, node, g):
            self.node = node
            self.g = g
            h = abs(node[0] - self.mouse_init[0]) + abs(node[1] - self.mouse_init[1])
            self.priority = h + g
            return

        def __lt__(self, other):
            return self.priority < other.priority

    def solver(self):
        orient = np.array([[0, 1], [1, 0], [0, -1], [-1, 0]])
        open_list = PriorityQueue()
        close_list = []
        path = []
        open_list.put(self.NextNode(self.cat_init, 1))
        parents = {}

        while open_list.not_empty:
            node = open_list.get()
            if self.puzzle_map[node.node[0], node.node[1]] == -1:
                print("catch the mouse!")
                node_backtrack = node.node
                path.append(node_backtrack)
                while str(node_backtrack) in parents:
                    path.append(parents[str(node_backtrack)])
                    node_backtrack = parents[str(node_backtrack)]
                break
            close_list.append(str(node.node))
            for i in range(4):
                nnode = node.node + orient[i]
                if self.is_legal(nnode, close_list):
                    open_list.put(self.NextNode(nnode, node.g + 1))
                    parents[str(nnode)] = node.node
        print("Path: ")
        path.reverse()
        for i in path:
            print(i)

    def is_legal(self, node, close_list):
        M, N = self.puzzle_map.shape
        if node[0] < 0 or node[1] < 0 or node[0] >= M or node[1] >= N:
            return False
        if self.puzzle_map[node[0], node[1]] == 1:
            return False
        if str(node) in close_list:
            return False
        return True


class PuzzleMap(object):
    def __init__(self, M=6, N=7, cat_init=[1, 3], mouse_init=[5, 2], grid='square', level=1):
        self.M = M
        self.N = N
        self.puzzle_map = np.zeros((self.M, self.N), dtype=np.int)
        self.cat_init = cat_init
        self.mouse_init = mouse_init
        self.grid = grid
        self.level = level
        self.obstacle = [[1, 4], [3, 1], [3, 2], [3, 3], [3, 4]]
        return

    def map_generator(self):
        self.puzzle_map[self.cat_init[0], self.cat_init[1]] = 2
        self.puzzle_map[self.mouse_init[0], self.mouse_init[1]] = -1
        self.obstacle_generator()

        return

    def obstacle_generator(self):
        for i in self.obstacle:
            self.puzzle_map[i] = 1

        return
