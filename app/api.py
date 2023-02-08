import falcon
import sys

from model import Model
from utils import get_logger, LOG_LEVEL

logger = get_logger(__name__, loglevel=LOG_LEVEL)


class Health():
    def on_get(self, req, resp):
        resp.media = "ok"


class Action:
    def __init__(self) -> None:
        self.model = Model()

    def on_post(self, req, resp):

        request = req.media
        logger.debug(f'Request from the operator: {list(request.keys())}')

        resp.status = falcon.HTTP_200

        response = {
            "model_status": resp.status,
            "prediction": None,
            "model_uri": None,
            "anomalies": None,
            "model_uri": None
            }

        required_fields = {'model_config', 'dataset', 'model_uri', 'metadata', 'period'}
        keys = set(request.keys())

        try:

            if required_fields == keys:

                config = request.get('model_config')

                data = request.get('dataset')
                period = request.get('period')
                model_uri = request.get('model_uri')

                result = self.model.run(data, period, config)

                response["prediction"] = result
                response["model_uri"] = model_uri
                response["anomalies"] = None

            logger.debug(f'Model response: {response}')

        except Exception as exc:

            response['model_status'] = falcon.HTTP_500
            logger.debug(f'Service error: {exc}')

        finally:
            resp.media = response

api = falcon.App()

api.add_route("/health", Health())
api.add_route("/action", Action())

logger.info("Service started")
