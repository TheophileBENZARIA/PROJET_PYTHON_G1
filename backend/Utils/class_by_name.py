from backend.Class.Generals.CaptainBraindead import CaptainBraindead
from backend.Class.Generals.GeneralClever import GeneralClever
from backend.Class.Generals.MajorDaft import MajorDaft
from backend.Class.Units.Crossbowman import Crossbowman
from backend.Class.Units.Knight import Knight
from backend.Class.Units.Pikeman import Pikeman


@staticmethod
def general_from_name(name: str) :
        GENERAL_REGISTRY: dict[str, type] = {
            "CaptainBraindead": CaptainBraindead,
            "MajorDaft": MajorDaft,
            "GeneralClever": GeneralClever,
        }

        return GENERAL_REGISTRY.get(name, CaptainBraindead)


@staticmethod
def unit_from_name(name: str):
    UNIT_CLASSES = {
        "knight": Knight,
        "pikeman": Pikeman,
        "crossbowman": Crossbowman,
        }

    return UNIT_CLASSES.get(name)