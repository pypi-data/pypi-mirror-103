import os
import time
import logging

from fintix_modelcurator.const import *
from fintix_modelcurator.repository import ModelRepository


def get_currenttime_ms():
    return time.time() // 1_000_000


def handle_error(error, logger=None):
    if logger is None:
        logger = logging

    if error is not None:
        message = "[Unknown message]" if error.getMessage() is None else error.getMessage()
        exception = error.getException()
        exit_code = error.getExitCode()
        shouldExit = error.shouldExit()

        if exception is not None:
            logger.error(message, exception)
        else:
            logger.error(message)

        if shouldExit:
            os._exit(exit_code)


def upload_model(model_name):
    res, err = ModelRepository.getInstance().upload_model(model_name)
    if err is None:
        logging.info(res)
    else:
        handle_error(err)


def get_model_save_path(model_name):
    return os.path.join(LOCAL_DEPLOY_MODEL_REPO, model_name)
