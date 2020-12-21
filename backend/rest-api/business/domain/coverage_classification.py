from enum import Enum
from utils.json import EnumConversibleToJson

class CoverageClassifications(EnumConversibleToJson):
    RED = "Vermelha"
    GREEN = "Verde"
    YELLOW = "Amarela"
