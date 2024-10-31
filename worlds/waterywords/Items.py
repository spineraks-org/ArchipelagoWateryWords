import typing
import string


from BaseClasses import Item, ItemClassification
from typing import Dict, Set

class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    classification: ItemClassification


class YachtDiceItem(Item):
    game: str = "Watery Words"


# the starting index is chosen semi-randomly to be 16871244000

letters = list(string.ascii_uppercase)
trap_letters = ["J", "Q", "X", "Z"]
item_table = {l: ItemData(1000209000+n, ItemClassification.progression | ItemClassification.trap) if l in trap_letters 
              else ItemData(1000209000+n, ItemClassification.progression) for n,l in enumerate(letters)}

item_table["Extra turn"] = ItemData(1000208999, ItemClassification.progression)

possible_bonuses = ["Triple Word Value", "Triple Letter Value", "Double Word Value",  "Double Letter Value"]
bonus_locations = ["NW", "NE", "SW", "SE", "AP1", "AP2", "AP3", "AP4", "AP5", "AP6"]

bonus_item_list = []  # list of lists
id = 1000208000
for bl in bonus_locations:
    for pb in possible_bonuses:
        item_table[f"{pb} {bl}"] = ItemData(id, ItemClassification.progression)
        id += 1
    bonus_item_list.append([f"{pb} {bl}" for pb in possible_bonuses])  # add list

if(id >= 1000209000):
    exit("Oh boy there are too many bonuses and ids are screwed up...")

group_table: Dict[str, Set[str]] = {
    "Tiles": letters,
    "Bonuses": [item for sublist in bonus_item_list for item in sublist]
}