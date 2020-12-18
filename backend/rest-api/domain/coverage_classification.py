from enum import Enum
import json
from utils.json import EnumConversibleToJson


class CoverageClassifications(EnumConversibleToJson):
    RED: str = "Vermelha"
    GREEN: str = "Verde"
    YELLOW: str = "Amarela"
