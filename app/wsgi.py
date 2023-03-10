from api import api
import os

import utils
logger = utils.get_logger(__name__, loglevel='DEBUG')

# --------- For local debugging/test only ----------
from wsgiref.simple_server import make_server

if __name__ == "__main__":

    app_port = os.getenv('MODEL_PORT', default=8007)

    with make_server("", int(app_port), api) as httpd:
        logger.debug(f"Listening Port {app_port}...")
        # Serve until process is killed
        httpd.serve_forever()
# --------- For local debugging/test only ----------

