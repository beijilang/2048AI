from components import *
import pygame
from random import randint, random
from constants import *


class Game:
    def __init__(self, dimension=4, margin=10):
        self.score = 0
        self.dimension = dimension
        self.board = Board()
        self.width = 800
        self.height = 800
        self.key_down = False
        self.margin = margin
        self.size = self.width, self.height
        self.clock = pygame.time.Clock()
        self.block_size = (self.width - (self.dimension + 1) * self.margin) // self.dimension
        # initialize a random tile with power = 1, or value = 2^1 = 2
        self.board.set_tile_power((randint(0, self.dimension - 1), randint(0, self.dimension - 1)), 1)

    def draw_grid(self, screen):
        font = pygame.font.Font(None, 64)
        for y in range(len(self.board.get_grid())):
            row = self.board.get_grid()[y]
            for x in range(len(row)):
                tile = row[x]
                rect = pygame.Rect(x * self.block_size + (x + 1) * self.margin, y * self.block_size + (y + 1) *
                                   self.margin,
                                   self.block_size,
                                   self.block_size)
                pygame.draw.rect(screen, tile.bg_color, rect)
                if type(tile.value) == int:
                    text_content = str(tile.value)
                else:
                    text_content = ''
                text = font.render(text_content, 30, tile.color)
                textpos = text.get_rect()
                textpos.center = rect.center
                screen.blit(text, textpos)

    def main(self):
        pygame.init()
        screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption('2048')

        while True:
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    self.handle_key_down(event)
                elif event.type == pygame.KEYUP:
                    self.handle_key_up(event)

            screen.fill(self.board.bg_color)
            self.draw_grid(screen)

            pygame.display.flip()

        pygame.quit()

    def handle_key_down(self, event):
        self.key_down = True
        if event.key == pygame.K_LEFT:
            self.board.move(LEFT)
        elif event.key == pygame.K_RIGHT:
            self.board.move(RIGHT)
        elif event.key == pygame.K_UP:
            self.board.move(UP)
        elif event.key == pygame.K_DOWN:
            self.board.move(DOWN)
        else:
            return
        # add a random tile, 2 or 4
        is_4 = random() < 0.1
        empty_pos = self.board.get_empty_tiles_pos()
        target_pos = empty_pos[randint(0, len(empty_pos) - 1)]
        print("random title position: " + str(target_pos))
        if is_4:
            self.board.set_tile_power(target_pos, 2)
        else:
            self.board.set_tile_power(target_pos, 1)



    def handle_key_up(self, event):
        self.key_down = False


if __name__ == "__main__":
    game = Game()
    game.main()
