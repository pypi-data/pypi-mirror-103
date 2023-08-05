#
# -*- coding: utf-8 -*-
# Copyright 2019 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#############################################
#                WARNING                    #
#############################################
#
# This file is auto generated by the resource
#   module builder playbook.
#
# Do not edit this file manually.
#
# Changes to this file will be over written
#   by the resource module builder.
#
# Changes should be made in the model used to
#   generate this file or in the resource module
#   builder template.
#
#############################################
"""
The arg spec for the vyos_static_routes module
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class Static_routesArgs(object):  # pylint: disable=R0903
    """The arg spec for the vyos_static_routes module"""

    def __init__(self, **kwargs):
        pass

    argument_spec = {
        "config": {
            "elements": "dict",
            "options": {
                "address_families": {
                    "elements": "dict",
                    "options": {
                        "afi": {
                            "choices": ["ipv4", "ipv6"],
                            "required": True,
                            "type": "str",
                        },
                        "routes": {
                            "elements": "dict",
                            "options": {
                                "blackhole_config": {
                                    "options": {
                                        "distance": {"type": "int"},
                                        "type": {"type": "str"},
                                    },
                                    "type": "dict",
                                },
                                "dest": {"required": True, "type": "str"},
                                "next_hops": {
                                    "elements": "dict",
                                    "options": {
                                        "admin_distance": {"type": "int"},
                                        "enabled": {"type": "bool"},
                                        "forward_router_address": {
                                            "required": True,
                                            "type": "str",
                                        },
                                        "interface": {"type": "str"},
                                    },
                                    "type": "list",
                                },
                            },
                            "type": "list",
                        },
                    },
                    "type": "list",
                }
            },
            "type": "list",
        },
        "running_config": {"type": "str"},
        "state": {
            "choices": [
                "merged",
                "replaced",
                "overridden",
                "deleted",
                "gathered",
                "rendered",
                "parsed",
            ],
            "default": "merged",
            "type": "str",
        },
    }  # pylint: disable=C0301
