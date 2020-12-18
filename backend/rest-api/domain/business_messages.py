from enum import Enum
import json


class EnumConversibleToJson(str, Enum):
    def __str__(self):
        return self.value


class DefaultOperationsRejectionsMessages(EnumConversibleToJson):
    NEED_A_ID_TO_FIND: str = "Você precisa definir um ID para selecionar uma entidade válida"


class WorkCenterOperationsRejectionMessages(EnumConversibleToJson):
    INVALID_REGION_NAME: str = "Você precisa adicionar a região do centro para prosseguir com o cadastro"
    INVALID_DATA_TO_REGISTER: str = "Você não pode cadastrar um Polo sem adicionar os dados do mesmo"


class ExpeditionOperationsRejectionMessages(EnumConversibleToJson):
    WORK_CENTER_IS_REQUIRED: str = "Você deve selecionar um polo para poder enviar uma expedição"
    QTY_OF_TERMINALS_IS_REQUIRED: str = "Você precisa nos informar uma quantidade de terminais a serem enviados"
