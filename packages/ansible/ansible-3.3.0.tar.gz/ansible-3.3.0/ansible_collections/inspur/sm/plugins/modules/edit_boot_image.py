#!/usr/bin/python
# -*- coding:utf-8 -*-

# Copyright(C) 2020 Inspur Inc. All Rights Reserved.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = '''
---
module: edit_boot_image
version_added: "0.1.0"
author:
    - WangBaoshan (@ISIB-group)
short_description: Set bmc boot image.
description:
   - Set bmc boot image on Inspur server.
options:
    image:
        description:
            - BMC boot image. 0-Higher firmware version;1-Image 1;2-Image 2;3-Lower firmware version;4-Latest updated firmware;5-Not latest updated firmware.
        choices: [0, 1, 2, 3, 4, 5]
        type: int
        required: true
extends_documentation_fragment:
    - inspur.sm.ism
'''

EXAMPLES = '''
- name: Boot image test
  hosts: ism
  connection: local
  gather_facts: no
  vars:
    ism:
      host: "{{ ansible_ssh_host }}"
      username: "{{ username }}"
      password: "{{ password }}"

  tasks:

  - name: "Set bmc boot image"
    inspur.sm.edit_boot_image:
      image: 2
      provider: "{{ ism }}"
'''

RETURN = '''
message:
    description: Messages returned after module execution.
    returned: always
    type: str
state:
    description: Status after module execution.
    returned: always
    type: str
changed:
    description: Check to see if a change was made on the device.
    returned: always
    type: bool
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.inspur.sm.plugins.module_utils.ism import (ism_argument_spec, get_connection)


class Image(object):
    def __init__(self, argument_spec):
        self.spec = argument_spec
        self.module = None
        self.init_module()
        self.results = dict()

    def init_module(self):
        """Init module object"""

        self.module = AnsibleModule(
            argument_spec=self.spec, supports_check_mode=False)

    def run_command(self):
        self.module.params['subcommand'] = 'setbootimage'
        self.results = get_connection(self.module)
        if self.results['State'] == 'Success':
            self.results['changed'] = True

    def show_result(self):
        """Show result"""
        self.module.exit_json(**self.results)

    def work(self):
        """Worker"""
        self.run_command()
        self.show_result()


def main():
    argument_spec = dict(
        image=dict(type='int', required=True, choices=[0, 1, 2, 3, 4, 5]),
    )
    argument_spec.update(ism_argument_spec)
    image_obj = Image(argument_spec)
    image_obj.work()


if __name__ == '__main__':
    main()
