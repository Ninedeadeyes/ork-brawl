from entity import Entity, get_blocking_entities_at_location
import libtcodpy as libtcod
from components.fighter import Fighter
from death_functions import kill_monster, kill_player
from fov_functions import initialize_fov, recompute_fov
from game_messages import MessageLog,Message
from game_states import GameStates 
from input_handlers import handle_keys 
from map_objects.game_map import GameMap
from render_functions import clear_all, render_all, RenderOrder
from random import randint

def main():
    screen_width = 190
    screen_height = 100

    bar_width = 20
    panel_height = 7
    panel_y = screen_height -panel_height    # panel y informs the y axis of 
                                             # of the panel for both message log
                                             # and health bar 


    message_x = bar_width + 2                  # message x informs the x axis
    message_width = screen_width-bar_width-2   # of the message 
    message_height = panel_height-1

    
    map_width = 170
    map_height = 80

    room_max_size = 20
    room_min_size = 8
    max_rooms = 100

    fov_algorithm = 0  # shape of pov 
    fov_light_walls = True  #if Walls will light or not  
    fov_radius = 15 

    max_monsters_per_room = 4


    colors = {

             "dark_wall": libtcod.Color(127,127,127),
             "dark_ground":libtcod.Color(127,101,63),
             "light_walls": libtcod.Color(127,137,127),
             "light_ground": libtcod.Color(127,110,63)



    }
    
    fighter_component = Fighter(hp =(randint(100,200)),defense =(randint(0,3)), power =(randint(20,40)))
    player = Entity(0,0,"@", libtcod.green,"Player",blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_component)
    entities = [player]



    libtcod.console_set_custom_font("arial10x10.png", libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

    libtcod.console_init_root(screen_width, screen_height, "Ork Brawl",False)
    
    con = libtcod.console_new(screen_width,screen_height)
    panel = libtcod.console_new(screen_width, panel_height)

    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, max_monsters_per_room)
    
    fov_recompute = True  
    #Because FOV doesn't need to be computed every turn (standing still), only need when moving to recompute 
    #True by default because it needs to be computed when the game start

    fov_map = initialize_fov(game_map)    # This call function and store result in fov_map

    message_log = MessageLog(message_x,message_width,message_height)

    test=Message("You wake up naked and angry with an urge to kill 'someting' ",libtcod.red)
    message=test
    message_log.add_message(message)
    
    
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    game_state = GameStates.PLAYERS_TURN

    

    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key , mouse )

        if fov_recompute:
            recompute_fov(fov_map,player.x,player.y,fov_radius, fov_light_walls,fov_algorithm)

        render_all(con,panel,entities,player,game_map,fov_map, fov_recompute,message_log, screen_width, screen_height, bar_width,
                  panel_height,panel_y,mouse,colors)

        fov_recompute = False  # in theory doesn't matter, can remove code but its good practise to 
                               # to switch it off when you are not using it 


        libtcod.console_flush()
        
        clear_all (con, entities)

        action = handle_keys(key)

        move = action.get("move")
        exit = action.get("exit")
        fullscreen = action.get("fullscreen")

        

        player_turn_results = []

       
        
        if move and game_state == GameStates.PLAYERS_TURN:
            dx, dy = move
            destination_x = player.x + dx
            destination_y = player.y + dy
            
            
           
            if not game_map.is_blocked(destination_x, destination_y):
                target = get_blocking_entities_at_location (entities,destination_x,destination_y)
                  # return entity or 'None' hence target=entity
                if target:
                    attack_results = player.fighter.attack(target)
                    player_turn_results.extend(attack_results)

                else:    
                    player.move(dx,dy)

                    fov_recompute = True   # will be in False due to game loop above 
                
                game_state = GameStates.ENEMY_TURN


        if exit:
            return True  # This could be either return False or break 
                         # returns a value to main hence ending the programme. 

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        for player_turn_result in player_turn_results:
            message = player_turn_result.get("message")
            dead_entity = player_turn_result.get ("dead")

            if message:
                message_log.add_message(message)

            if dead_entity:
                if dead_entity == player:
                    message,  game_state = kill_player(dead_entity)
                else:
                    message = kill_monster(dead_entity)

                message_log.add_message(message)


        if game_state == GameStates.ENEMY_TURN:
            for entity in entities:
                if entity.ai:
                    enemy_turn_results = entity.ai.take_turn(player, fov_map, game_map, entities)

                    for enemy_turn_result in enemy_turn_results:
                        message = enemy_turn_result.get("message")
                        dead_entity = enemy_turn_result.get("dead")

                        if message:
                            message_log.add_message(message)

                        if dead_entity:
                            if dead_entity == player:
                                message, game_state = kill_player(dead_entity)
                            else:
                                message = kill_monster(dead_entity)

                            message_log.add_message(message)

                            if game_state == GameStates.PLAYER_DEAD:
                                break

                    if game_state == GameStates.PLAYER_DEAD:
                        break
                    
            else:
                game_state =GameStates.PLAYERS_TURN



if __name__=='__main__':
    main()
