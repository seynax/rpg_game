from utils.database import *

class GameDatabase:
    def __init__(self, path):
        self.database   = Database(path)

        self.database   .make_table("players", [
            "player_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE",
            "player_name TEXT NOT NULL UNIQUE",
            "player_zone_active INTEGER NOT NULL",
            "player_attack FLOAT NOT NULL DEFAULT 0",
            "player_attack_speed FLOAT NOT NULL DEFAULT 0",
            "player_defense FLOAT NOT NULL DEFAULT 0",
            "player_life FLOAT NOT NULL DEFAULT 0",
            "player_regeneration_speed FLOAT NOT NULL DEFAULT 0",
            "player_level FLOAT NOT NULL DEFAULT 0"])
        
        self.database   .make_table("areas", [
            "area_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE",
            "area_name TEXT NOT NULL UNIQUE",
            "area_max_entity_count INTEGER NOT NULL DEFAULT 10",
        ]);

        self.database   .make_table("areas_next", [
            "area_id INTEGER PRIMARY KEY",
            "area_other_id INTEGER PRIMARY KEY"
        ])

        self.database   .make_table("areas_previous", [
            "area_id INTEGER PRIMARY KEY",
            "area_other_id INTEGER PRIMARY KEY"
        ])

    def add_area(self, area):
        self.database   .insert("areas", [area.name, area.max_entities_count])
        current_zone_id = self.database   .select("area_id", "areas where area_name = '" + area.name + "'")[0][0]

        for previous_area in area.previous_areas:
            previous_area_id = self.database   .select("area_id", "areas where area_name = '" + previous_area.name + "'")[0][0]
            self.database   .insert("areas_previous", [current_zone_id, previous_area_id], include_primary_key=True)

        for next_area in area.next_areas:
            next_area_id = self.database   .select("area_id", "areas where area_name = '" + next_area.name + "'")[0][0]
            self.database   .insert(table="areas_next", parameters=[current_zone_id, next_area_id], include_primary_key=True)

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