from enum import Enum
import json

class WorkCenterOperationsRejectionMessages(str, Enum):
    INVALID_REGION_NAME: str = "Você precisa adicionar a região do centro para prosseguir com o cadastro"
    INVALID_DATA_TO_REGISTER: str = "Você não pode cadastrar um Polo sem adicionar os dados do mesmo"
    NEED_A_ID_TO_FIND: str = "Você precisa definir um ID para selecionar um Polo"
    
    def __str__(self):
        return self.value
