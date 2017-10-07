"""
Alert schema should be:
{
    "alert_type": "whatever",
    "alert_message": "whatever",
    "triggered_by": message.value // must be json serializable
}
"""
import consumer
import producer


class AlertService(object):
    alert_type = "generic"
    print_msgs = True

    def __init__(self, monitor_topic, alert_topic):
        self.monitor_topic = monitor_topic
        self.alert_topic = alert_topic
        self.consumer = consumer.get_consumer(topic=self.monitor_topic)

    def process_message(self, message):
        # either emit an alert or do nothing
        pass

    def get_alert_message(self, message):
        raise NotImplemented("Oops, you need to define an alert message handler")

    def emit_alert(self, message):
        alert_msg = self.get_alert_message(message)
        payload = {
            "alert_type": self.alert_type,
            "alert_message": alert_msg,
            "triggered_by": message.value
        }
        if self.print_msgs:
            print("emiting alert:")
            print(alert_msg)
        return producer.send_msg(topic=self.alert_topic, key='', value=payload) # don't like key = '' :(

    def monitor(self, print_msgs=True):
        self.print_msgs = print_msgs
        for msg in self.consumer:
            self.process_message(msg)


class ThrottlingAlertService(AlertService):
    alert_type = "throttled"
    limit = 100 # 100 items per minute
    duration = 60

    def __init__(self, *args, **kwargs):
        super(ThrottlingAlertService, self).__init__(*args, **kwargs)
        self.user_msg_lists = {
            "andy": [] # temp for now; update to build dynamically
        }

    def process_message(self, message):
        try:
            contents = message.value['contents']
            sender = message.value['sender']
        except KeyError:
            print("malformed message")
            print(message.value)
            return
        self.user_msg_lists[sender].append(message.timestamp)
        if len(self.user_msg_lists[sender]) > self.limit:
            self.emit_alert(message)
        # remove items older than duration
        while (message.timestamp - self.user_msg_lists[sender][0]
                > self.duration * 1000): # kafka timestamps are in ms
            self.user_msg_lists[sender].pop(0)

    def get_alert_message(self, message):
        num_messages = len(self.user_msg_lists[message.value['sender']])
        msg = "Whoa, we got {num} messages in the past {duration} seconds,"\
            " {sender} might be a bot".format(
                num=num_messages,
                duration=self.duration,
                sender=message.value['sender'])
        return msg


class OffensiveContentAlertService(AlertService):
    alert_type = "foulmouth_detected"

    def __init__(self, offensive_content_list, *args, **kwargs):
        self.offensive_content_list = offensive_content_list
        super(OffensiveContentAlertService, self).__init__(*args, **kwargs)

    def process_message(self, message):
        try:
            contents = message.value['contents']
            sender = message.value['sender']
        except KeyError:
            print("malformed message")
            print(message.value)
            return
        if any([offensive in contents.lower()
                for offensive in self.offensive_content_list]):
            self.emit_alert(message)

    def get_alert_message(self, message):
        safe_message = message.value['contents'][0] + "@!$"
        return "{sender} said {contents}".format(sender=message.value['sender'],
            contents=safe_message)
