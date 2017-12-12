import numpy as np
from Queue import PriorityQueue
import pygame
import time
from config import *
import random

FPS = 30


class Agent(object):

    def __init__(self, puzzle_map):
        self.pmap = puzzle_map
        self.puzzle_map = puzzle_map.puzzle_map
        self.cat_init = puzzle_map.cat_init
        self.mouse_init = puzzle_map.mouse_init
        self.SOLVED = False
        self.open_list = None
        self.close_list = None
        self.path = None
        self.last_node = None
        return

    class NextNode:
        def __init__(self, node, g, mouse_init):
            self.node = node
            self.g = g
            h = abs(node[0] - mouse_init[0]) + abs(node[1] - mouse_init[1])
            self.priority = h + g
            return

        def __cmp__(self, other):
            return cmp(self.priority, other.priority)

    def solver(self, screen, block_lt_pos, block_shape):
        orient = [[0, 1], [1, 0], [0, -1], [-1, 0]]
        self.open_list = PriorityQueue()
        self.close_list = {}
        self.last_node = []
        self.path = []
        self.open_list.put(self.NextNode(self.cat_init, 0, self.mouse_init))
        parents = {}
        # print('puzzle map: ')
        print(self.puzzle_map)

        while self.open_list.not_empty:
            pygame.event.pump()
            node = self.open_list.get()
            if str(node.node) in self.close_list:
                continue
            self.last_node = node.node
            self.display(screen, block_lt_pos, block_shape)
            if self.puzzle_map[node.node[0], node.node[1]] == -1:
                print("catch the mouse!")
                node_backtrack = node.node
                self.path.append(node_backtrack)
                while str(node_backtrack) in parents:
                    self.path.append(parents[str(node_backtrack)])
                    node_backtrack = parents[str(node_backtrack)]
                self.path.reverse()
                self.SOLVED = True
                self.display(screen, block_lt_pos, block_shape)
                break
            self.close_list[str(node.node)] = node.node
            for i in range(4):
                nnode = [sum(x) for x in zip(node.node, orient[i])]
                if self.is_legal(nnode, self.close_list):
                    self.open_list.put(self.NextNode(nnode, node.g + 1, self.mouse_init))
                    parents[str(nnode)] = node.node
        return

    def is_legal(self, node, close_list):
        m, n = self.puzzle_map.shape
        if node[0] < 0 or node[1] < 0 or node[0] >= m or node[1] >= n:
            return False
        if self.puzzle_map[node[0], node[1]] == 1:
            return False
        if str(node) in close_list.keys():
            return False
        return True

    def display(self, screen, block_lt_pos, block_shape):
        block = pygame.Surface(block_shape, flags=pygame.SRCALPHA)
        # block.convert_alpha()
        if self.SOLVED is False:
            block.fill(CORNFLOWERBLUE)
            block.set_alpha(100)
            lt_pos = [block_lt_pos[0] + self.last_node[0] * block_shape[0],
                      block_lt_pos[1] + self.last_node[1] * block_shape[1]]
            screen.blit(block, lt_pos)
            pygame.display.update()
            time.sleep(1. / FPS)

        else:
            block.fill(BLUEVIOLET)
            block.set_alpha(100)
            cat_head = pygame.transform.scale(pygame.image.load(cat_fn).convert_alpha(), block_shape)
            grass_block = pygame.transform.scale(pygame.image.load(grass_fn).convert_alpha(), block_shape)
            for i in range(len(self.path)):
                if i == 0:
                    continue
                lt_pos_post = [block_lt_pos[0] + self.path[i - 1][0] * block_shape[0],
                               block_lt_pos[1] + self.path[i - 1][1] * block_shape[1]]
                lt_pos_curr = [block_lt_pos[0] + self.path[i][0] * block_shape[0],
                               block_lt_pos[1] + self.path[i][1] * block_shape[1]]
                screen.blit(grass_block, lt_pos_post)
                screen.blit(block, lt_pos_post)
                screen.blit(cat_head, lt_pos_curr)
                pygame.display.update()
                pygame.event.pump()
                time.sleep(3. / FPS)
            time.sleep(1)
        return


