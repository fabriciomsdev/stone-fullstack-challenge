from business.rules import WorkCenterBusinessRules
import falcon
from business.domain.entities import WorkCentersEntity
from business.messages import WorkCenterOperationsRejectionMessages

def verify_if_is_a_valid_work_center_to_register(req, resp, resource, params):
    if req.media is None or WorkCenterBusinessRules().is_not_a_valid_work_center_data_to_register(WorkCentersEntity(**req.media)):
        raise falcon.HTTPBadRequest("Bad Request", WorkCenterOperationsRejectionMessages.INVALID_REGION_NAME)
