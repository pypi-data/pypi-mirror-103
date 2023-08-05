#!/usr/bin/python
from __future__ import (absolute_import, division, print_function)
# Copyright 2019-2020 Fortinet, Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

__metaclass__ = type

ANSIBLE_METADATA = {'status': ['preview'],
                    'supported_by': 'community',
                    'metadata_version': '1.1'}

DOCUMENTATION = '''
---
module: fortios_system_nat64
short_description: Configure NAT64 in Fortinet's FortiOS and FortiGate.
description:
    - This module is able to configure a FortiGate or FortiOS (FOS) device by allowing the
      user to set and modify system feature and nat64 category.
      Examples include all parameters and values need to be adjusted to datasources before usage.
      Tested with FOS v6.0.0
version_added: "2.9"
author:
    - Link Zheng (@chillancezen)
    - Jie Xue (@JieX19)
    - Hongbin Lu (@fgtdev-hblu)
    - Frank Shen (@frankshen01)
    - Miguel Angel Munoz (@mamunozgonzalez)
    - Nicolas Thomas (@thomnico)
notes:
    - Legacy fortiosapi has been deprecated, httpapi is the preferred way to run playbooks

requirements:
    - ansible>=2.9.0
options:
    access_token:
        description:
            - Token-based authentication.
              Generated from GUI of Fortigate.
        type: str
        required: false
    vdom:
        description:
            - Virtual domain, among those defined previously. A vdom is a
              virtual instance of the FortiGate that can be configured and
              used as a different unit.
        type: str
        default: root

    system_nat64:
        description:
            - Configure NAT64.
        default: null
        type: dict
        suboptions:
            always_synthesize_aaaa_record:
                description:
                    - Enable/disable AAAA record synthesis .
                type: str
                choices:
                    - enable
                    - disable
            generate_ipv6_fragment_header:
                description:
                    - Enable/disable IPv6 fragment header generation.
                type: str
                choices:
                    - enable
                    - disable
            nat64_prefix:
                description:
                    - 'NAT64 prefix must be ::/96 .'
                type: str
            secondary_prefix:
                description:
                    - Secondary NAT64 prefix.
                type: list
                suboptions:
                    name:
                        description:
                            - NAT64 prefix name.
                        required: true
                        type: str
                    nat64_prefix:
                        description:
                            - NAT64 prefix.
                        type: str
            secondary_prefix_status:
                description:
                    - Enable/disable secondary NAT64 prefix.
                type: str
                choices:
                    - enable
                    - disable
            status:
                description:
                    - Enable/disable NAT64 .
                type: str
                choices:
                    - enable
                    - disable
'''

EXAMPLES = '''
- hosts: fortigates
  collections:
    - fortinet.fortios
  connection: httpapi
  vars:
   vdom: "root"
   ansible_httpapi_use_ssl: yes
   ansible_httpapi_validate_certs: no
   ansible_httpapi_port: 443
  tasks:
  - name: Configure NAT64.
    fortios_system_nat64:
      vdom:  "{{ vdom }}"
      system_nat64:
        always_synthesize_aaaa_record: "enable"
        generate_ipv6_fragment_header: "enable"
        nat64_prefix: "<your_own_value>"
        secondary_prefix:
         -
            name: "default_name_7"
            nat64_prefix: "<your_own_value>"
        secondary_prefix_status: "enable"
        status: "enable"

'''