class Agentv2(object):

    def __init__(self, puzzle_map):
        self.pmap = puzzle_map
        self.puzzle_map = puzzle_map.puzzle_map
        self.cat_init = puzzle_map.cat_init
        self.mouse_init = puzzle_map.mouse_init
        self.SOLVED = False
        self.open_list = None
        self.close_list = None
        self.path = None
        self.last_node = None
        self.last_jerry = self.mouse_init
        return

    class NextNode:
        def __init__(self, node, g, mouse_init):
            self.node = node
            self.g = g
            h = abs(node[0] - mouse_init[0]) + abs(node[1] - mouse_init[1])
            self.priority = h + g
            return

        def __cmp__(self, other):
            return cmp(self.priority, other.priority)

    def solver(self, screen, block_lt_pos, block_shape):
        orient = [[0, 1], [1, 0], [0, -1], [-1, 0]]
        orient_jerry = [[0, 1], [1, 0], [0, -1], [-1, 0]]
        self.open_list = PriorityQueue()
        self.close_list = {}
        self.last_node = []
        self.path = []
        self.open_list.put(self.NextNode(self.cat_init, 0, self.mouse_init))
        parents = {}
        # print('puzzle map: ')
        print(self.puzzle_map)

        while self.open_list.not_empty:
            pygame.event.pump()
            node = self.open_list.get()
            if str(node.node) in self.close_list:
                continue
            self.last_node = node.node
            self.display(screen, block_lt_pos, block_shape)
            if self.puzzle_map[node.node[0], node.node[1]] == -1:
                print("catch the mouse!")
                node_backtrack = node.node
                self.path.append(node_backtrack)
                while str(node_backtrack) in parents:
                    self.path.append(parents[str(node_backtrack)])
                    node_backtrack = parents[str(node_backtrack)]
                self.path.reverse()
                self.SOLVED = True
                self.display(screen, block_lt_pos, block_shape)
                break
            self.close_list[str(node.node)] = node.node
            for i in range(4):
                nnode = [sum(x) for x in zip(node.node, orient[i])]
                if self.is_legal(nnode) and not str(node) in self.close_list.keys():
                    self.open_list.put(self.NextNode(nnode, node.g + 1, self.mouse_init))
                    parents[str(nnode)] = node.node

            pygame.event.pump()
            node = self.open_list.get()
            if str(node.node) in self.close_list:
                continue
            self.last_node = node.node
            self.display(screen, block_lt_pos, block_shape)
            if self.puzzle_map[node.node[0], node.node[1]] == -1:
                print("catch the mouse!")
                node_backtrack = node.node
                self.path.append(node_backtrack)
                while str(node_backtrack) in parents:
                    self.path.append(parents[str(node_backtrack)])
                    node_backtrack = parents[str(node_backtrack)]
                self.path.reverse()
                self.SOLVED = True
                self.display(screen, block_lt_pos, block_shape)
                break
            self.close_list[str(node.node)] = node.node
            for i in range(4):
                nnode = [sum(x) for x in zip(node.node, orient[i])]
                if self.is_legal(nnode) and not str(node) in self.close_list.keys():
                    self.open_list.put(self.NextNode(nnode, node.g + 1, self.mouse_init))
                    parents[str(nnode)] = node.node

            pygame.event.pump()
            random.shuffle(orient_jerry)
            for i in range(4):
                nnode = [sum(x) for x in zip(self.mouse_init, orient_jerry[i])]
                if self.is_legal(nnode):
                    self.last_jerry = self.mouse_init
                    self.mouse_init = nnode
        return

    def is_legal(self, node):
        m, n = self.puzzle_map.shape
        if node[0] < 0 or node[1] < 0 or node[0] >= m or node[1] >= n:
            return False
        if self.puzzle_map[node[0], node[1]] == 1:
            return False
        return True

    def display(self, screen, block_lt_pos, block_shape):
        block = pygame.Surface(block_shape, flags=pygame.SRCALPHA)
        # block.convert_alpha()
        if self.SOLVED is False:
            block.fill(CORNFLOWERBLUE)
            block.set_alpha(100)
            mouse_head = pygame.transform.scale(pygame.image.load(mouse_fn).convert_alpha(), block_shape)
            grass_block = pygame.transform.scale(pygame.image.load(grass_fn).convert_alpha(), block_shape)
            lt_pos = [block_lt_pos[0] + self.last_node[0] * block_shape[0],
                      block_lt_pos[1] + self.last_node[1] * block_shape[1]]
            screen.blit(block, lt_pos)
            jerry_pos_post = [block_lt_pos[0] + self.last_jerry[0]*block_shape[0],
                              block_lt_pos[1] + self.last_jerry[1]*block_shape[1]]
            jerry_pos_curr = [block_lt_pos[0] + self.mouse_init[0]*block_shape[0],
                              block_lt_pos[1] + self.mouse_init[1]*block_shape[1]]
            screen.blit(mouse_head, jerry_pos_curr)
            screen.blit(grass_block, jerry_pos_post)
            if str(jerry_pos_post) in self.close_list.keys():
                screen.blit(block, jerry_pos_post)
            pygame.display.update()
            time.sleep(1. / FPS)

        else:
            block.fill(BLUEVIOLET)
            block.set_alpha(100)
            cat_head = pygame.transform.scale(pygame.image.load(cat_fn).convert_alpha(), block_shape)
            grass_block = pygame.transform.scale(pygame.image.load(grass_fn).convert_alpha(), block_shape)
            for i in range(len(self.path)):
                if i == 0:
                    continue
                lt_pos_post = [block_lt_pos[0] + self.path[i - 1][0] * block_shape[0],
                               block_lt_pos[1] + self.path[i - 1][1] * block_shape[1]]
                lt_pos_curr = [block_lt_pos[0] + self.path[i][0] * block_shape[0],
                               block_lt_pos[1] + self.path[i][1] * block_shape[1]]
                screen.blit(grass_block, lt_pos_post)
                screen.blit(block, lt_pos_post)
                screen.blit(cat_head, lt_pos_curr)
                pygame.display.update()
                pygame.event.pump()
                time.sleep(3. / FPS)
            time.sleep(1)
        return


