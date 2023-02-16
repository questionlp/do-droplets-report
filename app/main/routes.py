# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2021-2022 Linh Pham
# do-droplets-report is released under the terms of the Apache License 2.0
"""Main Routes for DigitalOcean Droplets Report"""
from os.path import exists, join
from flask import Blueprint, Response, current_app, render_template, send_file

from app.droplets import retrieve_droplets

blueprint = Blueprint("main", __name__)


@blueprint.route("/")
def index():
    """View: Site Index Page"""
    droplet_info = retrieve_droplets(
        api_key=current_app.config["app_settings"]["do_api_key"],
        api_url=current_app.config["app_settings"]["do_api_url"],
    )
    return render_template("index.html", droplet_info=droplet_info)


@blueprint.route("/robots.txt")
def robots_txt():
    """View: robots.txt File"""
    if not exists(join(current_app.root_path, "static", "robots.txt")):
        response = render_template("robots.txt")
        return Response(response, mimetype="text/plain")
    else:
        return send_file(
            join(current_app.root_path, "static", "robots.txt"), mimetype="text/plain"
        )
