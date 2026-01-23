from dataclasses import dataclass
from typing import Tuple, Union

@dataclass(frozen=True)
class Action:
    unit: object                 # unité qui agit
    kind: str                    # "attack" | "move"
    target: Union[object, Tuple[float, float]]