import logging

from population.pair import Pair


def call_operator(individual1, individual2):
    logging.debug("evaluating fitness of individuals")
    return Pair(individual1, individual2)
