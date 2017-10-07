import os
import random
import time

import producer


class MsgSimulator(object):
    """
    Usage:
    MsgSimulator(topic='human-messages', key='red').simulate()
    """

    def __init__(self, topic, key, delay=1):
        self.topic = topic
        self.key = key
        self.delay=delay # seconds

    def get_delay(self):
        """
        Override me if you want to control the delay
        """
        return self.delay

    def simulate(self, print_msg=True):
        while 1:
            value = self.get_value()
            producer.send_msg(
                topic=self.topic,
                value=value,
                key=self.key
            )
            if print_msg:
                print("sending msg:")
                print(value)
            time.sleep(self.get_delay())

    def get_user(self):
        return os.environ.get('USER')

    def get_message(self):
        return "blergface"

    def get_value(self):
        return {
            "sender": self.get_user(),
            "contents": self.get_message()
        }


class MsgChoiceSimulator(MsgSimulator):
    def __init__(self, msg_choices, *args, **kwargs):
        self.msg_choices = msg_choices
        super(MsgChoiceSimulator, self).__init__(*args, **kwargs)

    def get_message(self):
        return random.choice(self.msg_choices)


class NonsenseSimulator(MsgSimulator):
    phrases = [
        "The person you were before is like a summer breeze.",
        "That way likes to have a shower in the morning.",
        "The clear star that is yesterday is not yet ready to die.",
        "That memory shared lies ahead, with the future yet to come.",
    ]

    def get_message(self):
        return random.choice(self.phrases)
