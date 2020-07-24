import logging
import os
from re import match

import yaml

__PGA_ID = None
__PROPERTIES = {}


def parse_yaml(yaml_file_path):
    with open(yaml_file_path, mode="r", encoding="utf-8") as yaml_file:
        content = yaml.safe_load(yaml_file) or {}
    return content


def get_pga_id():
    if not __PGA_ID:
        return __retrieve_pga_id()
    return __PGA_ID


def __retrieve_pga_id():
    # Retrieve locally saved config file.
    files = [f for f in os.listdir("/") if match(r'[0-9]+--config\.yml', f)]
    # https://stackoverflow.com/questions/2225564/get-a-filtered-list-of-files-in-a-directory/2225927#2225927
    # https://regex101.com/

    if not files.__len__() > 0:
        raise Exception("Error retrieving the PGA ID: No matching config file found!")
    config = parse_yaml("/{}".format(files[0]))
    global __PGA_ID
    __PGA_ID = config.get("pga_id")
    logging.info("PGA_ID {id_} retrieved.".format(id_=__PGA_ID))
    return __PGA_ID


def get_property(property_key):
    return __PROPERTIES[property_key]


def set_property(property_key, property_value):
    __PROPERTIES[property_key] = property_value
