import libtcodpy as libtcod

def initialize_fov(game_map):
    fov_map = libtcod.map_new(game_map.width, game_map.height)

    for y in range (game_map.height):
        for x in range (game_map.width):
	        libtcod.map_set_properties(fov_map, x,y, not game_map.tiles[x][y].block_sight,
				                       not game_map.tiles[x][y].blocked)    # not so that fov don't overlap wall 

    return fov_map

def recompute_fov(fov_map, x,y, radius, light_walls= True, algorithm=0):
	libtcod.map_compute_fov(fov_map,x,y,radius,light_walls,algorithm)

	
#The recompute function will modify the fov_map variable based on where the player is, 
#what the radius for lighting is, whether or not to light the walls, and what algorithm we're using.
#