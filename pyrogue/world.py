"""
    pyrogue.world
    ~~~~~~~~~~~~~

    This module represents the world of the game, which handles all game logic
    outside of player input and drawing to the screen.
"""

import libtcodpy as libtcod

import player
import tile
import constants
import colors

import random

class World(object):
    """The game world, including all tiles and entities."""
    def __init__(self):
        self._map = Map()
        starting_pos = self._starting_pos()
        self.player = player.Player(starting_pos)
        self.tiles = self._map.current_level.tiles
        self.entities = [self.player]
    def _starting_pos(self):
        """This puts the player beside some upward stairs"""
        stairs = (pos for pos in self._map.current_level.up_stairs)
        for stair in stairs:
            for position in self._map.get_adjacents(stair):
                if self._map.is_empty(position):
                    return position
        raise Exception("Nowhere to put player...")
    def update(self):
        self.blocked_tiles = []
        for entity in self.entities:
            self.blocked_tiles.append(entity.pos)
        for position, tile in self.tiles.items():
            if tile.obstacle:
                self.blocked_tiles.append(position)
    def blocked(self, pos):
        return pos in self.blocked_tiles

class Map(object):
    """The game map, over all the levels."""
    def __init__(self):
        self.levels = 10
        self.current_level = Level()
        self.old_levels = []
    @staticmethod
    def get_adjacents(position):
        """Returns a generator of all points adjacent to a point."""
        pos_x, pos_y = position
        return ((a, b) for a in range(pos_x-1, pos_x+2)
                for b in range(pos_y-1, pos_y+2)
                if a != pos_x or b != pos_y
                and a >= 0 and b >= 0)
    def is_empty(self, position):
        return self.current_level.is_empty(position)
    def next_level(self):
        if self.levels:
            down_stairs = self.current_level.down_stairs
            self.current_level = Level(down_stairs)

class Level(object):
    """A single level, has more meta-data than just a matrix."""
    def __init__(self, down_stairs=None):
        self.stair_limit = 4
        self.empty_tiles = []
        self.carve_level()
        if down_stairs is None:
            generator = self.stair_gen("up")
            self.up_stairs = [pos for pos in generator]
        self.down_stairs = self.stair_gen("down")
    def carve_level(self):
        self.tiles = {}
        for width in range(constants.MAP_WIDTH):
            for height in range(constants.MAP_HEIGHT):
                # Fill map with unblocked tiles
                self.tiles[(width, height)] = tile.Floor()
                self.empty_tiles.append((width, height))
        self.tiles[(30, 22)] = tile.Wall()
        self.tiles[(50, 22)] = tile.Wall()
    def is_empty(self, position):
        return position in self.empty_tiles
    def stair_gen(self, direction):
        if direction == "up":
            stair = tile.UpStair
        else:
            stair = tile.DownStair
        stairs = []
        for _ in range(self.stair_limit):
            new_stair = random.choice(self.empty_tiles)
            stairs.append(new_stair)
            self.tiles[(new_stair)] = stair()
            self.empty_tiles.remove(new_stair)
        return stairs