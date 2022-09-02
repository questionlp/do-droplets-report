# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2021-2022 Linh Pham
# do-droplets-report is released under the terms of the Apache License 2.0
"""Main Routes for DigitalOcean Droplets Report"""
import json
from typing import Any, Dict

import pytz

from . import utility


def load_config(config_file_path: str = "config.json") -> Dict[str, Dict[str, Any]]:
    with open(config_file_path, "r") as config_file:
        app_config = json.load(config_file)

    if "time_zone" in app_config and app_config["time_zone"]:
        time_zone = app_config["time_zone"]
        time_zone_object, time_zone_string = utility.time_zone_parser(time_zone)

        app_config["app_time_zone"] = time_zone_object
        app_config["time_zone"] = time_zone_string
    else:
        app_config["app_time_zone"] = pytz.timezone("UTC")
        app_config["time_zone"] = "UTC"

    return app_config
