from backend.Class.Generals.CaptainBraindead import CaptainBraindead
from backend.Class.Generals.ColonelArchBtw import ColonelArchBtw
from backend.Class.Generals.GeneralClever import GeneralClever
from backend.Class.Generals.MajorDaft import MajorDaft
from backend.Class.Units.Crossbowman import Crossbowman
from backend.Class.Units.Knight import Knight
from backend.Class.Units.Pikeman import Pikeman

GENERAL_REGISTRY: dict[str, type] = {
            "CaptainBraindead": CaptainBraindead,
            "MajorDaft": MajorDaft,
            "GeneralClever": GeneralClever,
            "ColonelArchBtw": ColonelArchBtw,
        }

@staticmethod
def general_from_name(name: str) :
        return GENERAL_REGISTRY.get(name, CaptainBraindead)

@staticmethod
def get_available_generals() :
    return GENERAL_REGISTRY.keys()


UNIT_CLASSES = {
        "knight": Knight,
        "pikeman": Pikeman,
        "crossbowman": Crossbowman,
        }

@staticmethod
def unit_from_name(name: str):
    return UNIT_CLASSES.get(name)

@staticmethod
def get_available_unit() :
    return UNIT_CLASSES.keys()