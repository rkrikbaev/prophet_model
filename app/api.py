import falcon
import sys

from model import Model
from utils import get_logger, LOG_LEVEL, TRACKING_SERVER

logger = get_logger(__name__, loglevel=LOG_LEVEL)


class Health():
    def on_get(self, req, resp):
        resp.media = "ok"


class Action:
    def __init__(self) -> None:
        self.model = Model()

    def on_post(self, req, resp):

        request = req.media
        logger.debug(request)
        logger.debug(f'Request from the operator: {list(request.keys())}')

        resp.status = falcon.HTTP_200

        response = {
            "model_status": resp.status,
            "result": None,
            "model_uri": None,
            "anomalies": None
            }

        config = request.get('model_config')
        data = request.get('dataset')
        model_uri = request.get('model_uri')
        period = request.get('period')

        result = self.model.run(data, config, period)

        response["result"] = result
        response["model_uri"] = model_uri
        response["anomalies"] = None

        logger.debug(f'Model response: {response}')

        resp.media = response

api = falcon.App()

api.add_route("/health", Health())
api.add_route("/action", Action())

logger.info("Service started")
