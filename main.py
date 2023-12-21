from game.game              import *
from utils.choice_engine    import *
from random                 import *
from game.game_api          import *

game            = Game(player_entity_attributes=make_entity_attributes(25, 2, 8, 200, 4, 0))
print_players()

## ENTITIES TYPES
##                                              name,               attack, attack_speed,   defense,    life,   regeneration_speed, come_probability
spartan_type        =   game.add_entity_type(   "Spartane",         60,      0.5,            6,          400,    0.5,                10)
legionary_type      =   game.add_entity_type(   "Legionnaire",      40,      1,              2,          200,    1,                  25)
armed_civilian_type =   game.add_entity_type(   "Civil armée",      10,      1,              1,          150,    1,                  55)

## AREAS
##                                      name,               dangerousness,  max_entity_count
athena              =   game.add_area(  "Athène",           2,              10)
hapilly_forest      =   game.add_area(  "Hapilly Forest",   4,              10)
rome                =   game.add_area(  "Rome",             2,              10)
paris               =   game.add_area(  "Paris",             2,              10)

## AREA SPAWNERS
##  - IN ATHENA
##                             probability %,  min,    max,    entity type,            max count on spawner
athena.spawners.append(Spawner(8,              1,      1,      spartan_type,           2))
athena.spawners.append(Spawner(55,             1,      4,      armed_civilian_type,    8))

## AREA PATHS
def make_path(source, destination):
    source.next_areas.append(destination)
    destination.previous_areas.append(source)

make_path(athena, hapilly_forest)
make_path(athena, paris)
make_path(athena, rome)
make_path(rome, hapilly_forest)

input()

## FIRST AREA
game.current_area   =   athena

game.runtime() ## Launch game