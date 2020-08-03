import json
import logging
import os

from population.individual import Individual, IndividualEncoder
from utilities import utils


def call_operator(individual):
    # Write individual to file in input_path.
    # https://docs.python-guide.org/scenarios/serialization/#json-file-nested-data
    input_path = utils.get_custom_setting("input_path")
    with open(input_path, "x") as f:
        json.dump(individual, f, sort_keys=True, cls=IndividualEncoder)

    # Call operator with provided command.
    command_str = utils.get_custom_setting("command")
    logging.info("Retrieved command string: {cmdstr_}".format(cmdstr_=command_str))

    fixed_command = ""
    marker_open = 0
    marker_close = -1
    idx = 0
    for char in command_str:
        if char == "{":
            marker_open = idx
        elif char == "}":
            prev_marker = marker_close+1  # initially 0
            fixed_command += command_str[prev_marker:marker_open]

            marker_close = idx
            key = command_str[marker_open+1:marker_close]
            value = utils.get_property(key)
            if type(value) is list:
                param_string = ",".join(value)
            else:
                param_string = str(value)

            fixed_command += param_string
        idx += 1

    logging.info("Calling operator with: {cmd_}".format(cmd_=fixed_command))
    logs, error = utils.execute_command(
        command=fixed_command,
        working_directory=None,
        environment_variables=None,
        executor="AGENT",
        livestream=True,
    )
    logging.info(logs)

    # Retrieve individual from file in output_path.
    # https://docs.python-guide.org/scenarios/serialization/#json-file-nested-data
    output_path = utils.get_custom_setting("output_path")
    with open(output_path, "r") as f:
        ind_dict = json.load(f)
        resulting_individual = Individual(ind_dict["solution"], ind_dict["fitness"])

    logging.info("Reading from output file: {}".format(resulting_individual))  # TODO: remove

    # Delete the files that were created to ensure fresh start.
    os.remove(input_path)
    os.remove(output_path)
    return resulting_individual
