# Let's take Kafka for a test drive

We'll build a messaging application together.

## Setup
1. git clone this repo
2. `mkvirtualenv kafka_testing -p python3`
3. `setvirtualenvproject $VIRTUAL_ENV .`
4. `pip install -r requirements.txt`
5. get a copy of the .env file and put it in the root dir for this project
6. `echo "source .env" >> $VIRTUAL_ENV/bin/postactivate`

Ready to rock!

## Start using Kafka
1. Start sending message to Kafka:
```
from producer import send_msg
promise = send_msg(topic='human-messages', key='red', value={'some': 'dict'})
promise.succeeded()
```
Why was it `False`?
Try again:
```
promise.succeeded()
```
Now it's `True` - bc msgs are sent asychronously by the producer (unless you tell it to block for a response).

2. Now let's consume some messages. Do this in a new python session so you can send from one to the other.
```
import consumer
c = consumer.get_consumer('human-messages')
for msg in c:
    print(msg)
```
Note the pleasantly pythonic iterator syntax for consumers.  Suh-weet.

Go ahead and send some messages from the producers, and watch the consumer consume them.

3.  Let's define a bit of structure for messages in `human-messages`.  Henceforth the schema shall be:
```
{
    "sender": "sender name",
    "contents": "words words words"
}
```

Cool, now we can consume messages in a slightly prettier way because we can make some assumptions about their contents.
```
for msg in c:
    print("{} said: {}".format(msg.value['sender'], msg.value['contents']))
```

4. Let's chat.

5. Now let's build some chatbots, or msg simulators.  Do this in another new python process, or from your producer process.
```
from simulators import NonsenseSimulator
sim = NonsenseSimulator(topic='human-messages', key='green', delay=0.5)
sim.simulate()
```

Take some time and write your own chatbot.

6.  Dang, there's a lot of noise now.  Let's alert when someone sends too many messages.
```
from alerts import ThrottlingAlertService
throttlealertservice = ThrottlingAlertService(monitor_topic='human-messages', alert_topic='alerts')
throttlealertservice.monitor()
```

Notice how this consumes messages off of one topic and produces messages onto another topic.

7. Demo other alert service.

8. What other additional services can we build on top of this?  Let's try a few - hack for a few minutes.

9. Recap 
    - notice how individual producers and consumers are very cheap to create and destroy 
    - the key components of this architecture are the central commit log and the pre-defined schema for a topic.
