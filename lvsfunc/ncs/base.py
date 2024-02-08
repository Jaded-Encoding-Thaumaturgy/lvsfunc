from __future__ import annotations

from enum import Enum
from pathlib import Path
from typing import Any, Type, TypeVar

from stgpytools import (CustomKeyError, CustomTypeError, CustomValueError,
                        FuncExceptT, SPath, SPathLike)

__all__: list[str] = [
    "BaseNcEnum", "NCs",
]


class BaseNcEnum(Enum):
    """
    A base enum representing all the NCs of this show.
    This class is supposed to be inherited and extended
    to include all the possible NCOP/NCEDs of a show.

    Example using Cardcaptor Sakura's NCs:

    .. code-block:: python

        >>>class CardcaptorSakuraNCs(BaseNcEnum):
        >>>    NCOP1v1 = "BDMV/Cardcaptor Sakura Blu-ray BOX/CC_SAKURA_BD_BOX_DISC7/BDMV/STREAM/00004.m2ts"
        >>>    NCOP1v2 = "BDMV/Cardcaptor Sakura Blu-ray BOX/CC_SAKURA_BD_BOX_DISC7/BDMV/STREAM/00005.m2ts"
        >>>    NCOP2 = "BDMV/Cardcaptor Sakura Blu-ray BOX/CC_SAKURA_BD_BOX_DISC7/BDMV/STREAM/00006.m2ts"
        >>>    NCOP3 = "BDMV/Cardcaptor Sakura Blu-ray BOX/CC_SAKURA_BD_BOX_DISC11/BDMV/STREAM/00003.m2ts"
        >>>    NCED1 = "BDMV/Cardcaptor Sakura Blu-ray BOX/CC_SAKURA_BD_BOX_DISC7/BDMV/STREAM/00011.m2ts"
        >>>    NCED2 = "BDMV/Cardcaptor Sakura Blu-ray BOX/CC_SAKURA_BD_BOX_DISC7/BDMV/STREAM/00012.m2ts"
        >>>    NCED3 = "BDMV/Cardcaptor Sakura Blu-ray BOX/CC_SAKURA_BD_BOX_DISC11/BDMV/STREAM/00004.m2ts"

    You should then also create a mapping of episode ranges and NCs.
    This base class comes with a NONE for cases where an episode has no NCOP/NCED.

    These methods always expect there to be two values, so even for anime
    with only an ED, you should still set `YourNcEnum.NONE` for the OP.
    OVAs, movies, etc. should all have their separate entries, even if they share NCs.

    Example using the previous Cardcaptor Sakura NCs class:

    .. code-block:: python

        >>> nc_map: dict[tuple[int, int], tuple[CardcaptorSakuraNCs, CardcaptorSakuraNCs]] = {
        >>>     (1, 8): (CardcaptorSakuraNCs.NCOP1v1, CardcaptorSakuraNCs.NCED1),
        >>>     (9, 35): (CardcaptorSakuraNCs.NCOP1v2, CardcaptorSakuraNCs.NCED1),
        >>>     (36, 45): (CardcaptorSakuraNCs.NCOP2, CardcaptorSakuraNCs.NCED2),
        >>>     (46, 46): (CardcaptorSakuraNCs.NCOP2, CardcaptorSakuraNCs.NONE),
        >>>     (47, 69): (CardcaptorSakuraNCs.NCOP3, CardcaptorSakuraNCs.NCED3),
        >>>     (70, 70): (CardcaptorSakuraNCs.NCOP3, CardcaptorSakuraNCs.NONE)
        >>> }

    Now we can get the OP/EDs that were played in a specific episode
    using either the `from_epnum` or `from_filename` methods.

    Examples:

    .. code-block:: python

        # Getting the NCs from the episode number
        >>> ncop, nced = CardcaptorSakuraNCs.from_epnum(70, nc_map)
        (<NcEnum.NCOP3: SPath('BDMV/Cardcaptor Sakura Blu-ray BOX/CC_SAKURA_BD_BOX_DISC11/BDMV/STREAM/00003.m2ts')>,
         <NcEnum.NCED3: SPath('BDMV/Cardcaptor Sakura Blu-ray BOX/CC_SAKURA_BD_BOX_DISC11/BDMV/STREAM/00004.m2ts')>)

        # Getting the NCs from the filename. This assumes the filename is split up with _'s.
        >>> ncop, nced = CardcaptorSakuraNCs.from_filename("CCSBD_16.py", nc_map)
        (<NcEnum.NCOP1v2: SPath('BDMV/Cardcaptor Sakura Blu-ray BOX/CC_SAKURA_BD_BOX_DISC7/BDMV/STREAM/00005.m2ts')>,
         <NcEnum.NCED1: SPath('BDMV/Cardcaptor Sakura Blu-ray BOX/CC_SAKURA_BD_BOX_DISC7/BDMV/STREAM/00011.m2ts')>)
    """

    NONE = None
    """Represents no NC for the OP/ED in a given episode."""

    def __new__(cls: Type[NCs], value: Any) -> NCs:
        """Forcibly override the value to be an SPath."""

        if not isinstance(value, (str, Path, SPath)):
            raise CustomValueError(f"Your enum value MUST be an \"SPathLike\" ({SPathLike})!", cls, type(value))

        value = SPath(value)

        instance = object.__new__(cls)
        instance._value_ = value

        return instance

    @classmethod
    def from_epnum(
        cls: Type[NCs],
        episode_number: Any,
        nc_map: dict[tuple[int, int], tuple[NCs, NCs]],
        func_except: FuncExceptT | None = None
    ) -> tuple[NCs, NCs]:
        """
        Get a tuple of NcEnum's from an episode number.

        See the BaseNcEnum class docstring for examples of expected values.

        :param episode_number:      The episode number, preferably as an int or string.
                                    Having "NC" in the title will ALWAYS return (NCs.None, NCs.None)!
                                    If this value can not be found in the given map, an error will be thrown.
        :param nc_map:              A mapping of all the NCs and their episode ranges.
                                    See the BaseNcEnum class docstring for examples.
        :param func_except:         Function returned for custom error handling.
                                    This should only be set by VS package developers.

        :return:                    A tuple of the matching NCs based on the map.
        """

        func = func_except or cls.from_epnum

        if isinstance(episode_number, str):
            if "NC" in episode_number:
                return (cls.NONE, cls.NONE)  # type:ignore[return-value]

        for ranges, nc_value in nc_map.items():
            if not isinstance(ranges, tuple):
                raise CustomTypeError("Your episode ranges must be a tuple of values!", func, ranges)
            elif len(ranges) != 2:
                raise CustomValueError(f"Your episode ranges must contain two values, not {len(ranges)}!", func)

            first, last = ranges

            if type(first) is not type(last):
                raise CustomTypeError(f"Your values must be of the same type!", func, (type(x) for x in ranges))

            if isinstance(episode_number, int):
                result = cls.__get_ncs_from_int(episode_number, first, last, nc_value, func)
            else:
                result = cls.__get_ncs_from_any(episode_number, first, last, nc_value)

            if result is not None:
                return result

        raise CustomKeyError(f"Could not find matching NCs for \"{episode_number}\"!", func)

    @staticmethod
    def __get_ncs_from_any(
        episode_number: Any, first: Any, last: Any, value: tuple[NCs, NCs]
    ) -> tuple[NCs, NCs] | None:
        if not all(type(x) == type(episode_number) for x in (first, last)):
            return None

        if any(episode_number == x for x in (first, last)):
            return value

        return None

    @staticmethod
    def __get_ncs_from_int(
        episode_number: int, first: int, last: int,
        value: tuple[NCs, NCs], func: FuncExceptT
    ) -> tuple[NCs, NCs] | None:
        if first > last:
            raise CustomValueError(f"Last ({last}) may not be greater than first ({first})!", func)

        if first <= episode_number <= last:
            return value

        return None


NCs = TypeVar("NCs", bound=BaseNcEnum)


FirstEpisode = int
"""The first episode the NC aired in."""

LastEpisode = int
"""The last episode the NC aired in. If it only played in one episode, this should match the FirstEpisode."""
