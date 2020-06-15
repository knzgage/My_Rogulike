# A generic object to represent players, enemies, items and anything els in the game
class Entity:
    def __init__(self, x, y, char, color):
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    # Move an entity by certain x and y quantities
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