class PuzzleMap(object):
    def __init__(self, M, N, grid, level):
        self.M = M
        self.N = N
        self.grid = grid
        self.level = level
        self.block_lt_pos = [50, 50]
        self.playground = [720, 640]
        self.cat_head = pygame.image.load(cat_fn).convert_alpha()
        self.mouse_head = pygame.image.load(mouse_fn).convert_alpha()
        self.grass_block = pygame.image.load(grass_fn).convert_alpha()
        self.stone_block = pygame.image.load(stone_fn).convert_alpha()
        self.block_shape = [self.playground[0]/self.M, self.playground[1]/self.N]
        self.grass_block = pygame.transform.scale(self.grass_block, self.block_shape)
        self.stone_block = pygame.transform.scale(self.stone_block, self.block_shape)
        self.mouse_head = pygame.transform.scale(self.mouse_head, self.block_shape)
        self.cat_head = pygame.transform.scale(self.cat_head, self.block_shape)
        # self.block_shape = [self.grass_block.get_width(), self.grass_block.get_height()]
        self.obstacle = None
        self.puzzle_map = None
        self.cat_init = None
        self.mouse_init = None
        return

    def map_generator(self):
        self.puzzle_map = np.zeros((self.M, self.N), dtype=np.int)
        tmp = set()
        while len(tmp) < 2:
            tmp.add((random.randint(0, self.M - 1), random.randint(0, self.N - 1)))
        self.cat_init, self.mouse_init = list(tmp)
        self.puzzle_map[self.cat_init[0], self.cat_init[1]] = 2
        self.puzzle_map[self.mouse_init[0], self.mouse_init[1]] = -1

        self.obstacle_generator()
        return

    def obstacle_generator(self):
        random.seed()
        obstacle_num = int(self.M * self.N * 0.1 * self.level)
        orient = [(-1, 0), (1, 0), (0, 1), (0, -1)]
        open_list = list()
        open_list.append(self.cat_init)
        close_list = dict()
        pmap = np.ones((self.M, self.N), dtype=np.int)
        pmap[self.cat_init[0]][self.cat_init[1]] = 0
        pmap[self.mouse_init[0]][self.mouse_init[1]] = -1
        while len(open_list) != 0:
            node = open_list.pop()
            if pmap[node[0]][node[1]] == -1:
                path = close_list.values()
                path.append(node)
                path = set(tuple(x) for x in path)
                # fullnode = set((i, j) for i in range(self.M) for j in range(self.N))
                self.obstacle = list(set((i, j) for i in range(self.M) for j in range(self.N)) - path)
                break
            close_list[str(node)] = node
            random.shuffle(orient)
            for i in range(4):
                nextnode = [sum(x) for x in zip(node, orient[i])]
                if(0 <= nextnode[0] < self.M and 0 <= nextnode[1] < self.N and (str(nextnode) not in close_list)):
                    open_list.append(nextnode)
        random.shuffle(self.obstacle)
        # print('obstacle num: ', obstacle_num)
        for i in range(max(0, len(self.obstacle)-obstacle_num)):
            self.obstacle.pop()
        for i in self.obstacle:
            self.puzzle_map[i[0], i[1]] = 1
        return

    def display(self, screen):

        for i in range(self.M):
            for j in range(self.N):
                screen.blit(self.grass_block, (self.block_lt_pos[0] + i * self.block_shape[0],
                                               self.block_lt_pos[1] + j * self.block_shape[1]))
        for i in self.obstacle:
            lt_x = self.block_lt_pos[0] + i[0] * self.block_shape[0]
            lt_y = self.block_lt_pos[1] + i[1] * self.block_shape[1]
            screen.blit(self.stone_block, (lt_x, lt_y))
        screen.blit(self.cat_head, (self.block_lt_pos[0] + self.block_shape[0] * self.cat_init[0],
                                    self.block_lt_pos[1] + self.block_shape[1] * self.cat_init[1]))
        screen.blit(self.mouse_head, (self.block_lt_pos[0] + self.block_shape[0] * self.mouse_init[0],
                                      self.block_lt_pos[1] + self.block_shape[1] * self.mouse_init[1]))
        # pygame.draw.rect(screen, BLACK, (self.block_lt_pos[0], self.block_lt_pos[1], 720, 640), 1)
        return
