import logging
import os
import subprocess
import sys
from re import match

import yaml

__CONTAINER_CONF = None
__CUSTOM_CONF = None
__PROPERTIES = {}


# --- General util commands ---
def execute_command(
        command,
        working_directory,
        environment_variables,
        executor,
        logger=logging,
        livestream=False
):
    logger_prefix = ""
    if executor:
        logger_prefix = executor + ": "

    process = subprocess.Popen(
        command,
        cwd=working_directory,
        env=environment_variables,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=True,
    )

    logger.debug(logger_prefix + "command: " + command)

    stdout = ""
    for line in iter(process.stdout.readline, b''):
        line = str(line, "utf-8")
        stdout += line

        if livestream:
            sys.stdout.write(line)
        else:
            logger.debug(logger_prefix + "command output: " + line.rstrip())

    return_code = process.wait()
    stdout = stdout.rstrip()
    return stdout, return_code


def parse_yaml(yaml_file_path):
    with open(yaml_file_path, mode="r", encoding="utf-8") as yaml_file:
        content = yaml.safe_load(yaml_file) or {}
    return content


# Commands regarding messaging.
def get_messaging_source():
    if not __CONTAINER_CONF:
        __retrieve_container_config()
    return __CONTAINER_CONF["source"]


def get_messaging_target():
    if not __CONTAINER_CONF:
        __retrieve_container_config()
    return __CONTAINER_CONF["target"]


def get_pga_id():
    if not __CONTAINER_CONF:
        __retrieve_container_config()
    return __CONTAINER_CONF["pga_id"]


def __retrieve_container_config():
    # Retrieve custom agent config.
    if __CUSTOM_CONF is None:
        __retrieve_custom_config()
    container_name = __CUSTOM_CONF.get("container_name")

    # Retrieve locally saved config file.
    files = [f for f in os.listdir("/") if match(r'[0-9]+--{container_name}-config\.yml', f)]
    # https://stackoverflow.com/questions/2225564/get-a-filtered-list-of-files-in-a-directory/2225927#2225927
    # https://regex101.com/

    if not files.__len__() > 0:
        raise Exception("Error retrieving the container config: No matching config file found!")
    config = parse_yaml("/{}".format(files[0]))
    __CONTAINER_CONF["pga_id"] = config.get("pga_id")
    __CONTAINER_CONF["source"] = config.get("source")
    __CONTAINER_CONF["target"] = config.get("target")
    logging.info("Container config retrieved: {conf_}".format(conf_=__CONTAINER_CONF))


# Commands regarding properties and configuration.
def __retrieve_custom_config():
    global __CUSTOM_CONF
    __CUSTOM_CONF = parse_yaml("/custom-config.yml")
    logging.info("Custom config retrieved: {conf_}".format(conf_=__CUSTOM_CONF))


def get_custom_setting(key):
    if __CUSTOM_CONF is None:
        __retrieve_custom_config()
    return __CUSTOM_CONF[key]


def get_property(property_key):
    return __PROPERTIES[property_key]


def set_property(property_key, property_value):
    __PROPERTIES[property_key] = property_value
