import math


class Tile:
    bg_colors = {
        "BACKGROUND": (172, 157, 142),
        None: (193, 179, 165),
        1: (233, 221, 209),
        2: (232, 217, 187),
        3: (235, 160, 99),
        4: (237, 128, 78),
        5: (237, 100, 75),
        6: (236, 69, 43),
        7: (231, 197, 90),
        8: (231, 197, 91),
        9: (231, 188, 55),
        10: (230, 185, 38),
        11: (230, 181, 19)
    }

    def __init__(self, power=None):
        self.power = power
        self.value = 2 ** self.power if self.power else None
        self.color = (255, 255, 255)
        self.bg_color = Tile.bg_colors[self.power]

    def increment(self):
        self.power += 1
        self.value = 2 ** self.power if self.power else None
        self.bg_color = Tile.bg_colors[self.power]

    @staticmethod
    def get_color_by_power(power):
        if power in Tile.bg_colors:
            return Tile.bg_colors[power]
        else:
            return Tile.bg_colors[6]

    @staticmethod
    def get_color_by_value(value):
        if type(value) == int:
            power = math.log(value, 2)
            if type(power) == float and power == power // 1:
                power = power // 1
            else:
                print("Error: value input is not correct")
                exit(1)
        else:
            power = 6
        return Tile.bg_colors[power]

    def get_bg_color(self):
        return self.bg_color

    def get_color(self):
        return self.color

    def get_power(self):
        return self.power

    def set_power(self, power):
        self.power = power
        self.bg_color = Tile.get_color_by_power(power)

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value
        self.bg_color = Tile.get_color_by_value(value)


class Board:
    def __init__(self, dimension=4):
        # initialize grid to 4x4 tile board
        self.grid = []
        self.dimension = dimension
        self.bg_color = (172, 157, 142)
        for i in range(4):
            row = []
            for j in range(4):
                row.append(Tile())
            self.grid.append(row)

    def get_value_board(self):
        """
        convert self(board object) to a 2D array of pure integers (values)
        :return: 2D arrays of values
        """
        value_board = []
        for row in self.grid:
            value_row = [tile.get_value() for tile in row]
            value_board.append(value_row)
        return value_board

    def get_power_board(self):
        """
        convert self(board object) to a 2D array of pure integers (powers)
        :return: 2D arrays of powers
        """
        power_board = []
        for row in self.grid:
            power_row = [tile.get_power() for tile in row]
            power_board.append(power_row)
        return power_board

    def get_grid(self):
        return self.grid

    def get_tile(self, coordinate):
        return self.grid[coordinate[0]][coordinate[1]]

    def set_tile_power(self, coordinate, power):
        self.get_tile(coordinate).set_power(power)
