from typing import Callable, ClassVar

from item_data import Item
from loadout import Loadout

AreaLogicType = dict[str, dict[tuple[str, str], Callable[[Loadout], bool]]]
LocationLogicType = dict[str, Callable[[Loadout], bool]]


class LogicInterface:
    """ a static class with the 2 logic dictionaries"""

    area_logic: ClassVar[AreaLogicType]
    """
    {
        area_name: {
            (area_door_name_origin, area_door_name_destination):
                (loadout) -> can_traverse
        }
    }
    """

    location_logic: ClassVar[LocationLogicType]
    """
    {
        location_name:
            (loadout) -> can_access
    }
    """

    hard_required_items: ClassVar[list[Item]]
    """
    a list of the items that the game can't ever be beaten without (using this logic)

    A unit test will verify that this list is correct.
    """

    @staticmethod
    def can_fall_from_spaceport(loadout: Loadout) -> bool:
        """ returns whether I can leave spaceport by Ridley free-fall """
        raise NotImplementedError("can_fall_from_spaceport")

    @staticmethod
    def can_crash_spaceport(loadout: Loadout) -> bool:
        """ returns whether I can crash the spaceport with this loadout """
        raise NotImplementedError("can_fall_from_spaceport")

    @staticmethod
    def can_win(loadout: Loadout) -> bool:
        """
        returns whether I can detonate Daphne and get back to the ship

        this should call `_can_crash_spaceport`

        this should NOT reference `hard_required_items` (because unit tests will use this to test it)
        """
        raise NotImplementedError("can_fall_from_spaceport")
