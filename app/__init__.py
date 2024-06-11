# Copyright (c) 2021-2024 Linh Pham
# do-droplets-report is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Core Application for DigitalOcean Droplets Report."""
from flask import Flask

from app import config, utility
from app.errors import handlers
from app.main.routes import blueprint as main_bp
from app.version import APP_VERSION


def create_app():
    """Initialize Flask and Configure Settings."""
    app = Flask(__name__)
    app.url_map.strict_slashes = False

    # Override base Jinja options
    app.jinja_options = Flask.jinja_options.copy()
    app.jinja_options.update({"trim_blocks": True, "lstrip_blocks": True})
    app.create_jinja_environment()

    # Register error handlers
    app.register_error_handler(404, handlers.not_found)
    app.register_error_handler(500, handlers.handle_exception)

    # Load configuration file
    app.config["app_settings"] = config.load_config()

    # Set up Jinja globals
    app.jinja_env.globals["app_version"] = APP_VERSION
    app.jinja_env.globals["rendered_at"] = utility.generate_date_time_stamp
    app.jinja_env.globals["time_zone"] = app.config["app_settings"]["time_zone"]

    # Register application blueprints
    app.register_blueprint(main_bp)

    return app
