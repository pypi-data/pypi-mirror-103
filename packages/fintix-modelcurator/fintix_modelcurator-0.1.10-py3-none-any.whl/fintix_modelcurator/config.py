from configparser import ConfigParser

from fintix_modelcurator.const import *
from fintix_modelcurator.exit_code import *
from fintix_modelcurator.error import FintixError


class Config:
    INSTANCE = None
    CONFIG_DELIMITER = "/"
    SUPPORTED_FILE_EXT = [".properties"]

    def __init__(self):
        self.config = None
        self.initialized = False
        self.config_path = None

    def init(self, config_path):
        self.config_path = config_path
        if not any([self.config_path.endswith(ext) for ext in self.SUPPORTED_FILE_EXT]):
            return (
                NoResult,
                FintixError(
                    exception=Exception(
                        f"only the following config file format are supported: {', '.join(self.SUPPORTED_FILE_EXT)}"
                    ),
                    message="config initialization failed",
                    exit_code=CONFIG_INITIALIZATION_ERROR,
                    should_exit=True
                )
            )

        try:
            with open(self.config_path, 'r') as f:
                content = f.read()
                content = "[DEFAULT]" + os.linesep + content
                self.config = ConfigParser()
                self.config.read_string(content)
        except Exception as e:
            return (
                NoResult,
                FintixError(
                    exception=e,
                    message="config initialization failed",
                    exit_code=CONFIG_INITIALIZATION_ERROR,
                    should_exit=True
                )
            )

        self.initialized = True
        return NoResult, NoError

    def get(self, key_path):
        if self.config is None or not self.initialized:
            return (
                NoResult,
                FintixError(
                    exception=Exception("config have not been initialized"),
                    message="config have not been initialized yet",
                    exit_code=CONFIG_NOT_INITIALIZED,
                    should_exit=False
                )
            )

        if key_path is not None and len(key_path) > 0:
            keys = key_path.strip().split(Config.CONFIG_DELIMITER)
            current_configpath = ""
            current_config = self.config["DEFAULT"]
            for key in keys:
                current_configpath = key if len(current_config) == 0 else Config.CONFIG_DELIMITER.join(
                    (current_configpath, key))
                current_config = current_config.get(key)
                if current_config is None:
                    raise (
                        NoError,
                        FintixError(
                            exception=Exception(f"Could not found config for {key_path} because config already end at {current_configpath}"),
                            message=f"Could not found config for {key_path} because config already end at {current_configpath}",
                            exit_code=INVALID_CONFIG_PATH,
                            should_exit=False

                        )
                    )

            return current_config, NoError
        else:
            return (
                NoResult,
                FintixError(
                    exception=Exception("config key path could not be None or empty"),
                    message="config key path could not be None or empty",
                    exit_code=INVALID_CONFIG_PATH,
                    should_exit=False
                )
            )

    @classmethod
    def getInstance(cls):
        if cls.INSTANCE is None:
            cls.INSTANCE = Config()
        return cls.INSTANCE
