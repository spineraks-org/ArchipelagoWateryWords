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
item_table = {l: ItemData(1000209000+n, ItemClassification.progression) for n,l in enumerate(letters)}
item_table["Extra turn"] = ItemData(1000208000, ItemClassification.progression)

group_table: Dict[str, Set[str]] = {
    "Tiles": letters
}