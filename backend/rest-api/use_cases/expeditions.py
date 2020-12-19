from data.repositories import ExpeditionsRepository, WorkCentersRepository
from data.data_source import DBDataSource
from domain.entities import ExpeditionsEntity, WorkCentersEntity
from domain.business_rules import WorkCenterBusinessRules
from domain.business_messages import ExpeditionOperationsRejectionMessages, DefaultOperationsRejectionsMessages
from utils.exceptions import UseCaseException


class ExpeditionsUseCases():
    _expeditions_repository = None
    _business_rules = None
    _data_source = DBDataSource()

    def __init__(self):
        self._expeditions_repository: ExpeditionsRepository = ExpeditionsRepository(
            db_data_source=self._data_source)
        self._work_center_repository: WorkCentersRepository = WorkCentersRepository(
            db_data_source=self._data_source)
        self._business_rules: WorkCenterBusinessRules = WorkCenterBusinessRules()

    def _predict_qty_of_terminals_needed(self, expedition: ExpeditionsEntity = ExpeditionsEntity()) -> ExpeditionsEntity:
        wc : WorkCentersEntity = self._work_center_repository.find(expedition.work_center.id)
        wc.calcule_qty_of_terminals_available()
        
        avg_of_consume_in_wc = self._work_center_repository.get_average_of_attendence_by_days_period(
            expedition.work_center, wc.days_qty_ideal_for_coverage)

        if avg_of_consume_in_wc != 0:
            expedition.qty_of_terminals = self._business_rules.get_right_qty_to_cover_the_demand_by_days(
                wc.days_qty_ideal_for_coverage, avg_of_consume_in_wc, wc.qty_of_terminals_available)
        return expedition


    def create(self, expedition: ExpeditionsEntity = ExpeditionsEntity()) -> ExpeditionsEntity:
        if expedition.work_center == None:
            raise UseCaseException(
                ExpeditionOperationsRejectionMessages.WORK_CENTER_IS_REQUIRED)

        if (expedition.auto_predict_qty_needed is False
            and (expedition.qty_of_terminals == None or expedition.qty_of_terminals == 0)):
            raise UseCaseException(
                ExpeditionOperationsRejectionMessages.QTY_OF_TERMINALS_IS_REQUIRED)

        try:
            if (expedition.auto_predict_qty_needed):
                expedition = self._predict_qty_of_terminals_needed(
                    expedition)

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
