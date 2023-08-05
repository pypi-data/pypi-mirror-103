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
The arg spec for the iosxr_acls module
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class AclsArgs(object):  # pylint: disable=R0903
    """The arg spec for the iosxr_acls module
    """

    def __init__(self, **kwargs):
        pass

    argument_spec = {
        "running_config": {"type": "str"},
        "config": {
            "elements": "dict",
            "options": {
                "acls": {
                    "elements": "dict",
                    "options": {
                        "name": {"type": "str"},
                        "aces": {
                            "elements": "dict",
                            "mutually_exclusive": [
                                ["grant", "remark", "line"]
                            ],
                            "options": {
                                "destination": {
                                    "mutually_exclusive": [
                                        ["address", "any", "host", "prefix"],
                                        [
                                            "wildcard_bits",
                                            "any",
                                            "host",
                                            "prefix",
                                        ],
                                    ],
                                    "options": {
                                        "host": {"type": "str"},
                                        "address": {"type": "str"},
                                        "any": {"type": "bool"},
                                        "prefix": {"type": "str"},
                                        "port_protocol": {
                                            "mutually_exclusive": [
                                                [
                                                    "eq",
                                                    "gt",
                                                    "lt",
                                                    "neq",
                                                    "range",
                                                ]
                                            ],
                                            "options": {
                                                "eq": {"type": "str"},
                                                "gt": {"type": "str"},
                                                "lt": {"type": "str"},
                                                "neq": {"type": "str"},
                                                "range": {
                                                    "options": {
                                                        "end": {"type": "str"},
                                                        "start": {
                                                            "type": "str"
                                                        },
                                                    },
                                                    "required_together": [
                                                        ["start", "end"]
                                                    ],
                                                    "type": "dict",
                                                },
                                            },
                                            "type": "dict",
                                        },
                                        "wildcard_bits": {"type": "str"},
                                    },
                                    "required_together": [
                                        ["address", "wildcard_bits"]
                                    ],
                                    "type": "dict",
                                },
                                "dscp": {
                                    "mutually_exclusive": [
                                        ["eq", "gt", "lt", "neq", "range"]
                                    ],
                                    "type": "dict",
                                    "options": {
                                        "eq": {"type": "str"},
                                        "gt": {"type": "str"},
                                        "lt": {"type": "str"},
                                        "neq": {"type": "str"},
                                        "range": {
                                            "options": {
                                                "end": {"type": "str"},
                                                "start": {"type": "str"},
                                            },
                                            "required_together": [
                                                ["start", "end"]
                                            ],
                                            "type": "dict",
                                        },
                                    },
                                },
                                "fragments": {"type": "bool"},
                                "capture": {"type": "bool"},
                                "destopts": {"type": "bool"},
                                "authen": {"type": "bool"},
                                "routing": {"type": "bool"},
                                "hop_by_hop": {"type": "bool"},
                                "grant": {
                                    "type": "str",
                                    "choices": ["permit", "deny"],
                                },
                                "icmp_off": {"type": "bool"},
                                "log": {"type": "bool"},
                                "log_input": {"type": "bool"},
                                "line": {"type": "str", "aliases": ["ace"]},
                                "packet_length": {
                                    "mutually_exclusive": [
                                        ["eq", "lt", "neq", "range"],
                                        ["eq", "gt", "neq", "range"],
                                    ],
                                    "options": {
                                        "eq": {"type": "int"},
                                        "gt": {"type": "int"},
                                        "lt": {"type": "int"},
                                        "neq": {"type": "int"},
                                        "range": {
                                            "options": {
                                                "end": {"type": "int"},
                                                "start": {"type": "int"},
                                            },
                                            "type": "dict",
                                        },
                                    },
                                    "type": "dict",
                                },
                                "precedence": {"type": "str"},
                                "protocol": {"type": "str"},
                                "protocol_options": {
                                    "mutually_exclusive": [
                                        ["icmp", "tcp", "igmp", "icmpv6"]
                                    ],
                                    "options": {
                                        "icmpv6": {
                                            "type": "dict",
                                            "options": {
                                                "address_unreachable": {
                                                    "type": "bool"
                                                },
                                                "administratively_prohibited": {
                                                    "type": "bool"
                                                },
                                                "beyond_scope_of_source_address": {
                                                    "type": "bool"
                                                },
                                                "destination_unreachable": {
                                                    "type": "bool"
                                                },
                                                "echo": {"type": "bool"},
                                                "echo_reply": {"type": "bool"},
                                                "erroneous_header_field": {
                                                    "type": "bool"
                                                },
                                                "group_membership_query": {
                                                    "type": "bool"
                                                },
                                                "group_membership_report": {
                                                    "type": "bool"
                                                },
                                                "group_membership_termination": {
                                                    "type": "bool"
                                                },
                                                "host_unreachable": {
                                                    "type": "bool"
                                                },
                                                "nd_na": {"type": "bool"},
                                                "nd_ns": {"type": "bool"},
                                                "neighbor_redirect": {
                                                    "type": "bool"
                                                },
                                                "no_route_to_destination": {
                                                    "type": "bool"
                                                },
                                                "node_information_request_is_refused": {
                                                    "type": "bool"
                                                },
                                                "node_information_successful_reply": {
                                                    "type": "bool"
                                                },
                                                "packet_too_big": {
                                                    "type": "bool"
                                                },
                                                "parameter_problem": {
                                                    "type": "bool"
                                                },
                                                "port_unreachable": {
                                                    "type": "bool"
                                                },
                                                "query_subject_is_IPv4address": {
                                                    "type": "bool"
                                                },
                                                "query_subject_is_IPv6address": {
                                                    "type": "bool"
                                                },
                                                "query_subject_is_domainname": {
                                                    "type": "bool"
                                                },
                                                "reassembly_timeout": {
                                                    "type": "bool"
                                                },
                                                "redirect": {"type": "bool"},
                                                "router_advertisement": {
                                                    "type": "bool"
                                                },
                                                "router_renumbering": {
                                                    "type": "bool"
                                                },
                                                "router_solicitation": {
                                                    "type": "bool"
                                                },
                                                "rr_command": {"type": "bool"},
                                                "rr_result": {"type": "bool"},
                                                "rr_seqnum_reset": {
                                                    "type": "bool"
                                                },
                                                "time_exceeded": {
                                                    "type": "bool"
                                                },
                                                "ttl_exceeded": {
                                                    "type": "bool"
                                                },
                                                "unknown_query_type": {
                                                    "type": "bool"
                                                },
                                                "unreachable": {
                                                    "type": "bool"
                                                },
                                                "unrecognized_next_header": {
                                                    "type": "bool"
                                                },
                                                "unrecognized_option": {
                                                    "type": "bool"
                                                },
                                                "whoareyou_reply": {
                                                    "type": "bool"
                                                },
                                                "whoareyou_request": {
                                                    "type": "bool"
                                                },
                                            },
                                        },
                                        "icmp": {
                                            "options": {
                                                "administratively_prohibited": {
                                                    "type": "bool"
                                                },
                                                "alternate_address": {
                                                    "type": "bool"
                                                },
                                                "conversion_error": {
                                                    "type": "bool"
                                                },
                                                "dod_host_prohibited": {
                                                    "type": "bool"
                                                },
                                                "dod_net_prohibited": {
                                                    "type": "bool"
                                                },
                                                "echo": {"type": "bool"},
                                                "echo_reply": {"type": "bool"},
                                                "general_parameter_problem": {
                                                    "type": "bool"
                                                },
                                                "host_isolated": {
                                                    "type": "bool"
                                                },
                                                "host_precedence_unreachable": {
                                                    "type": "bool"
                                                },
                                                "host_redirect": {
                                                    "type": "bool"
                                                },
                                                "host_tos_redirect": {
                                                    "type": "bool"
                                                },
                                                "host_tos_unreachable": {
                                                    "type": "bool"
                                                },
                                                "host_unknown": {
                                                    "type": "bool"
                                                },
                                                "host_unreachable": {
                                                    "type": "bool"
                                                },
                                                "information_reply": {
                                                    "type": "bool"
                                                },
                                                "information_request": {
                                                    "type": "bool"
                                                },
                                                "mask_reply": {"type": "bool"},
                                                "mask_request": {
                                                    "type": "bool"
                                                },
                                                "mobile_redirect": {
                                                    "type": "bool"
                                                },
                                                "net_redirect": {
                                                    "type": "bool"
                                                },
                                                "net_tos_redirect": {
                                                    "type": "bool"
                                                },
                                                "net_tos_unreachable": {
                                                    "type": "bool"
                                                },
                                                "net_unreachable": {
                                                    "type": "bool"
                                                },
                                                "network_unknown": {
                                                    "type": "bool"
                                                },
                                                "no_room_for_option": {
                                                    "type": "bool"
                                                },
                                                "option_missing": {
                                                    "type": "bool"
                                                },
                                                "packet_too_big": {
                                                    "type": "bool"
                                                },
                                                "parameter_problem": {
                                                    "type": "bool"
                                                },
                                                "port_unreachable": {
                                                    "type": "bool"
                                                },
                                                "precedence_unreachable": {
                                                    "type": "bool"
                                                },
                                                "protocol_unreachable": {
                                                    "type": "bool"
                                                },
                                                "reassembly_timeout": {
                                                    "type": "bool"
                                                },
                                                "redirect": {"type": "bool"},
                                                "router_advertisement": {
                                                    "type": "bool"
                                                },
                                                "router_solicitation": {
                                                    "type": "bool"
                                                },
                                                "source_quench": {
                                                    "type": "bool"
                                                },
                                                "source_route_failed": {
                                                    "type": "bool"
                                                },
                                                "time_exceeded": {
                                                    "type": "bool"
                                                },
                                                "timestamp_reply": {
                                                    "type": "bool"
                                                },
                                                "timestamp_request": {
                                                    "type": "bool"
                                                },
                                                "traceroute": {"type": "bool"},
                                                "ttl_exceeded": {
                                                    "type": "bool"
                                                },
                                                "unreachable": {
                                                    "type": "bool"
                                                },
                                            },
                                            "type": "dict",
                                        },
                                        "igmp": {
                                            "options": {
                                                "dvmrp": {"type": "bool"},
                                                "host_query": {"type": "bool"},
                                                "host_report": {
                                                    "type": "bool"
                                                },
                                                "mtrace": {"type": "bool"},
                                                "mtrace_response": {
                                                    "type": "bool"
                                                },
                                                "pim": {"type": "bool"},
                                                "trace": {"type": "bool"},
                                            },
                                            "type": "dict",
                                        },
                                        "tcp": {
                                            "options": {
                                                "ack": {"type": "bool"},
                                                "established": {
                                                    "type": "bool"
                                                },
                                                "fin": {"type": "bool"},
                                                "psh": {"type": "bool"},
                                                "rst": {"type": "bool"},
                                                "syn": {"type": "bool"},
                                                "urg": {"type": "bool"},
                                            },
                                            "type": "dict",
                                        },
                                    },
                                    "type": "dict",
                                },
                                "remark": {"type": "str"},
                                "sequence": {"type": "int"},
                                "source": {
                                    "mutually_exclusive": [
                                        ["address", "any", "host", "prefix"],
                                        [
                                            "wildcard_bits",
                                            "any",
                                            "host",
                                            "prefix",
                                        ],
                                    ],
                                    "options": {
                                        "host": {"type": "str"},
                                        "address": {"type": "str"},
                                        "any": {"type": "bool"},
                                        "prefix": {"type": "str"},
                                        "port_protocol": {
                                            "mutually_exclusive": [
                                                [
                                                    "eq",
                                                    "gt",
                                                    "lt",
                                                    "neq",
                                                    "range",
                                                ]
                                            ],
                                            "options": {
                                                "eq": {"type": "str"},
                                                "gt": {"type": "str"},
                                                "lt": {"type": "str"},
                                                "neq": {"type": "str"},
                                                "range": {
                                                    "options": {
                                                        "end": {"type": "str"},
                                                        "start": {
                                                            "type": "str"
                                                        },
                                                    },
                                                    "required_together": [
                                                        ["start", "end"]
                                                    ],
                                                    "type": "dict",
                                                },
                                            },
                                            "type": "dict",
                                        },
                                        "wildcard_bits": {"type": "str"},
                                    },
                                    "required_together": [
                                        ["address", "wildcard_bits"]
                                    ],
                                    "type": "dict",
                                },
                                "ttl": {
                                    "mutually_exclusive": [
                                        ["eq", "gt", "lt", "neq", "range"]
                                    ],
                                    "options": {
                                        "eq": {"type": "int"},
                                        "gt": {"type": "int"},
                                        "lt": {"type": "int"},
                                        "neq": {"type": "int"},
                                        "range": {
                                            "options": {
                                                "end": {"type": "int"},
                                                "start": {"type": "int"},
                                            },
                                            "type": "dict",
                                        },
                                    },
                                    "type": "dict",
                                },
                            },
                            "type": "list",
                        },
                    },
                    "type": "list",
                },
                "afi": {
                    "choices": ["ipv4", "ipv6"],
                    "required": True,
                    "type": "str",
                },
            },
            "type": "list",
        },
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
