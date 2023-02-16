# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2021-2022 Linh Pham
# do-droplets-report is released under the terms of the Apache License 2.0
"""Utility Functions for DigitalOcean Droplets Report"""
from typing import Dict

import requests


def retrieve_droplets(api_key: str, api_url: str) -> Dict:
    if not api_key or not api_url:
        return None

    api_request = requests.get(url=api_url, auth=(api_key, ""))
    if not api_request.status_code == 200:
        return None

    api_response = api_request.json()
    api_request.close()

    droplets = api_response["droplets"]
    if not droplets:
        return None

    do_droplets = []
    for droplet in droplets:
        droplet_info = {
            "name": droplet["name"],
            "status": droplet["status"],
            "description": droplet["size"]["description"],
            "size_slug": droplet["size"]["slug"],
            "memory": droplet["memory"],
            "vcpus": droplet["vcpus"],
            "disk": droplet["disk"],
            "distro": droplet["image"]["distribution"],
            "region_name": droplet["region"]["name"],
            "region_slug": droplet["region"]["slug"],
            "tags": droplet["tags"],
        }
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

    return sorted(do_droplets, key=lambda i: i["name"])
