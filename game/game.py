from Components import *
import pygame
import sys
from random import randint


class Game:
    def __init__(self, dimension=4, margin=10):
        self.score = 0
        self.dimension = dimension
        self.board = Board()
        self.width = 800
        self.height = 800
        self.margin = margin
        self.size = self.width, self.height
        self.clock = pygame.time.Clock()
        self.block_size = (self.width - (self.dimension + 1) * self.margin) // self.dimension
        # initialize a random tile with power = 1, or value = 2^1 = 2
        self.board.set_tile_power((randint(0, self.dimension - 1), randint(0, self.dimension - 1)), 1)

    def draw_grid(self, screen):
        for y in range(len(self.board.get_grid())):
            row = self.board.get_grid()[y]
            for x in range(len(row)):
                tile = row[x]
                rect = pygame.Rect(x * self.block_size + (x + 1) * self.margin, y * self.block_size + (y + 1) *
                                   self.margin,
                                   self.block_size,
                                   self.block_size)
                pygame.draw.rect(screen, tile.bg_color, rect)

    def main(self):
        pygame.init()
        screen = pygame.display.set_mode(self.size)

        while True:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            screen.fill(self.board.bg_color)
            self.draw_grid(screen)

            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.main()
