from utils.database import *

class GameDatabase:
    def __init__(self, path):
        self.database    = Database(path)

        self.database    .make_table("stats", [
            "player_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE",
            "player_name TEXT NOT NULL UNIQUE",
            "player_attack FLOAT NOT NULL DEFAULT 0",
            "player_attack_speed FLOAT NOT NULL DEFAULT 0",
            "player_defense FLOAT NOT NULL DEFAULT 0",
            "player_life FLOAT NOT NULL DEFAULT 0",
            "player_regeneration_speed FLOAT NOT NULL DEFAULT 0",
            "player_level FLOAT NOT NULL DEFAULT 0"])

    def add_player(self, player_entity):
        self.database.insert("stats", [
            player_entity.name,
            player_entity.attributes.get("attack"),
            player_entity.attributes.get("attack_speed"),
            player_entity.attributes.get("defense"),
            player_entity.attributes.get("life"),
            player_entity.attributes.get("regeneration_speed"),
            player_entity.attributes.get("level")
        ])