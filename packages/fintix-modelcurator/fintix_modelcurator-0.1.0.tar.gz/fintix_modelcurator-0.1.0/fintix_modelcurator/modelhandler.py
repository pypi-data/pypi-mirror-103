import os
import sys
import logging
from zipimport import zipimporter
from argparse import ArgumentParser

from fintix_modelcurator.const import *
from fintix_modelcurator.exit_code import *
from fintix_modelcurator.input_type import *
from fintix_modelcurator.config import Config
from fintix_modelcurator.settings import Settings
from fintix_modelcurator.repository import ModelRepository
from fintix_modelcurator.error import FintixError
from fintix_modelcurator.utils import handle_error
from fintix_modelcurator.kafkahandler import KafkaHandler


def start():
    setting = Settings.getInstance().get_settings()
    model_name = setting.get('model')
    phase = setting.get('phase')
    input_type = setting.get('input_type')

    if model_name is None:
        error = FintixError(
            exception=None, message="model name was not defined",
            exit_code=MODEL_NOT_DEFINED, should_exit=True)
        return NoResult, error

    if phase is None:
        error = FintixError(
            exception=None, message="phase was not defined",
            exit_code=PHASE_NOT_DEFINED, should_exit=True)
        return NoResult, error

    if input_type is None:
        error = FintixError(
            exception=None, message="input type was not defined",
            exit_code=INPUT_TYPE_NOT_DEFINED, should_exit=True)
        return NoResult, error

    if input_type not in [SINGLE_POINT, TIME_WINDOW, POINT_WINDOW]:
        error = FintixError(
            exception=None, message="invalid input type",
            exit_code=INVALID_INPUT_TYPE, should_exit=True)
        return NoResult, error

    model_repo = ModelRepository.getInstance()

    KafkaHandler.getInstance().init()

    model, error = ModelRepository.getInstance().import_model(model_name=model_name, phase=phase)
    handle_error(error)




    return NoResult, NoError


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-c", "--config", help="specified config file", required=True)
    parser.add_argument("-s", "--settings", help="specified settings for data as json string", required=True)
    args = None
    if len(sys.argv[1:]) == 0:
        parser.print_help()
        sys.exit(0)
    else:
        args = parser.parse_args(sys.argv[1:])

    _, error = Config.getInstance().init(args.config)
    handle_error(error)

    _, error = Settings.getInstance().init(args.settings)
    handle_error(error)

    _, error = start()
    handle_error(error)

    os._exit(OK)
