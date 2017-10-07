import os

import kafka_helper


producer = kafka_helper.get_kafka_producer()

def send_msg(topic, value, key=None):
    msg = producer.send(
        os.environ.get('KAFKA_PREFIX', '') + topic,
        key=bytes(key, encoding='utf-8'),
        value=value)
    return msg
