import libtcodpy as libtcod

import math 

from render_functions import RenderOrder




class Entity:
    # A generic object to represent players, eneimes, items etc. 

 

    def __init__(self,x, y, char, color, name, blocks=False, render_order = RenderOrder.CORPSE, fighter = None, ai = None):
        self.x = x 
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks
        self.render_order = render_order
        self.fighter = fighter
        self.ai = ai 

        if self.fighter:
            self.fighter.owner = self 

        if self.ai:
            self.ai.owner = self 

 
    def move (self,dx,dy):
        self.x += dx
        self.y += dy

    
    def move_towards (self, target_x, target_y, game_map,entities):
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx = int(round(dx/distance))
        dy = int(round(dy/distance))

        if not (game_map.is_blocked(self.x + dx, self.y + dy) or 
                get_blocking_entities_at_location(entities, self.x + dx, self.y + dy)):

            self.move(dx,dy)

   

    def distance_to(self,other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx**2 + dy**2)

   
def get_blocking_entities_at_location (entities,destination_x,destination_y):
    for entity in entities:
        if entity.blocks and entity.x == destination_x and entity.y == destination_y:
            return entity

    return None		

# The reason the def is not within the class is because the function 
# eventhough related to the entities not specifically related to 
# a specific Entity so doesn't need to blong to the class 

#What the def get blockinging  function if one of them is blocking 
# and is at the x and y location we specified we return it. If none 
#of them match, then we return 'NONE' instead. 
