import logging
import subprocess
from zipimport import zipimporter
from urllib.parse import urlparse

import psycopg2
from psycopg2 import pool

from fintix_modelcurator.const import *
from fintix_modelcurator.exit_code import *
from fintix_modelcurator.phase import *
from fintix_modelcurator.config import Config
from fintix_modelcurator.error import FintixError


class ModelRepository:
    INSTANCE = None
    CONN_POOL_MIN = 1
    CONN_POOL_MAX = 5
    MODEL_REPO_TABLE = f"{DB_SCHEMA}.custom_model"

    def __init__(self):
        self.config = Config.getInstance()
        self.db_url = self.config.get(DB_URL_KEY)
        self.db_user = self.config.get(DB_USER_KEY)
        self.db_pwd = self.config.get(DB_PWD_KEY)

        url_parsed = urlparse(self.db_url.replace("jdbc:", ""))
        self.conpool = psycopg2.pool.ThreadedConnectionPool(
            minconn=self.CONN_POOL_MIN,
            maxconn=self.CONN_POOL_MAX,
            user=self.db_user,
            password=self.db_pwd,
            database=url_parsed.path[1:],
            host=url_parsed.hostname,
            port=url_parsed.port
        )

    def __download_model(self, model_name, phase):
        conn = None
        cur = None
        try:
            conn = self.conpool.getconn()
            cur = conn.cursor()
            if conn:
                cur.execute(f"SELECT model from %s where filename '%s'", (ModelRepository.MODEL_REPO_TABLE, model_name))
                blob = cur.fetchone()
                output_dir = LOCAL_TRAINING_MODEL_REPO if phase in [TRAINING_PHASE, EVALUATION_PHASE] else LOCAL_DEPLOY_MODEL_REPO
                output_file = os.path.join(output_dir, model_name + ".zip")
                with open(output_file, "wb") as modelzip:
                    modelzip.write(blob[0])
        except Exception as e:
            return (
                NoResult,
                FintixError(exception=e, message=f"could not download model {model_name} from model repository",
                            exit_code=MODEL_DOWNLOADING_ERROR, should_exit=True)
            )
        finally:
            if cur is not None:
                try:
                    cur.close()
                except:
                    pass
            if conn is not None:
                try:
                    self.conpool.putconn(conn)
                except:
                    pass
        return NoResult, NoError

    def __convert_model(self, model_name):
        try:
            res = subprocess.getoutput(f"jupyter nbconvert --to script {model_name}.ipynb")
            
        except Exception as e:



    def upload_model(self, model_name):
        res, err = self.__convert_model(model_name=model_name)


    def import_model(self, model_name, phase):
        if model_name is None or phase is None:
            return NoResult, FintixError(exception=None, message="failed to import model, model or phase could not be done")

        _, err = self.__download_model(model_name, phase)
        if err:
            return NoResult, err
        try:
            model = zipimporter(os.path.join(LOCAL_DEPLOY_MODEL_REPO, model_name + ".zip")).load_module(model_name)
        except Exception as e:
            return (
                NoResult,
                FintixError(
                    exception=e, message=f"failed to import model in {LOCAL_DEPLOY_MODEL_REPO}",
                    exit_code=MODEL_CODE_IMPORT_ERR, should_exit=True)
            )

        return model, NoError

    @classmethod
    def getInstance(cls):
        if cls.INSTANCE is None:
            cls.INSTANCE = ModelRepository()
        return cls.INSTANCE
