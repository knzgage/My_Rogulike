import tcod as libtcod
from random import randint

from components.ai import BasicMonster
from components.fighter import Fighter
from entity import Entity
from map_objects.tile import Tile
from map_objects.rectangle import Rect


class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

        return tiles

    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities,
                 max_monsters_per_room):
        # Create two rooms
        rooms = []
        num_rooms = 0

        for r in range(max_rooms):
            # Random width and height
            w = randint(room_min_size, room_max_size)
            h = randint(room_min_size, room_max_size)
            # Random position without going out of the boundaries of the map
            x = randint(0, map_width - w - 1)
            y = randint(0, map_height - h - 1)

            # Make the rectangle to work with
            new_room = Rect(x, y, w, h)

            # Check to see if new room intersects with any existing rooms
            for other_room in rooms:
                if new_room.intersect(other_room):
                    break

            # No intersections, so we can make the room
            else:
                # "Paint" the room to the map's tiles
                self.create_room(new_room)

                new_x, new_y = new_room.center()

                # If we are making the first room, put the player in it
                if num_rooms == 0:
                    player.x = new_x
                    player.y = new_y

                # All rooms after the first one
                else:
                    prev_x, prev_y = rooms[num_rooms - 1].center()

                    # 50/50 chance at which order we connect the new room to the previous
                    if randint(0, 1) == 1:
                        # Make tunnel horizontally, then vertically
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        # Make tunnel vertically then horizontally
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)

                #Add monsters to the room
                self.place_entities(new_room, entities, max_monsters_per_room)
                # Append the new room to the list
                rooms.append(new_room)
                num_rooms += 1

    def create_room(self, room):
        # Go through all the tiles in a rectangle and make them passable
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def place_entities(self, room, entities, max_monsters_per_room):
        # Get a random number of monsters
        number_of_monsters = randint(0, max_monsters_per_room)

        for i in range(number_of_monsters):
            # Choose a random location in the room
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            # Make sure there is no entity in the space we want to place monster
            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                # 80% chance of orc, 20% chance of troll
                if randint(0, 100) < 80:
                    fighter_component = Fighter(hp=10, defense=0, power=3)
                    ai_component = BasicMonster()
                    monster = Entity(x, y, 'o', libtcod.desaturated_green, "Orc", blocks=True,
                                     fighter=fighter_component, ai=ai_component)
                else:
                    fighter_component = Fighter(hp=16, defense=1, power=4)
                    ai_component = BasicMonster()
                    monster = Entity(x, y, 'T', libtcod.darker_green, "Troll", blocks=True,
                                     fighter=fighter_component, ai=ai_component )

                entities.append(monster)

    # Tells whether a  tile blocks movement or not
    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True

        return False
