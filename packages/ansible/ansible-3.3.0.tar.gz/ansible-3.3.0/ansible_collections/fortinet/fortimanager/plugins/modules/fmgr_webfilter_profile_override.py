#!/usr/bin/python
from __future__ import absolute_import, division, print_function
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
module: fmgr_webfilter_profile_override
short_description: Web Filter override settings.
description:
    - This module is able to configure a FortiManager device.
    - Examples include all parameters and values which need to be adjusted to data sources before usage.

version_added: "2.10"
author:
    - Link Zheng (@chillancezen)
    - Jie Xue (@JieX19)
    - Frank Shen (@fshen01)
    - Hongbin Lu (@fgtdev-hblu)
notes:
    - Running in workspace locking mode is supported in this FortiManager module, the top
      level parameters workspace_locking_adom and workspace_locking_timeout help do the work.
    - To create or update an object, use state present directive.
    - To delete an object, use state absent directive.
    - Normally, running one module can fail when a non-zero rc is returned. you can also override
      the conditions to fail or succeed with parameters rc_failed and rc_succeeded

options:
    bypass_validation:
        description: only set to True when module schema diffs with FortiManager API structure, module continues to execute without validating parameters
        required: false
        type: bool
        default: false
    workspace_locking_adom:
        description: the adom to lock for FortiManager running in workspace mode, the value can be global and others including root
        required: false
        type: str
    workspace_locking_timeout:
        description: the maximum time in seconds to wait for other user to release the workspace lock
        required: false
        type: int
        default: 300
    state:
        description: the directive to create, update or delete an object
        type: str
        required: true
        choices:
          - present
          - absent
    rc_succeeded:
        description: the rc codes list with which the conditions to succeed will be overriden
        type: list
        required: false
    rc_failed:
        description: the rc codes list with which the conditions to fail will be overriden
        type: list
        required: false
    adom:
        description: the parameter (adom) in requested url
        type: str
        required: true
    profile:
        description: the parameter (profile) in requested url
        type: str
        required: true
    webfilter_profile_override:
        description: the top level parameters set
        required: false
        type: dict
        suboptions:
            ovrd-cookie:
                type: str
                description: 'Allow/deny browser-based (cookie) overrides.'
                choices:
                    - 'deny'
                    - 'allow'
            ovrd-dur:
                type: str
                description: 'Override duration.'
            ovrd-dur-mode:
                type: str
                description: 'Override duration mode.'
                choices:
                    - 'constant'
                    - 'ask'
            ovrd-scope:
                type: str
                description: 'Override scope.'
                choices:
                    - 'user'
                    - 'user-group'
                    - 'ip'
                    - 'ask'
                    - 'browser'
            ovrd-user-group:
                type: str
                description: 'User groups with permission to use the override.'
            profile:
                type: str
                description: 'Web filter profile with permission to create overrides.'
            profile-attribute:
                type: str
                description: 'Profile attribute to retrieve from the RADIUS server.'
                choices:
                    - 'User-Name'
                    - 'User-Password'
                    - 'CHAP-Password'
                    - 'NAS-IP-Address'
                    - 'NAS-Port'
                    - 'Service-Type'
                    - 'Framed-Protocol'
                    - 'Framed-IP-Address'
                    - 'Framed-IP-Netmask'
                    - 'Framed-Routing'
                    - 'Filter-Id'
                    - 'Framed-MTU'
                    - 'Framed-Compression'
                    - 'Login-IP-Host'
                    - 'Login-Service'
                    - 'Login-TCP-Port'
                    - 'Reply-Message'
                    - 'Callback-Number'
                    - 'Callback-Id'
                    - 'Framed-Route'
                    - 'Framed-IPX-Network'
                    - 'State'
                    - 'Class'
                    - 'Vendor-Specific'
                    - 'Session-Timeout'
                    - 'Idle-Timeout'
                    - 'Termination-Action'
                    - 'Called-Station-Id'
                    - 'Calling-Station-Id'
                    - 'NAS-Identifier'
                    - 'Proxy-State'
                    - 'Login-LAT-Service'
                    - 'Login-LAT-Node'
                    - 'Login-LAT-Group'
                    - 'Framed-AppleTalk-Link'
                    - 'Framed-AppleTalk-Network'
                    - 'Framed-AppleTalk-Zone'
                    - 'Acct-Status-Type'
                    - 'Acct-Delay-Time'
                    - 'Acct-Input-Octets'
                    - 'Acct-Output-Octets'
                    - 'Acct-Session-Id'
                    - 'Acct-Authentic'
                    - 'Acct-Session-Time'
                    - 'Acct-Input-Packets'
                    - 'Acct-Output-Packets'
                    - 'Acct-Terminate-Cause'
                    - 'Acct-Multi-Session-Id'
                    - 'Acct-Link-Count'
                    - 'CHAP-Challenge'
                    - 'NAS-Port-Type'
                    - 'Port-Limit'
                    - 'Login-LAT-Port'
            profile-type:
                type: str
                description: 'Override profile type.'
                choices:
                    - 'list'
                    - 'radius'

'''

EXAMPLES = '''
 - hosts: fortimanager-inventory
   collections:
     - fortinet.fortimanager
   connection: httpapi
   vars:
      ansible_httpapi_use_ssl: True
      ansible_httpapi_validate_certs: False
      ansible_httpapi_port: 443
   tasks:
    - name: Web Filter override settings.
      fmgr_webfilter_profile_override:
         bypass_validation: False
         workspace_locking_adom: <value in [global, custom adom including root]>
         workspace_locking_timeout: 300
         rc_succeeded: [0, -2, -3, ...]
         rc_failed: [-2, -3, ...]
         adom: <your own value>
         profile: <your own value>
         webfilter_profile_override:
            ovrd-cookie: <value in [deny, allow]>
            ovrd-dur: <value of string>
            ovrd-dur-mode: <value in [constant, ask]>
            ovrd-scope: <value in [user, user-group, ip, ...]>
            ovrd-user-group: <value of string>
            profile: <value of string>
            profile-attribute: <value in [User-Name, User-Password, CHAP-Password, ...]>
            profile-type: <value in [list, radius]>

