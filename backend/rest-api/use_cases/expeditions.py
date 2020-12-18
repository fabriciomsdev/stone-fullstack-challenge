from data.repositories import ExpeditionsRepository
from data.data_source import DBDataSource
from domain.entities import ExpeditionsEntity
from domain.business_rules import WorkCenterBusinessRules
from domain.business_messages import ExpeditionOperationsRejectionMessages, DefaultOperationsRejectionsMessages
from utils.exceptions import UseCaseException


class ExpeditionsUseCases():
    _expeditions_repository = None
    _business_rules = None

    def __init__(self):
        self._expeditions_repository = ExpeditionsRepository(db_data_source=DBDataSource())
        self._business_rules = WorkCenterBusinessRules()

    def create(self, expedition: ExpeditionsEntity = ExpeditionsEntity()) -> ExpeditionsEntity:
        if expedition.work_center == None:
            raise UseCaseException(
                ExpeditionOperationsRejectionMessages.WORK_CENTER_IS_REQUIRED)

        if expedition.qty_of_terminals == None or expedition.qty_of_terminals == 0:
            raise UseCaseException(
                ExpeditionOperationsRejectionMessages.QTY_OF_TERMINALS_IS_REQUIRED)

        try:
            model_created = self._expeditions_repository.persist(expedition)
            self._expeditions_repository.save_transaction()
        except Exception as ex:
            self._expeditions_repository.revert_transaction()
            raise ex

        return model_created.to_entity()

    def get_all(self) -> list:
        return [model.to_entity() for model in self._expeditions_repository.fetch()]

    def find(self, primary_key: int) -> ExpeditionsEntity:
        if primary_key == None or primary_key == 0:
            raise UseCaseException(
                DefaultOperationsRejectionsMessages.NEED_A_ID_TO_FIND)

        return self._expeditions_repository.find(primary_key)

    def cancel_expedition(self, entity: ExpeditionsEntity) -> ExpeditionsEntity:
        entity.was_canceled = True
        return self.update(entity)

    def update(self, entity: ExpeditionsEntity) -> ExpeditionsEntity:
        try:
            model_updated = self._expeditions_repository.update(entity)
            self._expeditions_repository.save_transaction()
            return model_updated.to_entity()
        except Exception as ex:
            self._expeditions_repository.revert_transaction()
            raise ex

    def delete(self, entity: ExpeditionsEntity) -> bool:
        try:
            self._expeditions_repository.delete(entity)
            self._expeditions_repository.save_transaction()
        except Exception as ex:
            self._expeditions_repository.revert_transaction()
            raise ex
