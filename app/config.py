# Copyright (c) 2021-2024 Linh Pham
# do-droplets-report is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Main Routes for DigitalOcean Droplets Report."""
import json
from pathlib import Path
from typing import Any, Dict

import pytz

from . import utility


def load_config(
    config_file_path: str = "config.json", app_time_zone: str = "UTC"
) -> Dict[str, Dict[str, Any]]:
    """Load settings from config.json."""
    _config_file_path = Path(config_file_path)
    with _config_file_path.open(mode="r", encoding="utf-8") as config_file:
        app_config = json.load(config_file)

    time_zone = app_config.get("time_zone", app_time_zone)
    time_zone_object, time_zone_string = utility.time_zone_parser(time_zone)
    app_config["app_time_zone"] = time_zone_object
    app_config["time_zone"] = time_zone_string

    return app_config