RETURN = '''
build:
  description: Build number of the fortigate image
  returned: always
  type: str
  sample: '1547'
http_method:
  description: Last method used to provision the content into FortiGate
  returned: always
  type: str
  sample: 'PUT'
http_status:
  description: Last result given by FortiGate on last operation applied
  returned: always
  type: str
  sample: "200"
mkey:
  description: Master key (id) used in the last call to FortiGate
  returned: success
  type: str
  sample: "id"
name:
  description: Name of the table used to fulfill the request
  returned: always
  type: str
  sample: "urlfilter"
path:
  description: Path of the table used to fulfill the request
  returned: always
  type: str
  sample: "webfilter"
revision:
  description: Internal revision number
  returned: always
  type: str
  sample: "17.0.2.10658"
serial:
  description: Serial number of the unit
  returned: always
  type: str
  sample: "FGVMEVYYQT3AB5352"
status:
  description: Indication of the operation's result
  returned: always
  type: str
  sample: "success"
vdom:
  description: Virtual domain used
  returned: always
  type: str
  sample: "root"
version:
  description: Version of the FortiGate
  returned: always
  type: str
  sample: "v5.6.3"

'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.connection import Connection
from ansible_collections.fortinet.fortios.plugins.module_utils.fortios.fortios import FortiOSHandler
from ansible_collections.fortinet.fortios.plugins.module_utils.fortios.fortios import check_legacy_fortiosapi
from ansible_collections.fortinet.fortios.plugins.module_utils.fortimanager.common import FAIL_SOCKET_MSG


def filter_system_nat64_data(json):
    option_list = ['always_synthesize_aaaa_record', 'generate_ipv6_fragment_header', 'nat64_prefix',
                   'secondary_prefix', 'secondary_prefix_status', 'status']
    dictionary = {}

    for attribute in option_list:
        if attribute in json and json[attribute] is not None:
            dictionary[attribute] = json[attribute]

    return dictionary


def underscore_to_hyphen(data):
    if isinstance(data, list):
        for i, elem in enumerate(data):
            data[i] = underscore_to_hyphen(elem)
    elif isinstance(data, dict):
        new_data = {}
        for k, v in data.items():
            new_data[k.replace('_', '-')] = underscore_to_hyphen(v)
        data = new_data

    return data


def system_nat64(data, fos):
    vdom = data['vdom']
    system_nat64_data = data['system_nat64']
    filtered_data = underscore_to_hyphen(filter_system_nat64_data(system_nat64_data))

    return fos.set('system',
                   'nat64',
                   data=filtered_data,
                   vdom=vdom)


def is_successful_status(status):
    return status['status'] == "success" or \
        status['http_method'] == "DELETE" and status['http_status'] == 404


def fortios_system(data, fos):

    if data['system_nat64']:
        resp = system_nat64(data, fos)
    else:
        fos._module.fail_json(msg='missing task body: %s' % ('system_nat64'))

    return not is_successful_status(resp), \
        resp['status'] == "success" and \
        (resp['revision_changed'] if 'revision_changed' in resp else True), \
        resp


def main():
    mkeyname = None
    fields = {
        "access_token": {"required": False, "type": "str", "no_log": True},
        "vdom": {"required": False, "type": "str", "default": "root"},
        "system_nat64": {
            "required": False, "type": "dict", "default": None,
            "options": {
                "always_synthesize_aaaa_record": {"required": False, "type": "str",
                                                  "choices": ["enable",
                                                              "disable"]},
                "generate_ipv6_fragment_header": {"required": False, "type": "str",
                                                  "choices": ["enable",
                                                              "disable"]},
                "nat64_prefix": {"required": False, "type": "str"},
                "secondary_prefix": {"required": False, "type": "list",
                                     "options": {
                                         "name": {"required": True, "type": "str"},
                                         "nat64_prefix": {"required": False, "type": "str"}
                                     }},
                "secondary_prefix_status": {"required": False, "type": "str",
                                            "choices": ["enable",
                                                        "disable"]},
                "status": {"required": False, "type": "str",
                           "choices": ["enable",
                                       "disable"]}

            }
        }
    }

    check_legacy_fortiosapi()
    module = AnsibleModule(argument_spec=fields,
                           supports_check_mode=False)

    versions_check_result = None
    if module._socket_path:
        connection = Connection(module._socket_path)
        if 'access_token' in module.params:
            connection.set_option('access_token', module.params['access_token'])

        fos = FortiOSHandler(connection, module, mkeyname)

        is_error, has_changed, result = fortios_system(module.params, fos)
        versions_check_result = connection.get_system_version()
    else:
        module.fail_json(**FAIL_SOCKET_MSG)

    if versions_check_result and versions_check_result['matched'] is False:
        module.warn("Ansible has detected version mismatch between FortOS system and galaxy, see more details by specifying option -vvv")

    if not is_error:
        if versions_check_result and versions_check_result['matched'] is False:
            module.exit_json(changed=has_changed, version_check_warning=versions_check_result, meta=result)
        else:
            module.exit_json(changed=has_changed, meta=result)
    else:
        if versions_check_result and versions_check_result['matched'] is False:
            module.fail_json(msg="Error in repo", version_check_warning=versions_check_result, meta=result)
        else:
            module.fail_json(msg="Error in repo", meta=result)


if __name__ == '__main__':
    main()
