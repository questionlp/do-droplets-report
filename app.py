# -*- coding: utf-8 -*-
# Copyright (c) 2021 Linh Pham
# do-instances-report is relased under the terms of the Apache License 2.0
"""Flask application startup file"""

from collections import OrderedDict
from datetime import datetime
import os
from typing import Dict

import dotenv
from flask import Flask, redirect, render_template, url_for
import pytz
import requests

#region Flask App Initialization
app = Flask(__name__)
app.url_map.strict_slashes = False

# Override base Jinja options
app.jinja_options = Flask.jinja_options.copy()
app.jinja_options.update({"trim_blocks": True, "lstrip_blocks": True})
app.create_jinja_environment()

#endregion

# region Utility Functions
def time_zone_parser(time_zone: str) -> pytz.timezone:
    """Parses a time zone name into a pytz.timezone object.

    Returns pytz.timezone object and string if time_zone is valid.
    Otherwise, returns UTC if time zone is not a valid tz value."""

    try:
        time_zone_object = pytz.timezone(time_zone)
        time_zone_string = time_zone_object.zone
    except (pytz.UnknownTimeZoneError, AttributeError, ValueError):
        time_zone_object = pytz.timezone("UTC")
        time_zone_string = time_zone_object.zone

    return time_zone_object, time_zone_string

def generate_date_time_stamp(time_zone: pytz.timezone = pytz.timezone("UTC")):
    """Generate a current date/timestamp string"""

    now = datetime.now(time_zone)
    return now.strftime("%Y-%m-%d %H:%M:%S %Z")

def load_config() -> Dict:
    """Load DigitalOcean API Key and URL from environment variables"""

    dotenv.load_dotenv(dotenv.find_dotenv())
    config = {}
    config["DO_API_KEY"] = os.getenv("DO_API_KEY", default="")
    config["DO_API_URL"] = os.getenv("DO_API_URL",
                                     default="https://api.digitalocean.com/v2/droplets")
    time_zone_object, time_zone_string = time_zone_parser(os.getenv("TZ", default="UTC"))
    config["TIME_ZONE_OBJECT"] = time_zone_object
    config["TIME_ZONE_NAME"] = time_zone_string
    return config

#endregion

#region Routes
@app.route("/")
def index():
    """Default Landing Page"""

    config = load_config()
    rendered_time = generate_date_time_stamp(config["TIME_ZONE_OBJECT"])
    if not config["DO_API_KEY"]:
        return

    request = requests.get(config["DO_API_URL"],
                           auth=(config["DO_API_KEY"], ""))
    if not request.status_code == 200:
        return render_template("index.html",
                               droplet_info=None,
                               rendered_time=rendered_time)

    response = request.json()
    request.close()

    droplets = response["droplets"]
    if not droplets:
        return render_template("index.html",
                               droplet_info=None,
                               rendered_time=rendered_time)

    do_droplets = []
    for droplet in droplets:
        droplet_info = OrderedDict()
        droplet_info["name"] = droplet["name"]
        droplet_info["status"] = droplet["status"]
        droplet_info["memory"] = droplet["memory"]
        droplet_info["vcpus"] = droplet["vcpus"]
        droplet_info["disk"] = droplet["disk"]
        droplet_info["distro"] = droplet["image"]["distribution"]
        droplet_info["region_name"] = droplet["region"]["name"]
        droplet_info["region_slug"] = droplet["region"]["slug"]
        droplet_networks = droplet["networks"]

        for ipv4_networks in droplet_networks["v4"]:
            if ipv4_networks["type"] == "public":
                droplet_info["ipv4_public"] = ipv4_networks["ip_address"]
            elif ipv4_networks["type"] == "private":
                droplet_info["ipv4_private"] = ipv4_networks["ip_address"]

        if "v6" in droplet_networks:
            for ipv6_networks in droplet_networks["v6"]:
                if ipv6_networks["type"] == "public":
                    droplet_info["ipv6_public"] = ipv6_networks["ip_address"]
                elif ipv6_networks["type"] == "private":
                    droplet_info["ipv6_private"] = ipv6_networks["ip_address"]

        do_droplets.append(droplet_info)

    # Sort list based on droplet name
    do_droplets_sorted = sorted(do_droplets, key = lambda i: i["name"])

    return render_template("index.html",
                           droplet_info=do_droplets_sorted,
                           rendered_time=rendered_time)

#endregion

#region Application Initialization
if __name__ == "__main__":    
    app.run(debug=False, host="0.0.0.0", port="9248")

#endregion
