@staticmethod
def unit_from_name(name: str):
    UNIT_CLASSES = {
        "knight": Knight,
        "pikeman": Pikeman,
        "crossbowman": Crossbowman,
        }

    return UNIT_CLASSES.get(name)