'''

RETURN = '''
request_url:
    description: The full url requested
    returned: always
    type: str
    sample: /sys/login/user
response_code:
    description: The status of api request
    returned: always
    type: int
    sample: 0
response_message:
    description: The descriptive message of the api response
    type: str
    returned: always
    sample: OK.

'''
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.connection import Connection
from ansible_collections.fortinet.fortimanager.plugins.module_utils.napi import NAPIManager
from ansible_collections.fortinet.fortimanager.plugins.module_utils.napi import check_galaxy_version
from ansible_collections.fortinet.fortimanager.plugins.module_utils.napi import check_parameter_bypass


def main():
    jrpc_urls = [
        '/pm/config/adom/{adom}/obj/webfilter/profile/{profile}/override',
        '/pm/config/global/obj/webfilter/profile/{profile}/override'
    ]

    perobject_jrpc_urls = [
        '/pm/config/adom/{adom}/obj/webfilter/profile/{profile}/override/{override}',
        '/pm/config/global/obj/webfilter/profile/{profile}/override/{override}'
    ]

    url_params = ['adom', 'profile']
    module_primary_key = None
    module_arg_spec = {
        'bypass_validation': {
            'type': 'bool',
            'required': False,
            'default': False
        },
        'workspace_locking_adom': {
            'type': 'str',
            'required': False
        },
        'workspace_locking_timeout': {
            'type': 'int',
            'required': False,
            'default': 300
        },
        'rc_succeeded': {
            'required': False,
            'type': 'list'
        },
        'rc_failed': {
            'required': False,
            'type': 'list'
        },
        'adom': {
            'required': True,
            'type': 'str'
        },
        'profile': {
            'required': True,
            'type': 'str'
        },
        'webfilter_profile_override': {
            'required': False,
            'type': 'dict',
            'options': {
                'ovrd-cookie': {
                    'required': False,
                    'choices': [
                        'deny',
                        'allow'
                    ],
                    'type': 'str'
                },
                'ovrd-dur': {
                    'required': False,
                    'type': 'str'
                },
                'ovrd-dur-mode': {
                    'required': False,
                    'choices': [
                        'constant',
                        'ask'
                    ],
                    'type': 'str'
                },
                'ovrd-scope': {
                    'required': False,
                    'choices': [
                        'user',
                        'user-group',
                        'ip',
                        'ask',
                        'browser'
                    ],
                    'type': 'str'
                },
                'ovrd-user-group': {
                    'required': False,
                    'type': 'str'
                },
                'profile': {
                    'required': False,
                    'type': 'str'
                },
                'profile-attribute': {
                    'required': False,
                    'choices': [
                        'User-Name',
                        'User-Password',
                        'CHAP-Password',
                        'NAS-IP-Address',
                        'NAS-Port',
                        'Service-Type',
                        'Framed-Protocol',
                        'Framed-IP-Address',
                        'Framed-IP-Netmask',
                        'Framed-Routing',
                        'Filter-Id',
                        'Framed-MTU',
                        'Framed-Compression',
                        'Login-IP-Host',
                        'Login-Service',
                        'Login-TCP-Port',
                        'Reply-Message',
                        'Callback-Number',
                        'Callback-Id',
                        'Framed-Route',
                        'Framed-IPX-Network',
                        'State',
                        'Class',
                        'Vendor-Specific',
                        'Session-Timeout',
                        'Idle-Timeout',
                        'Termination-Action',
                        'Called-Station-Id',
                        'Calling-Station-Id',
                        'NAS-Identifier',
                        'Proxy-State',
                        'Login-LAT-Service',
                        'Login-LAT-Node',
                        'Login-LAT-Group',
                        'Framed-AppleTalk-Link',
                        'Framed-AppleTalk-Network',
                        'Framed-AppleTalk-Zone',
                        'Acct-Status-Type',
                        'Acct-Delay-Time',
                        'Acct-Input-Octets',
                        'Acct-Output-Octets',
                        'Acct-Session-Id',
                        'Acct-Authentic',
                        'Acct-Session-Time',
                        'Acct-Input-Packets',
                        'Acct-Output-Packets',
                        'Acct-Terminate-Cause',
                        'Acct-Multi-Session-Id',
                        'Acct-Link-Count',
                        'CHAP-Challenge',
                        'NAS-Port-Type',
                        'Port-Limit',
                        'Login-LAT-Port'
                    ],
                    'type': 'str'
                },
                'profile-type': {
                    'required': False,
                    'choices': [
                        'list',
                        'radius'
                    ],
                    'type': 'str'
                }
            }

        }
    }

    params_validation_blob = []
    check_galaxy_version(module_arg_spec)
    module = AnsibleModule(argument_spec=check_parameter_bypass(module_arg_spec, 'webfilter_profile_override'),
                           supports_check_mode=False)

    fmgr = None
    if module._socket_path:
        connection = Connection(module._socket_path)
        fmgr = NAPIManager(jrpc_urls, perobject_jrpc_urls, module_primary_key, url_params, module, connection, top_level_schema_name='data')
        fmgr.validate_parameters(params_validation_blob)
        fmgr.process_partial_curd()
    else:
        module.fail_json(msg='MUST RUN IN HTTPAPI MODE')
    module.exit_json(meta=module.params)


if __name__ == '__main__':
    main()
