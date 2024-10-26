import math
from typing import Dict

from BaseClasses import CollectionState, Entrance, Item, ItemClassification, Location, Region, Tutorial

from worlds.AutoWorld import WebWorld, World

from .Items import YachtDiceItem, item_table, group_table
from .Locations import YachtDiceLocation, all_locations, ini_locations
from .Rules import set_yacht_completion_rules, set_yacht_rules


class YachtDiceWeb(WebWorld):
    tutorials = [
        Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up Yacht Dice. This guide covers single-player, multiworld, and website.",
            "English",
            "setup_en.md",
            "setup/en",
            ["Spineraks"],
        )
    ]


class YachtDiceWorld(World):
    """
    Yacht Dice is a straightforward game, custom-made for Archipelago,
    where you cast your dice to chart a course for high scores,
    unlocking valuable treasures along the way.
    Discover more dice, extra rolls, multipliers,
    and unlockable categories to navigate the depths of the game.
    Roll your way to victory by reaching the target score!
    """

    game: str = "Watery Words"

    web = YachtDiceWeb()

    item_name_to_id = {name: data.code for name, data in item_table.items()}

    location_name_to_id = {name: data.id for name, data in all_locations.items()}
    
    item_name_groups = group_table

    ap_world_version = "0.0.1"

    def _get_yachtdice_data(self):
        return {
            # "world_seed": self.multiworld.per_slot_randoms[self.player].getrandbits(32),
            "seed_name": self.multiworld.seed_name,
            "player_name": self.multiworld.get_player_name(self.player),
            "player_id": self.player,
            "race": self.multiworld.is_race,
        }

    def generate_early(self):
        """
        In generate early, we fill the item-pool, then determine the number of locations, and add filler items.
        """
        self.itempool = []
        self.precollected = []
        
        WW_letters = (
            ['A'] * 9 + ['B'] * 2 + ['C'] * 2 + ['D'] * 4 + ['E'] * 12 + ['F'] * 2 +
            ['G'] * 3 + ['H'] * 2 + ['I'] * 9 + ['J'] * 1 + ['K'] * 1 + ['L'] * 4 +
            ['M'] * 2 + ['N'] * 6 + ['O'] * 8 + ['P'] * 2 + ['Q'] * 1 + ['R'] * 6 +
            ['S'] * 4 + ['T'] * 6 + ['U'] * 4 + ['V'] * 2 + ['W'] * 2 + ['X'] * 1 +
            ['Y'] * 2 + ['Z'] * 1
        )

        possible_start_words = ["the", "and", "for", "are", "but", "not", "you", "all", "any", "can", "had", "her", "was", "one", "our", "out", "day", "get", "has", "him", "his", "how", "man", "new", "now", "old", "see", "two", "way", "who", "boy", "did", "its", "let", "put", "say", "she", "too", "use"];
        
        # Choose a word randomly from possible_start_words
        selected_word = self.random.choice(possible_start_words)
        word_letters = [letter.upper() for letter in selected_word]

        # Remove each letter in the selected word from WW_letters
        for letter in word_letters:
            self.precollected.append(letter)
            print(letter)
            WW_letters.remove(letter)  # This removes one occurrence of the letter from WW_letters
        self.itempool += WW_letters
        
        self.precollected += ["Extra turn"] * 3
        self.itempool += ["Extra turn"] * 10
        
        for item in self.precollected:
            self.multiworld.push_precollected(self.create_item(item))

        # max score is the value of the last check. Goal score is the score needed to 'finish' the game
        self.max_score = 1000
        self.goal_score = 777
        
        self.number_of_locations = len(self.itempool) + 1


    def create_items(self):
        self.multiworld.itempool += [self.create_item(name) for name in self.itempool]

    def create_regions(self):
        # call the ini_locations function, that generates locations based on the inputs.
        location_table = ini_locations(
            self.goal_score,
            self.max_score,
            self.number_of_locations
        )

        # simple menu-board construction
        menu = Region("Menu", self.player, self.multiworld)
        board = Region("Board", self.player, self.multiworld)

        # add locations to board, one for every location in the location_table
        board.locations = [
            YachtDiceLocation(self.player, loc_name, loc_data.score, loc_data.id, board)
            for loc_name, loc_data in location_table.items()
            if loc_data.region == board.name
        ]

        # Change the victory location to an event and place the Victory item there.
        victory_location_name = f"{self.goal_score} score"
        self.get_location(victory_location_name).address = None
        self.get_location(victory_location_name).place_locked_item(
            Item("Victory", ItemClassification.progression, None, self.player)
        )

        # add the regions
        connection = Entrance(self.player, "New Board", menu)
        menu.exits.append(connection)
        connection.connect(board)
        self.multiworld.regions += [menu, board]

    def get_filler_item_name(self) -> str:
        return "A tile but you can't quite read what letter it is, so you decide to throw it away."

    def set_rules(self):
        """
        set rules per location, and add the rule for beating the game
        """
        set_yacht_rules(
            self.multiworld,
            self.player
        )
        set_yacht_completion_rules(self.multiworld, self.player)


    def create_item(self, name: str) -> Item:
        item_data = item_table[name]
        item = YachtDiceItem(name, item_data.classification, item_data.code, self.player)
        return item
