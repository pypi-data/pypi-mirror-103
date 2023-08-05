#!/usr/bin/python

# (c) 2019, NetApp, Inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'certified'}


DOCUMENTATION = '''
author: NetApp Ansible Team (@carchi8py) <ng-ansibleteam@netapp.com>
description:
  - Create/Delete NVME namespace
extends_documentation_fragment:
  - netapp.ontap.netapp.na_ontap
module: na_ontap_nvme_namespace
options:
  state:
    choices: ['present', 'absent']
    description:
      - Whether the specified namespace should exist or not.
    default: present
    type: str
  vserver:
    description:
      - Name of the vserver to use.
    required: true
    type: str
  ostype:
    description:
      - Specifies the ostype for initiators
    choices: ['windows', 'linux', 'vmware', 'xen', 'hyper_v']
    type: str
  size:
    description:
      - Size in bytes.
        Range is [0..2^63-1].
    type: int
  size_unit:
    description:
    - The unit used to interpret the size parameter.
    choices: ['bytes', 'b', 'kb', 'mb', 'gb', 'tb', 'pb', 'eb', 'zb', 'yb']
    type: str
    default: 'b'
  path:
    description:
      - Namespace path.
    required: true
    type: str
  block_size:
    description:
      - Size in bytes of a logical block. Possible values are 512 (Data ONTAP 9.6 and later), 4096. The default value is 4096.
    choices: [512, 4096]
    type: int
    version_added: '20.5.0'
short_description: "NetApp ONTAP Manage NVME Namespace"
version_added: 2.8.0
'''

EXAMPLES = """

    - name: Create NVME Namespace
      na_ontap_nvme_namespace:
        state: present
        ostype: linux
        path: /vol/ansible/test
        size: 20
        size_unit: mb
        vserver: "{{ vserver }}"
        hostname: "{{ hostname }}"
        username: "{{ username }}"
        password: "{{ password }}"

    - name: Create NVME Namespace (Idempotency)
      na_ontap_nvme_namespace:
        state: present
        ostype: linux
        path: /vol/ansible/test
        size: 20
        size_unit: mb
        vserver: "{{ vserver }}"
        hostname: "{{ hostname }}"
        username: "{{ username }}"
        password: "{{ password }}"
"""

RETURN = """
"""

import traceback
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native
import ansible_collections.netapp.ontap.plugins.module_utils.netapp as netapp_utils
from ansible_collections.netapp.ontap.plugins.module_utils.netapp_module import NetAppModule

HAS_NETAPP_LIB = netapp_utils.has_netapp_lib()


class NetAppONTAPNVMENamespace(object):
    """
    Class with NVME namespace methods
    """

    def __init__(self):

        self.argument_spec = netapp_utils.na_ontap_host_argument_spec()
        self.argument_spec.update(dict(
            state=dict(required=False, type='str', choices=['present', 'absent'], default='present'),
            vserver=dict(required=True, type='str'),
            ostype=dict(required=False, type='str', choices=['windows', 'linux', 'vmware', 'xen', 'hyper_v']),
            path=dict(required=True, type='str'),
            size=dict(required=False, type='int'),
            size_unit=dict(default='b', choices=['bytes', 'b', 'kb', 'mb', 'gb', 'tb', 'pb', 'eb', 'zb', 'yb'], type='str'),
            block_size=dict(required=False, choices=[512, 4096], type='int')
        ))

        self.module = AnsibleModule(
            argument_spec=self.argument_spec,
            required_if=[('state', 'present', ['ostype', 'size'])],
            supports_check_mode=True
        )

        self.na_helper = NetAppModule()
        self.parameters = self.na_helper.set_parameters(self.module.params)

        if self.parameters.get('size'):
            self.parameters['size'] = self.parameters['size'] * \
                netapp_utils.POW2_BYTE_MAP[self.parameters['size_unit']]

        if HAS_NETAPP_LIB is False:
            self.module.fail_json(msg="the python NetApp-Lib module is required")
        else:
            self.server = netapp_utils.setup_na_ontap_zapi(module=self.module, vserver=self.parameters['vserver'])

    def get_namespace(self):
        """
        Get current namespace details
        :return: dict if namespace exists, None otherwise
        """
        namespace_get = netapp_utils.zapi.NaElement('nvme-namespace-get-iter')
        query = {
            'query': {
                'nvme-namespace-info': {
                    'path': self.parameters['path'],
                    'vserver': self.parameters['vserver']
                }
            }
        }
        namespace_get.translate_struct(query)
        try:
            result = self.server.invoke_successfully(namespace_get, enable_tunneling=False)
        except netapp_utils.zapi.NaApiError as error:
            self.module.fail_json(msg='Error fetching namespace info: %s' % to_native(error),
                                  exception=traceback.format_exc())
        if result.get_child_by_name('num-records') and int(result.get_child_content('num-records')) >= 1:
            return result
        return None

    def create_namespace(self):
        """
        Create a NVME Namespace
        """
        options = {'path': self.parameters['path'],
                   'ostype': self.parameters['ostype'],
                   'size': self.parameters['size']
                   }
        if self.parameters.get('block_size'):
            options['block-size'] = self.parameters['block_size']
        namespace_create = netapp_utils.zapi.NaElement('nvme-namespace-create')
        namespace_create.translate_struct(options)
        try:
            self.server.invoke_successfully(namespace_create, enable_tunneling=True)
        except netapp_utils.zapi.NaApiError as error:
            self.module.fail_json(msg='Error creating namespace for path %s: %s'
                                  % (self.parameters.get('path'), to_native(error)),
                                  exception=traceback.format_exc())

    def delete_namespace(self):
        """
        Delete a NVME Namespace
        """
        options = {'path': self.parameters['path']
                   }
        namespace_delete = netapp_utils.zapi.NaElement.create_node_with_children('nvme-namespace-delete', **options)
        try:
            self.server.invoke_successfully(namespace_delete, enable_tunneling=True)
        except netapp_utils.zapi.NaApiError as error:
            self.module.fail_json(msg='Error deleting namespace for path %s: %s'
                                      % (self.parameters.get('path'), to_native(error)),
                                  exception=traceback.format_exc())

    def apply(self):
        """
        Apply action to NVME Namespace
        """
        netapp_utils.ems_log_event("na_ontap_nvme_namespace", self.server)
        current = self.get_namespace()
        cd_action = self.na_helper.get_cd_action(current, self.parameters)
        if self.na_helper.changed:
            if self.module.check_mode:
                pass
            else:
                if cd_action == 'create':
                    self.create_namespace()
                elif cd_action == 'delete':
                    self.delete_namespace()

        self.module.exit_json(changed=self.na_helper.changed)


def main():
    """Execute action"""
    community_obj = NetAppONTAPNVMENamespace()
    community_obj.apply()


if __name__ == '__main__':
    main()
