from utils.json import EnumConversibleToJson

class DefaultOperationsRejectionsMessages(EnumConversibleToJson):
    NEED_A_ID_TO_FIND: str = "Você precisa definir um ID para selecionar uma entidade válida"


class WorkCenterOperationsRejectionMessages(EnumConversibleToJson):
    INVALID_REGION_NAME: str = "Você precisa adicionar a região do centro para prosseguir com o cadastro"
    INVALID_DATA_TO_REGISTER: str = "Você não pode cadastrar um Polo sem adicionar os dados do mesmo"


class ExpeditionOperationsRejectionMessages(EnumConversibleToJson):
    WORK_CENTER_IS_REQUIRED: str = "Você deve selecionar um polo para poder enviar uma expedição"
    QTY_OF_TERMINALS_IS_REQUIRED: str = "Você precisa nos informar uma quantidade de terminais a serem enviados"

class AttendanceOperationsRejectionMessages(EnumConversibleToJson):
    WORK_CENTER_IS_REQUIRED: str = "Você deve selecionar um polo para pedir um atendimento"
    QTY_OF_TERMINALS_IS_REQUIRED: str = "Você precisa nos informar uma quantidade de terminais que serão usados durante o atendimento"
    ATTENDANCE_DATE_IS_REQUIRED: str = "Você precisa nos informar a data que realizará o atendimento"
    ATTENDANCE_DATE_IS_INVALID: str = "Você precisa nos informar uma data de atendimento valida"
