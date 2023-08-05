#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2018, Mikhail Yohman (@FragmentedPacket) <mikhail.yohman@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "status": ["preview"],
    "supported_by": "community",
}

DOCUMENTATION = r"""
---
module: netbox_vlan
short_description: Create, update or delete vlans within Netbox
description:
  - Creates, updates or removes vlans from Netbox
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Mikhail Yohman (@FragmentedPacket)
requirements:
  - pynetbox
version_added: '0.1.0'
options:
  netbox_url:
    description:
      - URL of the Netbox instance resolvable by Ansible control host
    required: true
    type: str
  netbox_token:
    description:
      - The token created within Netbox to authorize API access
    required: true
    type: str
  data:
    type: dict
    description:
      - Defines the vlan configuration
    suboptions:
      site:
        description:
          - The site the VLAN will be associated to
        required: false
        type: raw
      vlan_group:
        description:
          - The VLAN group the VLAN will be associated to
        required: false
        type: raw
      vid:
        description:
          - The VLAN ID
        required: false
        type: int
      name:
        description:
          - The name of the vlan
        required: true
        type: str
      tenant:
        description:
          - The tenant that the vlan will be assigned to
        required: false
        type: raw
      status:
        description:
          - The status of the vlan
        required: false
        type: raw
      vlan_role:
        description:
          - Required if I(state=present) and the vlan does not exist yet
        required: false
        type: raw
      description:
        description:
          - The description of the vlan
        required: false
        type: str
      tags:
        description:
          - Any tags that the vlan may need to be associated with
        required: false
        type: list
      custom_fields:
        description:
          - must exist in Netbox
        required: false
        type: dict
    required: true
  state:
    description:
      - Use C(present) or C(absent) for adding or removing.
    choices: [ absent, present ]
    default: present
    type: str
  query_params:
    description:
      - This can be used to override the specified values in ALLOWED_QUERY_PARAMS that is defined
      - in plugins/module_utils/netbox_utils.py and provides control to users on what may make
      - an object unique in their environment.
    required: false
    type: list
    elements: str
  validate_certs:
    description:
      - If C(no), SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates.
    default: true
    type: raw
"""

EXAMPLES = r"""
- name: "Test Netbox modules"
  connection: local
  hosts: localhost
  gather_facts: False

  tasks:
    - name: Create vlan within Netbox with only required information
      netbox_vlan:
        netbox_url: http://netbox.local
        netbox_token: thisIsMyToken
        data:
          name: Test VLAN
          vid: 400
        state: present

    - name: Delete vlan within netbox
      netbox_vlan:
        netbox_url: http://netbox.local
        netbox_token: thisIsMyToken
        data:
          name: Test VLAN
          vid: 400
        state: absent

    - name: Create vlan with all information
      netbox_vlan:
        netbox_url: http://netbox.local
        netbox_token: thisIsMyToken
        data:
          name: Test VLAN
          vid: 400
          site: Test Site
          group: Test VLAN Group
          tenant: Test Tenant
          status: Deprecated
          vlan_role: Test VLAN Role
          description: Just a test
          tags:
            - Schnozzberry
        state: present
"""

RETURN = r"""
vlan:
  description: Serialized object as created or already existent within Netbox
  returned: success (when I(state=present))
  type: dict
msg:
  description: Message indicating failure or info about what has been achieved
  returned: always
  type: str
"""

from ansible_collections.netbox.netbox.plugins.module_utils.netbox_utils import (
    NetboxAnsibleModule,
    NETBOX_ARG_SPEC,
)
from ansible_collections.netbox.netbox.plugins.module_utils.netbox_ipam import (
    NetboxIpamModule,
    NB_VLANS,
)
from copy import deepcopy


def main():
    """
    Main entry point for module execution
    """
    argument_spec = deepcopy(NETBOX_ARG_SPEC)
    argument_spec.update(
        dict(
            data=dict(
                type="dict",
                required=True,
                options=dict(
                    site=dict(required=False, type="raw"),
                    vlan_group=dict(required=False, type="raw"),
                    vid=dict(required=False, type="int"),
                    name=dict(required=True, type="str"),
                    tenant=dict(required=False, type="raw"),
                    status=dict(required=False, type="raw"),
                    vlan_role=dict(required=False, type="raw"),
                    description=dict(required=False, type="str"),
                    tags=dict(required=False, type="list"),
                    custom_fields=dict(required=False, type="dict"),
                ),
            ),
        )
    )
    required_if = [
        ("state", "present", ["name"]),
        ("state", "absent", ["name"]),
    ]

    module = NetboxAnsibleModule(
        argument_spec=argument_spec, supports_check_mode=True, required_if=required_if
    )

    netbox_vlan = NetboxIpamModule(module, NB_VLANS)
    netbox_vlan.run()


if __name__ == "__main__":  # pragma: no cover
    main()
