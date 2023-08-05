#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2020 T-Systems Multimedia Solutions GmbH
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: icinga_notification_template
short_description: Manage notification templates in Icinga2
description:
   - Add or remove a notification template to Icinga2 through the director API.
author: Sebastian Gumprich (@rndmh3ro) / Sebastian Gruber (sgruber94)
extends_documentation_fragment:
  - ansible.builtin.url
  - t_systems_mms.icinga_director.common_options
version_added: "1.9.0"
notes:
  - This module supports check mode.
options:
  state:
    description:
      - Apply feature state.
    choices: [ "present", "absent" ]
    default: present
    type: str
  object_name:
    description:
      - Name of the notification template.
    aliases: ['name']
    required: true
    type: str
  notification_interval:
    description:
      - The notification interval (in seconds). This interval is used for active notifications.
      - Defaults to 30 minutes. If set to 0, re-notifications are disabled.
    type: str
  types:
    description:
      - The state transition types you want to get notifications for.
    type: "list"
    elements: str
  states:
    description:
      - The host or service states you want to get notifications for.
    type: "list"
    elements: str
  times_begin:
    description:
      - First notification delay.
      - Delay unless the first notification should be sent.
    type: "int"
  times_end:
    description:
      - Last notification.
      - When the last notification should be sent.
    type: "int"
  zone:
    description:
      - Set the zone.
    type: str
  time_period:
    description:
      - The name of a time period which determines when this notification should be triggered.
    type: "str"
    aliases: ['period']
    version_added: "1.15.0"
  notification_command:
    description:
      - Check command definition
    type: "str"
    aliases: ['command']
    version_added: "1.15.0"
  users:
    description:
      - Users that should be notified by this notification
    type: "list"
    elements: str
    version_added: "1.15.0"
  user_groups:
    description:
      - User Groups that should be notified by this notification.
    type: "list"
    elements: str
    version_added: '1.16.0'
"""

EXAMPLES = """
- name: Create notification template
  t_systems_mms.icinga_director.icinga_notification_template:
    state: present
    url: "{{ icinga_url }}"
    url_username: "{{ icinga_user }}"
    url_password: "{{ icinga_pass }}"
    notification_interval: '0'
    object_name: foonotificationtemplate
    states:
      - Up
      - Down
    types:
      - Problem
      - Recovery
    times_begin: 20
    times_end: 120
    time_period: "24/7"
    notification_command: "mail-host-notification"
    users:
      - "rb"
    user_groups:
      - "OnCall"
"""

RETURN = r""" # """

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import url_argument_spec
from ansible_collections.t_systems_mms.icinga_director.plugins.module_utils.icinga import (
    Icinga2APIObject,
)


# ===========================================
# Module execution.
#
def main():
    # use the predefined argument spec for url
    argument_spec = url_argument_spec()

    # add our own arguments
    argument_spec.update(
        state=dict(default="present", choices=["absent", "present"]),
        url=dict(required=True),
        object_name=dict(required=True, aliases=["name"]),
        notification_interval=dict(required=False),
        states=dict(type="list", elements="str", required=False),
        times_begin=dict(type="int", required=False),
        times_end=dict(type="int", required=False),
        types=dict(type="list", elements="str", required=False),
        zone=dict(required=False, default=None),
        time_period=dict(required=False, aliases=["period"]),
        notification_command=dict(required=False, aliases=["command"]),
        users=dict(type="list", elements="str", required=False),
        user_groups=dict(type="list", elements="str", required=False),
    )

    # Define the main module
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    data = {
        "object_name": module.params["object_name"],
        "object_type": "template",
        "notification_interval": module.params["notification_interval"],
        "states": module.params["states"],
        "times_begin": module.params["times_begin"],
        "times_end": module.params["times_end"],
        "types": module.params["types"],
        "zone": module.params["zone"],
        "period": module.params["time_period"],
        "command": module.params["notification_command"],
        "users": module.params["users"],
        "user_groups": module.params["user_groups"],
    }

    icinga_object = Icinga2APIObject(
        module=module, path="/notification", data=data
    )

    changed, diff = icinga_object.update(module.params["state"])
    module.exit_json(
        changed=changed,
        diff=diff,
    )


# import module snippets
if __name__ == "__main__":
    main()
