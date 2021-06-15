import logging
import random
import time


MESSAGES = []

HEARTBEAT_INTERVAL = 5000


def get_message():
    if random.randrange(5) == 4:
        raise Exception("ITS A 4")

    return "message"


def add_message(message):
    MESSAGES.append(message)


def main():
    last_heartbeat_ts = 0
    while True:
        current_ts = int(round(time.time() * 1000))
        if (current_ts - last_heartbeat_ts) >= HEARTBEAT_INTERVAL:
            last_heartbeat_ts = current_ts
            print "trace publisher running"
        try:
            # do a thing that might raise an exception
            message = get_message()
        except Exception as e:
            #logging.exception("Error getting message")
            message = None

        try:
            add_message(message)
        except Exception as e:
            #logging.exception("Error adding message")
            pass


if __name__ == '__main__':
    main()
