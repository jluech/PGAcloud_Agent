import logging

from database_handler.handlers import DatabaseHandlers
from database_handler.redis_handler import RedisHandler
from message_handler.handlers import MessageHandlers
from message_handler.rabbit_message_queue import RabbitMessageQueue
from utilities.utils import get_pga_id, set_property

logging.basicConfig(level=logging.DEBUG)  # TODO: remove and reduce to INFO

DATABASE_HANDLER = DatabaseHandlers.Redis
MESSAGE_HANDLER = MessageHandlers.RabbitMQ
RELEVANT_PROPERTIES = []


def listen_for_fitness_evaluation():
    pga_id = get_pga_id()
    database_handler = get_database_handler(pga_id)
    for prop in RELEVANT_PROPERTIES:
        set_property(
            property_key=prop,
            property_value=database_handler.retrieve(prop)
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
    listen_for_fitness_evaluation()
