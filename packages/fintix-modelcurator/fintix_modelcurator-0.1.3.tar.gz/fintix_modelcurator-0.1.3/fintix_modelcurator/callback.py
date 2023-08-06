import json
import logging

from tensorflow.keras.callbacks import Callback

from fintix_modelcurator.config import *
from confluent_kafka import Producer


class FintixCallback(Callback):
    def __init__(self, model_name):
        self.model_name = model_name
        self.config = Config.getInstance()
        self.kafka_settings = {
            'bootstrap.servers': '192.168.2.102:9092',
        }
        self.predict_output_topic = f"{model_name}_model_output"
        self.producer = Producer(self.kafka_settings)
        super(Callback, self).__init__()

    def on_data_delivered(self, err, msg):
        if err is not None:
            logging.error('Message delivery failed: {}'.format(err))
        else:
            logging.error('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

    def on_train_end(self, logs=None):
        self.producer.produce(
            f"_fintix_model_monitoring_{self.model_name}_train_end",
            json.dumps(logs).encode('utf-8'),
            self.on_data_delivered)
        self.producer.flush()
        logging.info(f"Stop training; got logs: {logs}")

    def on_train_batch_end(self, batch, logs=None):
        self.producer.produce(
            f"_fintix_model_monitoring_{self.model_name}_train_batch",
            json.dumps(logs).encode('utf-8'),
            self.on_data_delivered)
        self.producer.flush()
        logging.info(f"Training: end of batch {batch}; got logs {logs}")

    def on_epoch_end(self, epoch, logs=None):
        self.producer.produce(
            f"_fintix_model_monitoring_{self.model_name}_train_epoch",
            json.dumps(logs).encode('utf-8'),
            self.on_data_delivered)
        self.producer.flush()
        logging.info(f"End epoch {epoch} of training; got logs {logs}")

    def on_test_end(self, logs=None):
        self.producer.produce(
            f"_fintix_model_monitoring_{self.model_name}_test",
            json.dumps(logs).encode('utf-8'),
            self.on_data_delivered)
        self.producer.flush()
        logging.info(f"Stop testing; got logs {logs}")

    def on_test_batch_end(self, batch, logs=None):
        self.producer.produce(
            f"_fintix_model_monitoring_{self.model_name}_test_batch",
            json.dumps(logs).encode('utf-8'),
            self.on_data_delivered)
        self.producer.flush()
        logging.info(f"Evaluating: end of batch {batch}; got logs {logs}")

    def on_predict_end(self, logs=None):
        self.producer.produce(
            f"_fintix_model_monitoring_{self.model_name}_predict",
            json.dumps(logs).encode('utf-8'),
            self.on_data_delivered)
        self.producer.flush()
        logging.info(f"Stop predicting; got logs {logs}")

    def on_predict_batch_end(self, batch, logs=None):
        for data in logs["outputs"]:
            self.producer.produce(self.predict_output_topic, json.dumps(data).encode('utf-8'), self.on_data_delivered)
            self.producer.flush()
        logging.info(f"Predicting: end of batch {batch}; got logs {logs}")
