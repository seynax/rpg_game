from game.game              import *
from utils.choice_engine    import *
from random                 import *
from game.game_flask        import *
from game.game_database     import *

game            = Game(player_entity_attributes=make_entity_attributes(25, 2, 8, 200, 4, 0))
game_database   = GameDatabase("resources/SQLITE/rpg_game.db")
game_database.add_player(game.player_entity)

## ENTITIES TYPES
##                                              name,               attack, attack_speed,   defense,    life,   regeneration_speed, come_probability
spartan_type        =   game.add_entity_type(   "Spartane",         60,      0.5,            6,          400,    0.5,                10)
legionary_type      =   game.add_entity_type(   "Legionnaire",      40,      1,              2,          200,    1,                  25)
armed_civilian_type =   game.add_entity_type(   "Civil armée",      10,      1,              1,          150,    1,                  55)

## AREAS
##                                      name,               dangerousness,  max_entity_count
athena_area         =   game.add_area(  "Athène",           2,              10)
hapilly_forest      =   game.add_area(  "Hapilly Forest",   4,              10)

## AREA SPAWNERS
##  - IN ATHENA
##                                  probability %,  min,    max,    entity type,            max count on spawner
athena_area.spawners.append(Spawner(8,              1,      1,      spartan_type,           2))
athena_area.spawners.append(Spawner(55,             1,      4,      armed_civilian_type,    8))

## AREA PATHS
hapilly_forest.previous_areas   .append(athena_area)
athena_area.next_areas          .append(hapilly_forest)

game_database.add_area(hapilly_forest)
game_database.add_area(athena_area)
game_database.database.select_print("*", "areas")
game_database.database.select_print("*", "areas_next")
game_database.database.select_print("*", "areas_previous")
input()

## FIRST AREA
game.current_area   =   athena_area

game.runtime() ## Launch game