import os
from random                 import *
from utils.choice_engine    import *
from game.entity            import *

class Area:
    def __init__(self, name, dangerousness, max_entities_count):
        self.name               = name
        self.dangerousness      = dangerousness
        self.next_areas         = []
        self.previous_areas     = []
        self.entities           = []
        self.max_entities_cont  = max_entities_count
        self.spawners           = []

    def add_entity(self, entity_type, count=1):
        i = 0
        while i < count:
            self.entities.append(Entity(entity_type))
            i += 1

    def print_areas_if_exists(self, areas, base_text, counter=0):
        if len(areas) <= 0:
            return counter

        text = base_text
        i = 0
        for area in areas:
            if i > 0:
                text += ", "
            text += "[" + str(counter) + "] " + area.name
            counter += 1
            i += 1
        print(text)
        return counter

    def print(self):
        print("Vous êtes actuellement dans la zone " + self.name)
        counter = self.print_areas_if_exists(self.previous_areas,   "Les zones précédentes sont : ",    0)
        counter = self.print_areas_if_exists(self.next_areas,       "Les zones suivantes sont : ",      counter)

    def getArea(self, index):
        if index < len(self.previous_areas):
            return self.previous_areas[index]

        return self.next_areas[index - len(self.previous_areas)]

    def runtime(self):
        ## Entities come runtime
        for entity in self.entities:
            if randint(0, 100) <= entity.entity_type.come_probability:
                return entity

        ## Entities spawn runtime
        if len(self.entities) >= self.max_entities_cont:
            return
        for spawner in self.spawners:
            spawner.spawn(self)

class Spawner:
    def __init__(self, probability, min, max, entity_type, max_count_on_area):
        self.probability            = probability
        self.min                    = min
        self.max                    = max
        self.entity_type            = entity_type
        self.current_count_on_map   = 0
        self.max_count_on_area       = max_count_on_area

    def spawn(self, area):
        if(randint(0, 100) <= self.probability):
            count = randint(self.min, self.max)
            if(self.current_count_on_map + count > self.max_count_on_area):
                return
            self.current_count_on_map += count
            area.add_entity(self.entity_type, count)
            return count
        return

class Game:
    def __init__(self, player_entity_attributes):
        player_name = None
        while player_name == None or not isinstance(player_name, str):
            player_name = input("Player name ? ")

        self.player_entity  = PlayerEntity(player_name, player_entity_attributes)
        self.entity_types   = []
        self.areas          = []
        self.running        = True
        self.front_entity   = None

    def add_entity_type(self, name, attack, attack_speed, defense, life, regeneration_speed, come_probability):
        entity_type = make_entity_type(name, attack, attack_speed, defense, life, regeneration_speed, come_probability)
        self.entity_types.append(entity_type)
        return entity_type

    def add_area(self, name, dangerousness, max_entity_count):
        area = Area(name, dangerousness, max_entity_count)
        self.areas.append(area)
        return area

    def runtime(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        if not self.running:
            return

        if(self.front_entity != None):
            self.combat_runtime()
        else:
            self.map_runtime()

    def map_runtime(self):
        if self.current_area == None:
            print("Vous n'existez pas")
            return

        self.current_area.print()

        area    = None
        while(area == None):

            action  = None
            while(action == None or not action.isnumeric()):
                action = input("Choisissez une zone à explorer (grâce à son index). Q -> QUIT : ")
                if action == "q":
                    self.running = False
                    return

            area = self.current_area.getArea(int(action))

        self.current_area = area
        come_entity = self.current_area.runtime()
        if come_entity != None:
            self.front_entity   = come_entity
        self.runtime()

    def combat_runtime(self):
        self.player_entity.attributes.reset("defense")
        print("Vous faites face à un " + self.front_entity.entity_type.name + " !")
        action = input("Choissisez une action. A -> ATTAQUER, P -> PARER, F -> FUIR, Q -> Quitter")
        if action.lower() == 'q':
            self.running = False
            return

        os.system('cls' if os.name == 'nt' else 'clear')
        action_state = -1
        if action.lower() == "p":
            action_state = self.player_entity.attempt_pare()[0]
        elif action.lower() == "f":
            if self.player_entity.attempt_flee(self.front_entity) == 1:
                self.front_entity = None
                input()
                self.runtime() ## STOP COMBAT
        elif action.lower() == "a":
            action_state = self.player_entity.attempt_attack(self.front_entity)

        action = self.front_entity.make_decision(self.player_entity, action, action_state)
        print("Action de l'adversaire : " + action)
        input()
        if action.lower() == "p":
            state = randint(0, 3)
        elif action.lower() == "f":
            action_state = self.front_entity.attack(self.player_entity)
            if action_state == 0:
                print("L'adversaire tente de vous attaquer. C'est un echec. Vous avez " + str(self.player_entity.attributes.get("life")))
            else:
                print("L'adversaire tente de vous attaquer. C'est une réussite. Vous avez " + str(self.player_entity.attributes.get("life")))

        if self.front_entity.attributes.get("life") <= 0:
            print("L'adversaire est vaincue !")
            input()
            self.increase_player_level()
            self.runtime()
        elif self.player_entity.attributes.get("life") <= 0:
            print("Vous avez perdu !")
            return ## EXIT GAME

        self.front_entity.regen()
        self.player_entity.regen()
        self.combat_runtime() ## CONTINUE COMBAT

    def increase_player_level(self):
        self.player_entity.attributes.increase("level")

def make_entity_attributes(attack, attack_speed, defense, life, regeneration_speed, level):
    entity_attributes = Attributes()

    entity_attributes.add("attack", attack)
    entity_attributes.add("attack_speed", attack_speed)
    entity_attributes.add("defense", defense)
    entity_attributes.add("life", life)
    entity_attributes.add("regeneration_speed", regeneration_speed)
    entity_attributes.add("level", level)

    return entity_attributes

def make_entity_type(name, attack, attack_speed, defense, life, regeneration_speed, come_probability=-1):
    entity_type = EntityType(name, come_probability)

    entity_type.add_attribute("attack", attack)
    entity_type.add_attribute("attack_speed", attack_speed)
    entity_type.add_attribute("defense", defense)
    entity_type.add_attribute("life", life)
    entity_type.add_attribute("regeneration_speed", regeneration_speed)

    return entity_type