from typing import Callable, ClassVar

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

    @staticmethod
    def can_fall_from_spaceport(loadout: Loadout) -> bool:
        """ returns whether I can leave spaceport by Ridley free-fall """
        raise NotImplementedError("can_fall_from_spaceport")
