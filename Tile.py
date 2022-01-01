import pygame
import Color
import os
import time
"""Tiles."""
WHITE_TILE = pygame.image.load(os.path.join("assets", "white.png"))
YELLOW_TILE = pygame.image.load(os.path.join("assets", "yellow.png"))
RED_TILE = pygame.image.load(os.path.join("assets", "red.png"))

"""A class that represents the tiles on the Connect 4 board. """


class Tile:
    def __init__(self, x, y):
        self.color = Color.Colors.WHITE
        image = self.get_path()
        self.image = image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

    def __str__(self):
        """Returns a string with the color of the tile."""
        return f"Tile Color: {Color.Colors.tostring(self.color)}"

    def __eq__(self, other):
        return isinstance(other, Tile) and \
               self.color == other.color

    def get_path(self):
        """Returns the path of a tile specified
        by the color. """
        if self.color == Color.Colors.WHITE:
            return WHITE_TILE
        elif self.color == Color.Colors.YELLOW:
            return YELLOW_TILE
        else:
            return RED_TILE

    def change_color(self, player_color: Color.Colors):
        """ Changes the color of the tile. """
        if self.color != Color.Colors.WHITE:
            raise ValueError
        else:
            self.color = player_color
            self.image = self.get_path()
            self.rect = self.image.get_rect()

    def change_to_white(self):
        """Changes a tile back to the color WHITE. """
        if self.color == Color.Colors.WHITE:
            raise ValueError
        else:
            self.color = Color.Colors.WHITE
            self.image = self.get_path()
            time.sleep(0.1)
            self.rect = self.image.get_rect()

