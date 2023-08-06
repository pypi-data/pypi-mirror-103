import logging
from argparse import ArgumentParser

from fintix_modelcurator.const import *
from fintix_modelcurator.exit_code import *
from fintix_modelcurator.trigger_type import *
from fintix_modelcurator.config import Config
from fintix_modelcurator.settings import Settings
from fintix_modelcurator.repository import ModelRepository
from fintix_modelcurator.error import FintixError
from fintix_modelcurator.utils import handle_error
from fintix_modelcurator.cbhandler import DataCallbackHandler


def init_logging():
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)

    return NoResult, NoError


def start():
    setting = Settings.getInstance().get_settings()
    model_name = setting.get('model')
    phase = setting.get('phase')
    input_topic = setting.get('input_topic')
    trigger_type = setting.get('trigger').get('type')
    trigger_interval = setting.get('trigger').get('interval')
    trigger_unit = setting.get('trigger').get('unit')
    stop_after_triggers = setting.get('stop_after')

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

    if trigger_type is None:
        error = FintixError(
            exception=None, message="input type was not defined",
            exit_code=INPUT_TYPE_NOT_DEFINED, should_exit=True)
        return NoResult, error

    if input_topic is None:
        error = FintixError(
            exception=None, message="input topic was not defined",
            exit_code=INPUT_TOPIC_NOT_DEFINED, should_exit=True)
        return NoResult, error

    if trigger_type not in [POINT_INTERVAL, TIME_INTERVAL]:
        error = FintixError(
            exception=None, message="invalid input type",
            exit_code=INVALID_INPUT_TYPE, should_exit=True)
        return NoResult, error

    model, error = ModelRepository.getInstance().import_model(model_name=model_name, phase=phase)
    if error is not NoError:
        return (
            NoResult, error
        )

    callback_handler = DataCallbackHandler.getInstance()
    callback_handler.init(
                        model=model,
                        model_name=model_name,
                        phase=phase,
                        input_topic=input_topic,
                        trigger_type=trigger_type,
                        trigger_interval=trigger_interval,
                        trigger_unit=trigger_unit,
                        stop_after_triggers=stop_after_triggers,
                    )

    res, error = callback_handler.start()

    return res, error


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

    _, error = init_logging()
    handle_error(error)

    _, error = start()
    handle_error(error)

    os._exit(OK)
