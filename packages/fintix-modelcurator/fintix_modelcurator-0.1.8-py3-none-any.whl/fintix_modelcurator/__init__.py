import os
import sys
import logging

from fintix_modelcurator.callback import FintixCallback
from fintix_modelcurator.utils import get_model_save_path, upload_model
from fintix_modelcurator.config import Config
from fintix_modelcurator.const import *

__all__ = ['FintixCallback', 'get_model_save_path', 'upload_model']


def __init_logging():
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)


def __init_config():
    config_file = os.path.join(FINTIX_HOME_DIR, "application.properties")
    Config.getInstance().init(config_file)


__init_logging()
__init_config()
