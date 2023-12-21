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
            "area_max_entity_count INTEGER NOT NULL DEFAULT 10"
        ]);

        self.database   .make_table("areas_paths", [
            "path_id INTEGER PRIMARY KEY AUTOINCREMENT",
            "area_source_id INTEGER NOT NULL",
            "area_destination_id INTEGER NOT NULL"
        ],
        """
        FOREIGN KEY(area_source_id) REFERENCES areas(area_id) ON DELETE CASCADE
        FOREIGN KEY(area_destination_id) REFERENCES areas(area_id) ON DELETE CASCADE
        """)

        '''self.database   .make_table("entities", [
            "entity_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE",
            "entity_name TEXT UNIQUE",
            "entity_zone_active INTEGER NOT NULL",
            "entity_attack FLOAT NOT NULL DEFAULT 0",
            "entity_attack_speed FLOAT NOT NULL DEFAULT 0",
            "entity_defense FLOAT NOT NULL DEFAULT 0",
            "entity_life FLOAT NOT NULL DEFAULT 0",
            "entity_regeneration_speed FLOAT NOT NULL DEFAULT 0",
            "entity_level FLOAT NOT NULL DEFAULT 0",
            "entity_come_probability FLOAT NOT NULL DEFAULT 0"            
        ])

    def add_entity(self, area, entity_type):
        current_zone_id = self.database   .select("area_id", "areas where area_name = '" + area.name + "'")[0][0]
        self.database   .insert("entities",
            [entity_type.name,
            current_zone_id,
            entity_type.attributes.get("attack"),
            entity_type.attributes.get("attack_speed"),
            entity_type.attributes.get("attack"),
            entity_type.attributes.get("attack"),
            entity_type.attributes.get("attack"),
            entity_type.attributes.get("attack"),
            entity_type.attributes.get("attack"),
            entity_type.attributes.get("attack"),])'''

    def add_area(self, area):
        self.database   .insert("areas", [area.name, area.max_entities_count])

    def resolve_area_paths(self, area):
        source_area_id = self.database   .select("area_id", "areas where area_name = '" + area.name + "'")[0][0]
        for destination_area in area.next_areas:
            destination_area_id = self.database   .select("area_id", "areas where area_name = '" + destination_area.name + "'")[0][0]
            self.database   .insert("areas_paths", [source_area_id, destination_area_id])

    def add_player(self, player_entity, active_area_id = 0):
        self.database.insert("players", [
            player_entity.name,
            active_area_id,
            player_entity.attributes.get("attack"),
            player_entity.attributes.get("attack_speed"),
            player_entity.attributes.get("defense"),
            player_entity.attributes.get("life"),
            player_entity.attributes.get("regeneration_speed"),
            player_entity.attributes.get("level")
        ])