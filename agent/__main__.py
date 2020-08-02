import logging
import time

from database_handler.handlers import DatabaseHandlers
from database_handler.redis_handler import RedisHandler
from message_handler.handlers import MessageHandlers
from message_handler.rabbit_message_queue import RabbitMessageQueue
from utilities import utils

logging.basicConfig(level=logging.INFO)

DATABASE_HANDLER = DatabaseHandlers.Redis
MESSAGE_HANDLER = MessageHandlers.RabbitMQ


def listen_for_operator_request():
    pga_id = utils.get_pga_id()

    database_handler = get_database_handler(pga_id)
    relevant_properties = utils.get_custom_setting("property_keys")
    for prop in relevant_properties:
        is_list = prop.get("is_list")
        if is_list:
            value = database_handler.retrieve_list(prop.get("key"))
        else:
            value = database_handler.retrieve_item(prop.get("key"))
        timer = 0
        start = time.perf_counter()
        while value is None and timer < 45:
            if is_list:
                value = database_handler.retrieve_list(prop.get("key"))
            else:
                value = database_handler.retrieve_item(prop.get("key"))
            time.sleep(1)
            timer = time.perf_counter() - start
        if timer >= 10:
            raise Exception("Could not load property: {key_}".format(key_=prop.get("key")))

        if is_list:
            decoded = []
            for val in value:
                decoded.append(val.decode("utf-8"))
            value = decoded
        else:
            value = value.decode("utf-8")
        utils.set_property(
            property_key=prop.get("key"),
            property_value=value
        )

    message_handler = get_message_handler(pga_id)
    message_handler.receive_messages()


def get_database_handler(pga_id):
    if DATABASE_HANDLER == DatabaseHandlers.Redis:
        return RedisHandler(pga_id)
    else:
        raise Exception("No valid DatabaseHandler defined!")


def get_message_handler(pga_id):
    if MESSAGE_HANDLER == MessageHandlers.RabbitMQ:
        return RabbitMessageQueue(pga_id)
    else:
        raise Exception("No valid MessageHandler defined!")


if __name__ == "__main__":
    listen_for_operator_request()
