
import libtcodpy as libtcod
from random import randint
from components.ai import BasicMonster
from components.fighter import Fighter
from entity import Entity
from map_objects.tile import Tile 
from map_objects.rectangle import Rect
from render_functions import RenderOrder

class GameMap: 
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range (self.height)] for x in range(self.width)]
        
        return tiles 

        #By setting  Tile(False) to True it will initilazie all our tiles to be blocked 
        #by default and we all rooms will be 'digged' out and hence unblocked

    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player,entities,max_monsters_per_room):
        rooms = []
        num_rooms = 0

        for r in range(max_rooms):
            # random width and height 
            w = randint(room_min_size, room_max_size)
            h = randint(room_min_size, room_max_size)
            # random position without going out of the boundaries of the map
            x = randint (0, map_width - w - 1)
            y = randint (0, map_height - h - 1)
             #-1 becasue trying to find top left x and y axis (rem original formula room.x1+1)

            new_room = Rect(x, y , w, h)
            #Rect class make rectangle easier to work with 

            for other_room in rooms:   # Run through the others rooms and see if they intersect with this one if interect breaks. 
                if new_room.intersect(other_room):
                    break
            
            else:    # this means there are no intersections, so this room is valid
            
                self.create_room(new_room)   # paint it to the map's tile 
 
                (new_x, new_y) = new_room.center()  #Center coordinate of new rooms, used to put player in and tunnels  

                if num_rooms == 0:   # This is the first room, where the player starts at (variable above) 
                    player.x = new_x
                    player.y = new_y          

                else:    #All rooms after thie first : Connect it to the previous room with a tunnel in the center 
                    
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()  # center coordinates of previous room 

                    if randint(0, 1) == 1:    #Flip a coin ( random that is either 1 or 0 )
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y,new_y, new_x)

                    else:    #first, move vertically, then hoizontally 
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x,new_x, new_y)


                        # create a v and h tunnel if new room is distant away from the center from previous room 
                        # only create one tunnel if new room is only 1 direction away from previous room (same y or x axis) 
                
                self.place_entities(new_room, entities, max_monsters_per_room)

                rooms.append(new_room)
                num_rooms += 1

    def create_room (self, room) :
        #go through the tiles in the rectangle and make them passable 
        for x in range (room.x1 +1, room.x2 ):
            for y in range (room.y1 +1, room.y2):
                self.tiles [x][y].blocked =False
                self.tiles [x][y].block_sight =False
      
      # x1 and y1 is the x and y value whilst x2 is the end width value of x and y2 is the end length value of y  
      # Look at Rectangle.py 
      # From x1 to x2, and y1 to y2, we'll want to set each tile in the Rect to be not blocked
      # +1 because there will always be a wall inbetween different rooms. 
      # don't subtract from x2 and y2 because it doesn not include end value of range (0,10)
      #1,2,3,4,5,6,7,8,9
   
    def create_h_tunnel (self,x1,x2,y):
        for x in range (min(x1,x2), max(x1, x2) + 1):
            self.tiles [x][y].blocked = False
            self.tiles [x][y].block_sight = False

    def create_v_tunnel (self,y1, y2, x) :
        for y in range (min(y1,y2), max (y1, y2) + 1 ):
            self.tiles [x][y].blocked = False
            self.tiles [x][y].block_sight = False
    
    # Two above functions make tunnels passable.  
    # Just augments are used instead of the Rect function like rooms
        
    def place_entities(self,room, entities, max_monsters_per_room):
        #Get a random numbers of Monster
        number_of_monsters = randint(0,max_monsters_per_room)

        for i in range(number_of_monsters):
            #choose a random location in the room 
            x = randint (room.x1 + 1, room.x2 -1)   # -1 because entity will be in area of wall if not 
            y = randint (room.y1 + 1, room.y2 -1)

            if not any ([entity for entity in entities if entity.x == x and entity.y== y]):
                if randint(0,100) < 50:
                    fighter_component = Fighter ( hp =25, defense = 1, power=3)
                    ai_component = BasicMonster()

                    monster = Entity (x,y,"S",libtcod.yellow,"Snotling",blocks=True, render_order =RenderOrder.ACTOR, fighter= fighter_component,
                                       ai = ai_component)

                else:

                    fighter_component = Fighter(hp=40, defense=3, power = 4) 
                    ai_component = BasicMonster()
                    monster = Entity(x,y,"G", libtcod.darker_green,"Grot",blocks=True,render_order =RenderOrder.ACTOR, fighter= fighter_component,
                        ai = ai_component)


                entities.append(monster)
         
      # Above function place monsters into the dungeon 'entities' is a list in the engine 
      # hence it states if there is no entity at a entity within the list entities with equal x and y 

  
    def is_blocked(self,x,y):
        if self.tiles[x][y].blocked:
            return True

        return False
        
            


        
