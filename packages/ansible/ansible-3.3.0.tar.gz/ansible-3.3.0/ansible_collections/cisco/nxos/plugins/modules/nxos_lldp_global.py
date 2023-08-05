#!/usr/bin/python
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
The module file for nxos_lldp_global
"""
from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
module: nxos_lldp_global
short_description: LLDP resource module
description: This module configures and manages the Link Layer Discovery Protocol(LLDP)
  attributes on NX-OS platforms.
version_added: 1.0.0
author: Adharsh Srivats Rangarajan (@adharshsrivatsr)
notes:
- Tested against NxOS 7.3.(0)D1(1) on VIRL
- The LLDP feature needs to be enabled before using this module
options:
  running_config:
    description:
    - This option is used only with state I(parsed).
    - The value of this option should be the output received from the NX-OS device
      by executing the command B(show running-config | include lldp).
    - The state I(parsed) reads the configuration from C(running_config) option and
      transforms it into Ansible structured data as per the resource module's argspec
      and the value is then returned in the I(parsed) key within the result.
    type: str
  config:
    description:
    - A list of link layer discovery configurations
    type: dict
    suboptions:
      holdtime:
        description:
        - Amount of time the receiving device should hold the information (in seconds)
        type: int
      port_id:
        description:
        - This attribute defines if the interface names should be advertised in the
          long(0) or short(1) form.
        type: int
        choices:
        - 0
        - 1
      reinit:
        description:
        - Amount of time to delay the initialization of LLDP on any interface (in
          seconds)
        type: int
      timer:
        description:
        - Frequency at which LLDP updates need to be transmitted (in seconds)
        type: int
      tlv_select:
        description:
        - This attribute can be used to specify the TLVs that need to be sent and
          received in the LLDP packets. By default, all TLVs are advertised
        type: dict
        suboptions:
          dcbxp:
            description:
            - Used to specify the Data Center Bridging Exchange Protocol TLV
            type: bool
          management_address:
            description:
            - Used to specify the management address in TLV messages
            type: dict
            suboptions:
              v4:
                description: Management address with TLV v4
                type: bool
              v6:
                description: Management address with TLV v6
                type: bool
          port:
            description:
            - Used to manage port based attributes in TLV messages
            type: dict
            suboptions:
              description:
                description:
                - Used to specify the port description TLV
                type: bool
              vlan:
                description:
                - Used to specify the port VLAN ID TLV
                type: bool
          power_management:
            description:
            - Used to specify IEEE 802.3 DTE Power via MDI TLV
            type: bool
          system:
            description:
            - Used to manage system based attributes in TLV messages
            type: dict
            suboptions:
              capabilities:
                description:
                - Used to specify the system capabilities TLV
                type: bool
              description:
                description:
                - Used to specify the system description TLV
                type: bool
              name:
                description:
                - Used to specify the system name TLV
                type: bool
  state:
    description:
    - The state of the configuration after module completion
    type: str
    choices:
    - merged
    - replaced
    - deleted
    - gathered
    - rendered
    - parsed
    default: merged

"""
EXAMPLES = """
# Using merged
# Before state:
# -------------
#
# user(config)# show running-config | include lldp
# feature lldp

- name: Merge provided configuration with device configuration
  cisco.nxos.nxos_lldp_global:
    config:
      timer: 35
      holdtime: 100
    state: merged

# After state:
# ------------
#
# user(config)# show running-config | include lldp
# feature lldp
# lldp timer 35
# lldp holdtime 100


# Using replaced
# Before state:
# -------------
#
# user(config)# show running-config | include lldp
# feature lldp
# lldp holdtime 100
# lldp reinit 5
# lldp timer 35

- name: Replace device configuration of specific LLDP attributes with provided configuration
  cisco.nxos.nxos_lldp_global:
    config:
      timer: 40
      tlv_select:
        system:
          description: true
          name: false
        management_address:
          v4: true
    state: replaced

# After state:
# ------------
#
# user(config)# show running-config | include lldp
# feature lldp
# lldp timer 40
# no lldp tlv-select system-name


# Using deleted
# Before state:
# -------------
#
# user(config)# show running-config | include lldp
# feature lldp
# lldp holdtime 5
# lldp reinit 3

- name: Delete LLDP configuration (this will by default remove all lldp configuration)
  cisco.nxos.nxos_lldp_global:
    state: deleted

# After state:
# ------------
#
# user(config)# show running-config | include lldp
# feature lldp

# Using rendered

- name: Use rendered state to convert task input to device specific commands
  cisco.nxos.nxos_lldp_global:
    config:
      holdtime: 130
      port_id: 1
      reinit: 5
      tlv_select:
        dcbxp: yes
        power_management: yes
    state: rendered

# Task Output (redacted)
# -----------------------

# rendered:
#   - "lldp tlv-select dcbxp"
#   - "lldp tlv-select power-management"
#   - "lldp portid-subtype 1"
#   - "lldp reinit 5"
#   - "lldp holdtime 130"

# Using parsed

# parsed.cfg
# ------------
# lldp holdtime 131
# lldp reinit 7
# no lldp tlv-select system-name
# no lldp tlv-select system-description

# Task output (redacted)
# -----------------------

# parsed:
#   holdtime: 131
#   reinit: 7
#   tlv_select:
#     system:
#       description: false
#       name: false

# Using gathered

# Existing device config state
# -------------------------------
# feature lldp
# lldp holdtime 129
# lldp reinit 5
# lldp timer 35
# no lldp tlv-select system-name

# Task output (redacted)
# -----------------------

# gathered:
#   reinit: 5
#   timer: 35
#   tlv_select:
#     system:
#       name: False
#   holdtime: 129
"""
RETURN = """
before:
  description: The configuration as structured data prior to module invocation.
  returned: always
  type: dict
  sample: >
    The configuration returned will always be in the same format
     of the parameters above.
after:
  description: The configuration as structured data after module completion.
  returned: when changed
  type: dict
  sample: >
    The configuration returned will always be in the same format
     of the parameters above.
commands:
  description: The set of commands pushed to the remote device.
  returned: always
  type: list
  sample: ['lldp holdtime 125', 'lldp reinit 4', 'no lldp tlv-select system-name']
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.argspec.lldp_global.lldp_global import (
    Lldp_globalArgs,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.config.lldp_global.lldp_global import (
    Lldp_global,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    required_if = [
        ("state", "merged", ("config",)),
        ("state", "replaced", ("config",)),
        ("state", "rendered", ("config",)),
        ("state", "parsed", ("running_config",)),
    ]
    mutually_exclusive = [("config", "running_config")]

    module = AnsibleModule(
        argument_spec=Lldp_globalArgs.argument_spec,
        required_if=required_if,
        mutually_exclusive=mutually_exclusive,
        supports_check_mode=True,
    )

    result = Lldp_global(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
