from confluent_kafka import Consumer, Producer, KafkaError, KafkaException

from fintix_modelcurator.config import Config


class KafkaHandler:
    INSTANCE = None

    def __init__(self):
        self.config = None
        self.kafka_settings = None
        self.consumer = None
        self.producer = None

    def init(self):
        self.config = Config.getInstance()
        self.kafka_settings = {
            'bootstrap.servers': '192.168.2.102:9092',
            'group.id': 'mygroup',
            'client.id': 'client-1',
            'enable.auto.commit': True,
            'session.timeout.ms': 6000,
            'default.topic.config': {
                'auto.offset.reset': 'smallest'
            }
        }
        self.consumer = Consumer(self.kafka_settings)
        self.producer = Producer(self.kafka_settings)

    def get(self):
        try:
            consumer.subscribe([input_topic])
            while True:
                msg = consumer.poll(timeout=1.0)
                if msg is None:
                    continue

                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        sys.stderr.write(
                            '%% %s [%d] reached end at offset %d\n' % (msg.topic(), msg.partition(), msg.offset()))
                    elif msg.error():
                        raise KafkaException(msg.error())
                else:
                    raw_message = tf.constant(msg.value())
                    raw_key = tf.constant(msg.key())
                    x, y = decode_kafka_online_item(raw_message, raw_key, input_shape)
                    x = tf.data.Dataset.from_tensors(x)
                    print(x)
                    res = model.predict(x)
                    print(str(res))
                    consumer.commit(msg)
        finally:
            # Close down consumer to commit final offsets.
            consumer.close()

    @classmethod
    def getInstance(cls):
        if cls.INSTANCE is None:
            cls.INSTANCE = KafkaHandler()
        return cls.INSTANCE
