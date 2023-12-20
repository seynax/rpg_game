import os
from random                 import *
from utils.choice_engine    import *

class Attributes:
    def __init__(self):
        self.attributes = {}

    def add(self, name, value):
        self.attributes[name + ".default"] = value
        self.attributes[name + ".current"] = value

    def get(self, name):
        return self.attributes[name + ".current"]

    def get_default(self, name):
        return self.attributes[name + ".default"]

    def operate(self, name, func):
        previousValue   = self.attributes[name + ".current"]
        newValue        = func(previousValue)
        self.attributes[name + ".current"] = newValue
        return (previousValue, newValue)

    def divide(self, name, value):
        return self.operate(name, lambda previousValue: previousValue / value)

    def multiply(self, name, value):
        return self.operate(name, lambda previousValue: previousValue * value)

    def decrease(self, name, value=1):
        return self.operate(name, lambda previousValue: previousValue - value)

    def increase(self, name, value=1):
        return self.operate(name, lambda previousValue: previousValue + value)

    def set(self, name, value):
        return self.operate(name, lambda previousValue: value)

    def reset(self, name):
        return self.operate(name, lambda previousValue: self.get_default(name))

class EntityType:
    def __init__(self, name, come_probability):
        self.name               = name
        self.attributesType     = {}
        self.come_probability   = come_probability

    def add_attribute(self, name, default_value):
        self.attributesType[name] = default_value

    def make_attributes(self):
        attributes = Attributes()
        for name, value in self.attributesType.items():
            attributes.add(name, value)
        return attributes

class Entity:
    def __init__(self, attributes, entity_type=None):
        self.attributes     = attributes
        self.entity_type    = entity_type


    def attempt_regenaration(self):
        life            = self.attributes.get        ("life")
        max_life        = self.attributes.get_default("life")
        if life >= max_life:
            return 0

        regeneration    = randint(0, self.attributes.get        ("regeneration_speed"))
        if regeneration <= 0:
            return -1

        if life + regeneration >= max_life:
            life = max_life
            return 2

        self.attributes.increase("life", regeneration)
        return 1

    def attempt_attack(self, attacked_entity):
        attacker_entity_attack  = randint(0, self.attributes.get("attack"))
        if attacker_entity_attack <= 0:
            return 0
        attacked_entity_defense = randint(1, attacked_entity.attributes.get("defense"))
        attacked_entity.attributes.decrease("life", attacker_entity_attack / attacked_entity_defense)
        return 1

    def attempt_pare(self, attacker_entity):
        attacker_max_speed      = attacker_entity.attributes.get("attack_speed")
        attacker_current_speed  = randint(0, attacker_max_speed)
        attacked_max_speed      = self.attributes.get("attack_speed")
        attacked_current_speed  = randint(0, attacked_max_speed)
        pare_chance_modifier    = 4 - randint(0, 8)

        state = randint(1, 2) if attacked_current_speed * pare_chance_modifier > attacker_current_speed else randint(0, 1)

        multiple_choices_index(state, [
            make_choice(execution=lambda value, parameters: self.attributes.divide("defense", 2)),
            make_choice(execution=lambda value, parameters: self.attributes.multiply("defense", 1.5)),
            make_choice(),
            make_choice(execution=lambda value, parameters: self.attributes.multiply("defense", 2))])

    def attempt_flee(self, attacker_entity):
        attacker_max_speed      = attacker_entity.attributes.get("attack_speed")
        attacker_current_speed  = randint(0, attacker_max_speed)
        attacked_max_speed      = self.attributes.get("attack_speed")
        attacked_current_speed  = randint(0, attacked_max_speed)

        if(attacked_current_speed >= attacker_current_speed):
            return 1
        return 0

    def make_decision(self, player_entity, last_player_action, last_player_action_state):
        attack_probability  =   randint(10, 75)
        pare_probability    =   randint(10, 75)
        flee_probability    =   randint(2,  25)

        if(last_player_action == 'a'):
            if(last_player_action_state == 1):
                attack_probability  /= 1.5
                pare_probability    *= 1.5
            else:
                attack_probability /= 2
                pare_probability *= 1.5
        elif(last_player_action == 'p'):
            attack_probability /= 1.5
        elif(self.attributes.get("life") < self.attributes.get_default("life") / 4):
            flee_probability *= 4

        rand = randint(0, int(attack_probability + pare_probability + flee_probability))

        if rand < attack_probability:
            return 'a'
        if rand < attack_probability + pare_probability:
            return 'p'
        return 'f'

class PlayerEntity:
    def __init__(self, name, attributes):
        self.entity     = Entity(attributes)
        self.attributes = attributes
        self.name       = name

    def attempt_attack(self, attacker_entity):
        state = self.entity.attempt_flee(attacker_entity)
        return multiple_choices_index(state, [
            make_choice(message="Vous tentez de fuir. C'est un echec.",
                        exit=True, state=0),
            make_choice(message="Vous tentez de fuir. C'est une réussite.",
                        exit=True, state=1)
        ])

    def attempt_pare(self, attacker_entity):
        state = self.entity.attempt_pare(attacker_entity)
        return multiple_choices_index(state, [
            make_choice(execution=lambda value, parameters: self.attributes.divide("defense", 2),
                        message="Vous tentez de parer, mais c'est un echec cuisant. Vous perdez beaucoup de défense (%p0 -> %p1)",
                        exit=True, state=0),
            make_choice(message="Vous tentez de parer, mais c'est un echec.",
                        exit=True, state=1),
            make_choice(execution=lambda value, parameters: self.attributes.multiply("defense", 1.5),
                        message="Vous tentez de parer, c'est une réussite. Vous gaagnez un peu de défense (%p0 -> %p1)",
                        exit=True, state=2),
            make_choice(execution=lambda value, parameters: self.attributes.multiply("defense", 2),
                        message="Vous tentez de parer, c'est une réussite écrasante. Vous gagnez de la défense (%p0 -> %p1)",
                        exit=True, state=3),
        ])

    def attempt_flee(self, attacker_entity):
        state = self.entity.attempt_flee(attacker_entity)
        return multiple_choices_index(state, [
            make_choice(message="Vous tentez de fuir. C'est un echec.",
                        exit=True, state=0),
            make_choice(message="Vous tentez de fuir. C'est une réussite.",
                        exit=True, state=1)
        ])

def make_entity_attributes(attack, attack_speed, defense, life, regeneration_speed):
    entity_attributes = Attributes()

    entity_attributes.add("attack", attack)
    entity_attributes.add("attack_speed", attack_speed)
    entity_attributes.add("defense", defense)
    entity_attributes.add("life", life)
    entity_attributes.add("regeneration_speed", regeneration_speed)

    return entity_attributes

def make_entity_type(name, attack, attack_speed, defense, life, regeneration_speed, come_probability=-1):
    entity_type = EntityType(name, come_probability)

    entity_type.add_attribute("attack", attack)
    entity_type.add_attribute("attack_speed", attack_speed)
    entity_type.add_attribute("defense", defense)
    entity_type.add_attribute("life", life)
    entity_type.add_attribute("regeneration_speed", regeneration_speed)

    return entity_type