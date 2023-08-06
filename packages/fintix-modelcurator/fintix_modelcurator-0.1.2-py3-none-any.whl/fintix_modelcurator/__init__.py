import sys
import logging

from fintix_modelcurator.callback import FintixCallback
from fintix_modelcurator.utils import get_model_save_path

__all__ = ['FintixCallback', 'get_model_save_path']


def init_logging():
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)


init_logging()
