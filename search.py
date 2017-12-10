import numpy as np
from Queue import PriorityQueue
import pygame
import time
from color_map import *

FPS = 30


class Agent(object):

    def __init__(self, puzzle_map):
        self.pmap = puzzle_map
        self.puzzle_map = puzzle_map.puzzle_map
        self.cat_init = puzzle_map.cat_init
        self.mouse_init = puzzle_map.mouse_init
        self.SOLVED = False
        return

    class NextNode:
        def __init__(self, node, g, mouse_init):
            self.node = node
            self.g = g
            h = abs(node[0] - mouse_init[0]) + abs(node[1] - mouse_init[1])
            self.priority = h + g
            return

        def __lt__(self, other):
            return self.priority < other.priority

    def solver(self, screen, block_lt_pos, block_shape):
        orient = [[0, 1], [1, 0], [0, -1], [-1, 0]]
        self.open_list = PriorityQueue()
        self.close_list = {}
        self.path = []
        self.open_list.put(self.NextNode(self.cat_init, 1, self.mouse_init))
        parents = {}
        print('puzzle map: ')
        print(self.puzzle_map)

        while self.open_list.not_empty:
            pygame.event.pump()
            node = self.open_list.get()
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
            self.display(screen, block_lt_pos, block_shape)
            for i in range(4):
                # nnode = map(add, node.node, orient[i])
                nnode = [sum(x) for x in zip(node.node, orient[i])]
                if self.is_legal(nnode, self.close_list):
                    self.open_list.put(self.NextNode(nnode, node.g + 1, self.mouse_init))
                    parents[str(nnode)] = node.node
            # time.sleep(1./FPS)
            # time.sleep(1)
        print("Path: ", self.path)
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
        self.pmap.display(screen)
        block = pygame.Surface(block_shape, flags=pygame.SRCALPHA)
        block.convert_alpha()
        if self.SOLVED is False:
            print('close list: ', self.close_list.keys())
            block.fill(CORNFLOWERBLUE)
            for k, v in self.close_list.iteritems():
                lt_pos = [block_lt_pos[0]+v[0]*block_shape[0], block_lt_pos[1]+v[1]*block_shape[1]]
                screen.blit(block, lt_pos)
                pygame.display.update()
                time.sleep(1./FPS)

        else:
            pygame.display.flip()
            block.fill(BLUEVIOLET)
            for i in self.path:
                lt_pos = [block_lt_pos[0]+i[0]*block_shape[0], block_lt_pos[1]+i[1]*block_shape[1]]
                screen.blit(block, lt_pos)
                pygame.display.update()
                time.sleep(1./FPS)
            time.sleep(1)
            cat_head = pygame.image.load(cat_fn).convert_alpha()
            grass_block = pygame.image.load(grass_fn).convert_alpha()
            grass_block = pygame.transform.scale(grass_block, (cat_head.get_width(), cat_head.get_height()))
            for i in range(len(self.path)):
                if i == 0:
                    continue
                lt_pos_post = [block_lt_pos[0]+self.path[i-1][0]*block_shape[0], block_lt_pos[1]+self.path[i-1][1]*block_shape[1]]
                lt_pos_curr = [block_lt_pos[0]+self.path[i][0]*block_shape[0], block_lt_pos[1]+self.path[i][1]*block_shape[1]]
                screen.blit(block, lt_pos_post)
                screen.blit(grass_block, lt_pos_post)
                screen.blit(cat_head, lt_pos_curr)
                pygame.display.update()
                time.sleep(1./2)
        # time.sleep(1./FPS)
        # pygame.display.flip()
        return


class PuzzleMap(object):
    def __init__(self, M, N, cat_init, mouse_init, grid, level):
        self.M = M
        self.N = N
        self.puzzle_map = np.zeros((self.M, self.N), dtype=np.int)
        self.cat_init = cat_init
        self.mouse_init = mouse_init
        self.grid = grid
        self.level = level
        self.block_lt_pos = [50, 50]
        self.obstacle = [[1, 4], [3, 1], [3, 2], [3, 3], [3, 4]]
        self.cat_head = pygame.image.load(cat_fn).convert_alpha()
        self.mouse_head = pygame.image.load(mouse_fn).convert_alpha()
        self.grass_block = pygame.image.load(grass_fn).convert_alpha()
        self.stone_block = pygame.image.load(stone_fn).convert_alpha()
        self.grass_block = pygame.transform.scale(self.grass_block,
                                                  (self.cat_head.get_width(), self.cat_head.get_height()))
        self.stone_block = pygame.transform.scale(self.stone_block,
                                                  (self.cat_head.get_width(), self.cat_head.get_height()))
        self.block_shape = [self.grass_block.get_width(), self.grass_block.get_height()]
        return

    def map_generator(self):
        self.puzzle_map[self.cat_init[0], self.cat_init[1]] = 2
        self.puzzle_map[self.mouse_init[0], self.mouse_init[1]] = -1
        self.obstacle_generator()
        return

    def obstacle_generator(self):
        for i in self.obstacle:
            self.puzzle_map[i[0], i[1]] = 1
        return

    def display(self, screen):

        for i in range(self.M):
            for j in range(self.N):
                screen.blit(self.grass_block, (self.block_lt_pos[0]+i*self.block_shape[0],
                                               self.block_lt_pos[1]+j*self.block_shape[1]))
        for i in self.obstacle:
            lt_x = self.block_lt_pos[0]+i[0]*self.block_shape[0]
            lt_y = self.block_lt_pos[1]+i[1]*self.block_shape[1]
            screen.blit(self.stone_block, (lt_x, lt_y))
        screen.blit(self.cat_head, (self.block_lt_pos[0]+self.block_shape[0]*self.cat_init[0],
                                    self.block_lt_pos[1]+self.block_shape[1]*self.cat_init[1]))
        screen.blit(self.mouse_head, (self.block_lt_pos[0]+self.block_shape[0]*self.mouse_init[0],
                                      self.block_lt_pos[1]+self.block_shape[1]*self.mouse_init[1]))
        return
