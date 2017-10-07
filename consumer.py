import json
import os

from kafka import KafkaConsumer
import kafka_helper


def get_consumer(topic):
    consumer = kafka_helper.get_kafka_consumer(
        os.environ.get('KAFKA_PREFIX', '') + topic)
    return consumer


def get_alltime_consumer(topic):
    all_time_consumer = KafkaConsumer(
        os.environ.get('KAFKA_PREFIX', '') + topic,
        bootstrap_servers=kafka_helper.get_kafka_brokers(),
        security_protocol='SSL',
        ssl_context=kafka_helper.get_kafka_ssl_context(),
        value_deserializer=lambda v: json.loads(v.decode('utf-8')),
        enable_auto_commit=False,
        auto_offset_reset='earliest'
    )
    return all_time_consumer

