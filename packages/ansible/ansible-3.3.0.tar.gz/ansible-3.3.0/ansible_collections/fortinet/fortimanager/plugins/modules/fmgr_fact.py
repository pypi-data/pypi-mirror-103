#!/usr/bin/python
from __future__ import absolute_import, division, print_function
# Copyright 2020 Fortinet, Inc.
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
module: fmgr_fact
short_description: Gather fortimanager facts.
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
    rc_succeeded:
        description: the rc codes list with which the conditions to succeed will be overriden
        type: list
        required: false
    rc_failed:
        description: the rc codes list with which the conditions to fail will be overriden
        type: list
        required: false
    facts:
        description: the top level parameters set
        type: dict
        required: false
'''

EXAMPLES = '''
- name: gathering fortimanager facts
  hosts: fortimanager01
  gather_facts: no
  connection: httpapi
  collections:
    - fortinet.fortimanager
  vars:
    ansible_httpapi_use_ssl: True
    ansible_httpapi_validate_certs: False
    ansible_httpapi_port: 443
  tasks:
   - name: retrieve all the scripts
     fmgr_fact:
       facts:
           selector: 'dvmdb_script'
           params:
               adom: 'root'
               script: ''

   - name: retrive all the interfaces
     fmgr_fact:
       facts:
           selector: 'system_interface'
           params:
               interface: ''
   - name: retrieve the interface port1
     fmgr_fact:
       facts:
           selector: 'system_interface'
           params:
               interface: 'port1'
   - name: fetch urlfilter with name urlfilter4
     fmgr_fact:
       facts:
         selector: 'webfilter_urlfilter'
         params:
           adom: 'root'
           urlfilter: ''
         filter:
           -
             - 'name'
             - '=='
             - 'urlfilter4'
         fields:
           - 'id'
           - 'name'
           - 'comment'
         sortings:
           - 'id': 1
             'name': -1
   - name: Retrieve device
     fmgr_fact:
       facts:
         selector: 'dvmdb_device'
         params:
           adom: 'root'
           device: ''
         option:
           - 'get meta'
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


def main():
    facts_metadata = {
        'dnsfilter_domainfilter': {
            'params': [
                'domain-filter',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/dnsfilter/domain-filter/{domain-filter}',
                '/pm/config/global/obj/dnsfilter/domain-filter/{domain-filter}'
            ]
        },
        'dnsfilter_domainfilter_entries': {
            'params': [
                'domain-filter',
                'entries',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/dnsfilter/domain-filter/{domain-filter}/entries/{entries}',
                '/pm/config/global/obj/dnsfilter/domain-filter/{domain-filter}/entries/{entries}'
            ]
        },
        'dnsfilter_profile': {
            'params': [
                'profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/dnsfilter/profile/{profile}',
                '/pm/config/global/obj/dnsfilter/profile/{profile}'
            ]
        },
        'dnsfilter_profile_domainfilter': {
            'params': [
                'profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/dnsfilter/profile/{profile}/domain-filter',
                '/pm/config/global/obj/dnsfilter/profile/{profile}/domain-filter'
            ]
        },
        'dnsfilter_profile_ftgddns': {
            'params': [
                'profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/dnsfilter/profile/{profile}/ftgd-dns',
                '/pm/config/global/obj/dnsfilter/profile/{profile}/ftgd-dns'
            ]
        },
        'dnsfilter_profile_ftgddns_filters': {
            'params': [
                'profile',
                'filters',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/dnsfilter/profile/{profile}/ftgd-dns/filters/{filters}',
                '/pm/config/global/obj/dnsfilter/profile/{profile}/ftgd-dns/filters/{filters}'
            ]
        },
        'webproxy_forwardserver': {
            'params': [
                'forward-server',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/web-proxy/forward-server/{forward-server}',
                '/pm/config/global/obj/web-proxy/forward-server/{forward-server}'
            ]
        },
        'webproxy_forwardservergroup': {
            'params': [
                'forward-server-group',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/web-proxy/forward-server-group/{forward-server-group}',
                '/pm/config/global/obj/web-proxy/forward-server-group/{forward-server-group}'
            ]
        },
        'webproxy_forwardservergroup_serverlist': {
            'params': [
                'forward-server-group',
                'server-list',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/web-proxy/forward-server-group/{forward-server-group}/server-list/{server-list}',
                '/pm/config/global/obj/web-proxy/forward-server-group/{forward-server-group}/server-list/{server-list}'
            ]
        },
        'webproxy_profile': {
            'params': [
                'profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/web-proxy/profile/{profile}',
                '/pm/config/global/obj/web-proxy/profile/{profile}'
            ]
        },
        'webproxy_profile_headers': {
            'params': [
                'profile',
                'headers',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/web-proxy/profile/{profile}/headers/{headers}',
                '/pm/config/global/obj/web-proxy/profile/{profile}/headers/{headers}'
            ]
        },
        'webproxy_wisp': {
            'params': [
                'wisp',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/web-proxy/wisp/{wisp}',
                '/pm/config/global/obj/web-proxy/wisp/{wisp}'
            ]
        },
        'log_customfield': {
            'params': [
                'custom-field',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/log/custom-field/{custom-field}',
                '/pm/config/global/obj/log/custom-field/{custom-field}'
            ]
        },
        'fmupdate_customurllist': {
            'params': [
            ],
            'urls': [
                '/cli/global/fmupdate/custom-url-list'
            ]
        },
        'system_route6': {
            'params': [
                'route6'
            ],
            'urls': [
                '/cli/global/system/route6/{route6}'
            ]
        },
        'voip_profile': {
            'params': [
                'profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/voip/profile/{profile}',
                '/pm/config/global/obj/voip/profile/{profile}'
            ]
        },
        'voip_profile_sccp': {
            'params': [
                'profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/voip/profile/{profile}/sccp',
                '/pm/config/global/obj/voip/profile/{profile}/sccp'
            ]
        },
        'voip_profile_sip': {
            'params': [
                'profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/voip/profile/{profile}/sip',
                '/pm/config/global/obj/voip/profile/{profile}/sip'
            ]
        },
        'icap_profile': {
            'params': [
                'profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/icap/profile/{profile}',
                '/pm/config/global/obj/icap/profile/{profile}'
            ]
        },
        'icap_server': {
            'params': [
                'server',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/icap/server/{server}',
                '/pm/config/global/obj/icap/server/{server}'
            ]
        },
        'fmupdate_service': {
            'params': [
            ],
            'urls': [
                '/cli/global/fmupdate/service'
            ]
        },
        'fmupdate_serveraccesspriorities': {
            'params': [
            ],
            'urls': [
                '/cli/global/fmupdate/server-access-priorities'
            ]
        },
        'fmupdate_serveraccesspriorities_privateserver': {
            'params': [
                'private-server'
            ],
            'urls': [
                '/cli/global/fmupdate/server-access-priorities/private-server/{private-server}'
            ]
        },
        'dvmdb_device': {
            'params': [
                'device',
                'adom'
            ],
            'urls': [
                '/dvmdb/adom/{adom}/device/{device}',
                '/dvmdb/device/{device}'
            ]
        },
        'dvmdb_device_haslave': {
            'params': [
                'device',
                'ha_slave',
                'adom'
            ],
            'urls': [
                '/dvmdb/adom/{adom}/device/{device}/ha_slave/{ha_slave}',
                '/dvmdb/device/{device}/ha_slave/{ha_slave}'
            ]
        },
        'dvmdb_device_vdom': {
            'params': [
                'device',
                'vdom',
                'adom'
            ],
            'urls': [
                '/dvmdb/adom/{adom}/device/{device}/vdom/{vdom}',
                '/dvmdb/device/{device}/vdom/{vdom}'
            ]
        },
        'gtp_apn': {
            'params': [
                'apn',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/gtp/apn/{apn}',
                '/pm/config/global/obj/gtp/apn/{apn}'
            ]
        },
        'gtp_apngrp': {
            'params': [
                'apngrp',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/gtp/apngrp/{apngrp}',
                '/pm/config/global/obj/gtp/apngrp/{apngrp}'
            ]
        },
        'gtp_iewhitelist': {
            'params': [
                'ie-white-list',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/gtp/ie-white-list/{ie-white-list}',
                '/pm/config/global/obj/gtp/ie-white-list/{ie-white-list}'
            ]
        },
        'gtp_iewhitelist_entries': {
            'params': [
                'ie-white-list',
                'entries',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/gtp/ie-white-list/{ie-white-list}/entries/{entries}',
                '/pm/config/global/obj/gtp/ie-white-list/{ie-white-list}/entries/{entries}'
            ]
        },
        'gtp_messagefilterv0v1': {
            'params': [
                'message-filter-v0v1',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/gtp/message-filter-v0v1/{message-filter-v0v1}',
                '/pm/config/global/obj/gtp/message-filter-v0v1/{message-filter-v0v1}'
            ]
        },
        'gtp_messagefilterv2': {
            'params': [
                'message-filter-v2',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/gtp/message-filter-v2/{message-filter-v2}',
                '/pm/config/global/obj/gtp/message-filter-v2/{message-filter-v2}'
            ]
        },
        'gtp_tunnellimit': {
            'params': [
                'tunnel-limit',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/gtp/tunnel-limit/{tunnel-limit}',
                '/pm/config/global/obj/gtp/tunnel-limit/{tunnel-limit}'
            ]
        },
        'application_categories': {
            'params': [
                'categories',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/application/categories/{categories}',
                '/pm/config/global/obj/application/categories/{categories}'
            ]
        },
        'application_custom': {
            'params': [
                'custom',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/application/custom/{custom}',
                '/pm/config/global/obj/application/custom/{custom}'
            ]
        },
        'application_group': {
            'params': [
                'group',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/application/group/{group}',
                '/pm/config/global/obj/application/group/{group}'
            ]
        },
        'application_list': {
            'params': [
                'list',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/application/list/{list}',
                '/pm/config/global/obj/application/list/{list}'
            ]
        },
        'application_list_entries': {
            'params': [
                'list',
                'entries',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/application/list/{list}/entries/{entries}',
                '/pm/config/global/obj/application/list/{list}/entries/{entries}'
            ]
        },
        'application_list_entries_parameters': {
            'params': [
                'list',
                'entries',
                'parameters',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/application/list/{list}/entries/{entries}/parameters/{parameters}',
                '/pm/config/global/obj/application/list/{list}/entries/{entries}/parameters/{parameters}'
            ]
        },
        'vpn_certificate_ca': {
            'params': [
                'ca',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/vpn/certificate/ca/{ca}',
                '/pm/config/global/obj/vpn/certificate/ca/{ca}'
            ]
        },
        'vpn_certificate_ocspserver': {
            'params': [
                'ocsp-server',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/vpn/certificate/ocsp-server/{ocsp-server}',
                '/pm/config/global/obj/vpn/certificate/ocsp-server/{ocsp-server}'
            ]
        },
        'vpn_certificate_remote': {
            'params': [
                'remote',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/vpn/certificate/remote/{remote}',
                '/pm/config/global/obj/vpn/certificate/remote/{remote}'
            ]
        },
        'vpnsslweb_hostchecksoftware': {
            'params': [
                'host-check-software',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/vpn/ssl/web/host-check-software/{host-check-software}',
                '/pm/config/global/obj/vpn/ssl/web/host-check-software/{host-check-software}'
            ]
        },
        'vpnsslweb_hostchecksoftware_checkitemlist': {
            'params': [
                'host-check-software',
                'check-item-list',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/vpn/ssl/web/host-check-software/{host-check-software}/check-item-list/{check-item-list}',
                '/pm/config/global/obj/vpn/ssl/web/host-check-software/{host-check-software}/check-item-list/{check-item-list}'
            ]
        },
        'vpnsslweb_portal': {
            'params': [
                'portal',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/vpn/ssl/web/portal/{portal}',
                '/pm/config/global/obj/vpn/ssl/web/portal/{portal}'
            ]
        },
        'vpnsslweb_portal_bookmarkgroup': {
            'params': [
                'portal',
                'bookmark-group',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/vpn/ssl/web/portal/{portal}/bookmark-group/{bookmark-group}',
                '/pm/config/global/obj/vpn/ssl/web/portal/{portal}/bookmark-group/{bookmark-group}'
            ]
        },
        'vpnsslweb_portal_bookmarkgroup_bookmarks': {
            'params': [
                'portal',
                'bookmark-group',
                'bookmarks',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/vpn/ssl/web/portal/{portal}/bookmark-group/{bookmark-group}/bookmarks/{bookmarks}',
                '/pm/config/global/obj/vpn/ssl/web/portal/{portal}/bookmark-group/{bookmark-group}/bookmarks/{bookmarks}'
            ]
        },
        'vpnsslweb_portal_bookmarkgroup_bookmarks_formdata': {
            'params': [
                'portal',
                'bookmark-group',
                'bookmarks',
                'form-data',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/vpn/ssl/web/portal/{portal}/bookmark-group/{bookmark-group}/bookmarks/{bookmarks}/form-data/{form-data}',
                '/pm/config/global/obj/vpn/ssl/web/portal/{portal}/bookmark-group/{bookmark-group}/bookmarks/{bookmarks}/form-data/{form-data}'
            ]
        },
        'vpnsslweb_portal_macaddrcheckrule': {
            'params': [
                'portal',
                'mac-addr-check-rule',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/vpn/ssl/web/portal/{portal}/mac-addr-check-rule/{mac-addr-check-rule}',
                '/pm/config/global/obj/vpn/ssl/web/portal/{portal}/mac-addr-check-rule/{mac-addr-check-rule}'
            ]
        },
        'vpnsslweb_portal_oschecklist': {
            'params': [
                'portal',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/vpn/ssl/web/portal/{portal}/os-check-list',
                '/pm/config/global/obj/vpn/ssl/web/portal/{portal}/os-check-list'
            ]
        },
        'vpnsslweb_portal_splitdns': {
            'params': [
                'portal',
                'split-dns',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/vpn/ssl/web/portal/{portal}/split-dns/{split-dns}',
                '/pm/config/global/obj/vpn/ssl/web/portal/{portal}/split-dns/{split-dns}'
            ]
        },
        'vpnsslweb_realm': {
            'params': [
                'realm',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/vpn/ssl/web/realm/{realm}',
                '/pm/config/global/obj/vpn/ssl/web/realm/{realm}'
            ]
        },
        'pkg_firewall_centralsnatmap': {
            'params': [
                'pkg',
                'central-snat-map',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/pkg/{pkg}/firewall/central-snat-map/{central-snat-map}'
            ]
        },
        'pkg_firewall_dospolicy': {
            'params': [
                'pkg',
                'DoS-policy',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/pkg/{pkg}/firewall/DoS-policy/{DoS-policy}'
            ]
        },
        'pkg_firewall_dospolicy_anomaly': {
            'params': [
                'pkg',
                'DoS-policy',
                'anomaly',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/pkg/{pkg}/firewall/DoS-policy/{DoS-policy}/anomaly/{anomaly}'
            ]
        },
        'pkg_firewall_dospolicy6': {
            'params': [
                'pkg',
                'DoS-policy6',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/pkg/{pkg}/firewall/DoS-policy6/{DoS-policy6}'
            ]
        },
        'pkg_firewall_dospolicy6_anomaly': {
            'params': [
                'pkg',
                'DoS-policy6',
                'anomaly',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/pkg/{pkg}/firewall/DoS-policy6/{DoS-policy6}/anomaly/{anomaly}'
            ]
        },
        'pkg_firewall_interfacepolicy': {
            'params': [
                'pkg',
                'interface-policy',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/pkg/{pkg}/firewall/interface-policy/{interface-policy}'
            ]
        },
        'pkg_firewall_interfacepolicy6': {
            'params': [
                'pkg',
                'interface-policy6',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/pkg/{pkg}/firewall/interface-policy6/{interface-policy6}'
            ]
        },
        'pkg_firewall_localinpolicy': {
            'params': [
                'pkg',
                'local-in-policy',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/pkg/{pkg}/firewall/local-in-policy/{local-in-policy}'
            ]
        },
        'pkg_firewall_localinpolicy6': {
            'params': [
                'pkg',
                'local-in-policy6',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/pkg/{pkg}/firewall/local-in-policy6/{local-in-policy6}'
            ]
        },
        'pkg_firewall_multicastpolicy': {
            'params': [
                'pkg',
                'multicast-policy',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/pkg/{pkg}/firewall/multicast-policy/{multicast-policy}'
            ]
        },
        'pkg_firewall_multicastpolicy6': {
            'params': [
                'pkg',
                'multicast-policy6',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/pkg/{pkg}/firewall/multicast-policy6/{multicast-policy6}'
            ]
        },
        'pkg_firewall_policy': {
            'params': [
                'pkg',
                'policy',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/pkg/{pkg}/firewall/policy/{policy}'
            ]
        },
        'pkg_firewall_policy_vpndstnode': {
            'params': [
                'pkg',
                'policy',
                'vpn_dst_node',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/pkg/{pkg}/firewall/policy/{policy}/vpn_dst_node/{vpn_dst_node}'
            ]
        },
        'pkg_firewall_policy_vpnsrcnode': {
            'params': [
                'pkg',
                'policy',
                'vpn_src_node',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/pkg/{pkg}/firewall/policy/{policy}/vpn_src_node/{vpn_src_node}'
            ]
        },
        'pkg_firewall_policy46': {
            'params': [
                'pkg',
                'policy46',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/pkg/{pkg}/firewall/policy46/{policy46}'
            ]
        },
        'pkg_firewall_policy6': {
            'params': [
                'pkg',
                'policy6',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/pkg/{pkg}/firewall/policy6/{policy6}'
            ]
        },
        'pkg_firewall_policy64': {
            'params': [
                'pkg',
                'policy64',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/pkg/{pkg}/firewall/policy64/{policy64}'
            ]
        },
        'pkg_firewall_proxypolicy': {
            'params': [
                'pkg',
                'proxy-policy',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/pkg/{pkg}/firewall/proxy-policy/{proxy-policy}'
            ]
        },
        'pkg_firewall_shapingpolicy': {
            'params': [
                'pkg',
                'shaping-policy',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/pkg/{pkg}/firewall/shaping-policy/{shaping-policy}'
            ]
        },
        'dvmdb_revision': {
            'params': [
                'revision',
                'adom'
            ],
            'urls': [
                '/dvmdb/adom/{adom}/revision/{revision}',
                '/dvmdb/global/revision/{revision}',
                '/dvmdb/revision/{revision}'
            ]
        },
        'system_ha': {
            'params': [
            ],
            'urls': [
                '/cli/global/system/ha'
            ]
        },
        'system_ha_peer': {
            'params': [
                'peer'
            ],
            'urls': [
                '/cli/global/system/ha/peer/{peer}'
            ]
        },
        'system_admin_group': {
            'params': [
                'group'
            ],
            'urls': [
                '/cli/global/system/admin/group/{group}'
            ]
        },
        'system_admin_group_member': {
            'params': [
                'group',
                'member'
            ],
            'urls': [
                '/cli/global/system/admin/group/{group}/member/{member}'
            ]
        },
        'system_admin_ldap': {
            'params': [
                'ldap'
            ],
            'urls': [
                '/cli/global/system/admin/ldap/{ldap}'
            ]
        },
        'system_admin_ldap_adom': {
            'params': [
                'ldap',
                'adom'
            ],
            'urls': [
                '/cli/global/system/admin/ldap/{ldap}/adom/{adom}'
            ]
        },
        'system_admin_profile': {
            'params': [
                'profile'
            ],
            'urls': [
                '/cli/global/system/admin/profile/{profile}'
            ]
        },
        'system_admin_profile_datamaskcustomfields': {
            'params': [
                'profile',
                'datamask-custom-fields'
            ],
            'urls': [
                '/cli/global/system/admin/profile/{profile}/datamask-custom-fields/{datamask-custom-fields}'
            ]
        },
        'system_admin_radius': {
            'params': [
                'radius'
            ],
            'urls': [
                '/cli/global/system/admin/radius/{radius}'
            ]
        },
        'system_admin_setting': {
            'params': [
            ],
            'urls': [
                '/cli/global/system/admin/setting'
            ]
        },
        'system_admin_tacacs': {
            'params': [
                'tacacs'
            ],
            'urls': [
                '/cli/global/system/admin/tacacs/{tacacs}'
            ]
        },
        'system_admin_user': {
            'params': [
                'user'
            ],
            'urls': [
                '/cli/global/system/admin/user/{user}'
            ]
        },
        'system_admin_user_adom': {
            'params': [
                'user',
                'adom'
            ],
            'urls': [
                '/cli/global/system/admin/user/{user}/adom/{adom}'
            ]
        },
        'system_admin_user_adomexclude': {
            'params': [
                'user',
                'adom-exclude'
            ],
            'urls': [
                '/cli/global/system/admin/user/{user}/adom-exclude/{adom-exclude}'
            ]
        },
        'system_admin_user_appfilter': {
            'params': [
                'user',
                'app-filter'
            ],
            'urls': [
                '/cli/global/system/admin/user/{user}/app-filter/{app-filter}'
            ]
        },
        'system_admin_user_dashboard': {
            'params': [
                'user',
                'dashboard'
            ],
            'urls': [
                '/cli/global/system/admin/user/{user}/dashboard/{dashboard}'
            ]
        },
        'system_admin_user_dashboardtabs': {
            'params': [
                'user',
                'dashboard-tabs'
            ],
            'urls': [
                '/cli/global/system/admin/user/{user}/dashboard-tabs/{dashboard-tabs}'
            ]
        },
        'system_admin_user_ipsfilter': {
            'params': [
                'user',
                'ips-filter'
            ],
            'urls': [
                '/cli/global/system/admin/user/{user}/ips-filter/{ips-filter}'
            ]
        },
        'system_admin_user_metadata': {
            'params': [
                'user',
                'meta-data'
            ],
            'urls': [
                '/cli/global/system/admin/user/{user}/meta-data/{meta-data}'
            ]
        },
        'system_admin_user_policypackage': {
            'params': [
                'user',
                'policy-package'
            ],
            'urls': [
                '/cli/global/system/admin/user/{user}/policy-package/{policy-package}'
            ]
        },
        'system_admin_user_restrictdevvdom': {
            'params': [
                'user',
                'restrict-dev-vdom'
            ],
            'urls': [
                '/cli/global/system/admin/user/{user}/restrict-dev-vdom/{restrict-dev-vdom}'
            ]
        },
        'system_admin_user_webfilter': {
            'params': [
                'user',
                'web-filter'
            ],
            'urls': [
                '/cli/global/system/admin/user/{user}/web-filter/{web-filter}'
            ]
        },
        'system_workflow_approvalmatrix': {
            'params': [
                'approval-matrix'
            ],
            'urls': [
                '/cli/global/system/workflow/approval-matrix/{approval-matrix}'
            ]
        },
        'system_workflow_approvalmatrix_approver': {
            'params': [
                'approval-matrix',
                'approver'
            ],
            'urls': [
                '/cli/global/system/workflow/approval-matrix/{approval-matrix}/approver/{approver}'
            ]
        },
        'system_syslog': {
            'params': [
                'syslog'
            ],
            'urls': [
                '/cli/global/system/syslog/{syslog}'
            ]
        },
        'fmupdate_analyzer_virusreport': {
            'params': [
            ],
            'urls': [
                '/cli/global/fmupdate/analyzer/virusreport'
            ]
        },
        'sys_ha_status': {
            'params': [
            ],
            'urls': [
                '/sys/ha/status'
            ]
        },
        'system_log_alert': {
            'params': [
            ],
            'urls': [
                '/cli/global/system/log/alert'
            ]
        },
        'system_log_ioc': {
            'params': [
            ],
            'urls': [
                '/cli/global/system/log/ioc'
            ]
        },
        'system_log_maildomain': {
            'params': [
                'mail-domain'
            ],
            'urls': [
                '/cli/global/system/log/mail-domain/{mail-domain}'
            ]
        },
        'system_log_settings': {
            'params': [
            ],
            'urls': [
                '/cli/global/system/log/settings'
            ]
        },
        'system_log_settings_rollinganalyzer': {
            'params': [
            ],
            'urls': [
                '/cli/global/system/log/settings/rolling-analyzer'
            ]
        },
        'system_log_settings_rollinglocal': {
            'params': [
            ],
            'urls': [
                '/cli/global/system/log/settings/rolling-local'
            ]
        },
        'system_log_settings_rollingregular': {
            'params': [
            ],
            'urls': [
                '/cli/global/system/log/settings/rolling-regular'
            ]
        },
        'pkg_central_dnat': {
            'params': [
                'pkg',
                'dnat',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/pkg/{pkg}/central/dnat/{dnat}'
            ]
        },
        'user_adgrp': {
            'params': [
                'adgrp',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/user/adgrp/{adgrp}',
                '/pm/config/global/obj/user/adgrp/{adgrp}'
            ]
        },
        'user_device': {
            'params': [
                'device',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/user/device/{device}',
                '/pm/config/global/obj/user/device/{device}'
            ]
        },
        'user_devicecategory': {
            'params': [
                'device-category',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/user/device-category/{device-category}',
                '/pm/config/global/obj/user/device-category/{device-category}'
            ]
        },
        'user_devicegroup': {
            'params': [
                'device-group',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/user/device-group/{device-group}',
                '/pm/config/global/obj/user/device-group/{device-group}'
            ]
        },
        'user_devicegroup_dynamicmapping': {
            'params': [
                'device-group',
                'dynamic_mapping',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/user/device-group/{device-group}/dynamic_mapping/{dynamic_mapping}',
                '/pm/config/global/obj/user/device-group/{device-group}/dynamic_mapping/{dynamic_mapping}'
            ]
        },
        'user_devicegroup_tagging': {
            'params': [
                'device-group',
                'tagging',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/user/device-group/{device-group}/tagging/{tagging}',
                '/pm/config/global/obj/user/device-group/{device-group}/tagging/{tagging}'
            ]
        },
        'user_device_dynamicmapping': {
            'params': [
                'device',
                'dynamic_mapping',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/user/device/{device}/dynamic_mapping/{dynamic_mapping}',
                '/pm/config/global/obj/user/device/{device}/dynamic_mapping/{dynamic_mapping}'
            ]
        },
        'user_device_tagging': {
            'params': [
                'device',
                'tagging',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/user/device/{device}/tagging/{tagging}',
                '/pm/config/global/obj/user/device/{device}/tagging/{tagging}'
            ]
        },
        'user_fortitoken': {
            'params': [
                'fortitoken',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/user/fortitoken/{fortitoken}',
                '/pm/config/global/obj/user/fortitoken/{fortitoken}'
            ]
        },
        'user_fsso': {
            'params': [
                'fsso',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/user/fsso/{fsso}',
                '/pm/config/global/obj/user/fsso/{fsso}'
            ]
        },
        'user_fssopolling': {
            'params': [
                'fsso-polling',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/user/fsso-polling/{fsso-polling}',
                '/pm/config/global/obj/user/fsso-polling/{fsso-polling}'
            ]
        },
        'user_fssopolling_adgrp': {
            'params': [
                'fsso-polling',
                'adgrp',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/user/fsso-polling/{fsso-polling}/adgrp/{adgrp}',
                '/pm/config/global/obj/user/fsso-polling/{fsso-polling}/adgrp/{adgrp}'
            ]
        },
        'user_fsso_dynamicmapping': {
            'params': [
                'fsso',
                'dynamic_mapping',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/user/fsso/{fsso}/dynamic_mapping/{dynamic_mapping}',
                '/pm/config/global/obj/user/fsso/{fsso}/dynamic_mapping/{dynamic_mapping}'
            ]
        },
        'user_group': {
            'params': [
                'group',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/user/group/{group}',
                '/pm/config/global/obj/user/group/{group}'
            ]
        },
        'user_group_guest': {
            'params': [
                'group',
                'guest',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/user/group/{group}/guest/{guest}',
                '/pm/config/global/obj/user/group/{group}/guest/{guest}'
            ]
        },
        'user_group_match': {
            'params': [
                'group',
                'match',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/user/group/{group}/match/{match}',
                '/pm/config/global/obj/user/group/{group}/match/{match}'
            ]
        },
        'user_ldap': {
            'params': [
                'ldap',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/user/ldap/{ldap}',
                '/pm/config/global/obj/user/ldap/{ldap}'
            ]
        },
        'user_ldap_dynamicmapping': {
            'params': [
                'ldap',
                'dynamic_mapping',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/user/ldap/{ldap}/dynamic_mapping/{dynamic_mapping}',
                '/pm/config/global/obj/user/ldap/{ldap}/dynamic_mapping/{dynamic_mapping}'
            ]
        },
        'user_local': {
            'params': [
                'local',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/user/local/{local}',
                '/pm/config/global/obj/user/local/{local}'
            ]
        },
        'user_passwordpolicy': {
            'params': [
                'password-policy',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/user/password-policy/{password-policy}',
                '/pm/config/global/obj/user/password-policy/{password-policy}'
            ]
        },
        'user_peer': {
            'params': [
                'peer',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/user/peer/{peer}',
                '/pm/config/global/obj/user/peer/{peer}'
            ]
        },
        'user_peergrp': {
            'params': [
                'peergrp',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/user/peergrp/{peergrp}',
                '/pm/config/global/obj/user/peergrp/{peergrp}'
            ]
        },
        'user_pop3': {
            'params': [
                'pop3',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/user/pop3/{pop3}',
                '/pm/config/global/obj/user/pop3/{pop3}'
            ]
        },
        'user_pxgrid': {
            'params': [
                'pxgrid',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/user/pxgrid/{pxgrid}',
                '/pm/config/global/obj/user/pxgrid/{pxgrid}'
            ]
        },
        'user_radius': {
            'params': [
                'radius',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/user/radius/{radius}',
                '/pm/config/global/obj/user/radius/{radius}'
            ]
        },
        'user_radius_accountingserver': {
            'params': [
                'radius',
                'accounting-server',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/user/radius/{radius}/accounting-server/{accounting-server}',
                '/pm/config/global/obj/user/radius/{radius}/accounting-server/{accounting-server}'
            ]
        },
        'user_radius_dynamicmapping': {
            'params': [
                'radius',
                'dynamic_mapping',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/user/radius/{radius}/dynamic_mapping/{dynamic_mapping}',
                '/pm/config/global/obj/user/radius/{radius}/dynamic_mapping/{dynamic_mapping}'
            ]
        },
        'user_securityexemptlist': {
            'params': [
                'security-exempt-list',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/user/security-exempt-list/{security-exempt-list}',
                '/pm/config/global/obj/user/security-exempt-list/{security-exempt-list}'
            ]
        },
        'user_securityexemptlist_rule': {
            'params': [
                'security-exempt-list',
                'rule',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/user/security-exempt-list/{security-exempt-list}/rule/{rule}',
                '/pm/config/global/obj/user/security-exempt-list/{security-exempt-list}/rule/{rule}'
            ]
        },
        'user_tacacs': {
            'params': [
                'tacacs+',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/user/tacacs+/{tacacs+}',
                '/pm/config/global/obj/user/tacacs+/{tacacs+}'
            ]
        },
        'user_tacacs_dynamicmapping': {
            'params': [
                'tacacs+',
                'dynamic_mapping',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/user/tacacs+/{tacacs+}/dynamic_mapping/{dynamic_mapping}',
                '/pm/config/global/obj/user/tacacs+/{tacacs+}/dynamic_mapping/{dynamic_mapping}'
            ]
        },
        'system_snmp_community': {
            'params': [
                'community'
            ],
            'urls': [
                '/cli/global/system/snmp/community/{community}'
            ]
        },
        'system_snmp_community_hosts': {
            'params': [
                'community',
                'hosts'
            ],
            'urls': [
                '/cli/global/system/snmp/community/{community}/hosts/{hosts}'
            ]
        },
        'system_snmp_community_hosts6': {
            'params': [
                'community',
                'hosts6'
            ],
            'urls': [
                '/cli/global/system/snmp/community/{community}/hosts6/{hosts6}'
            ]
        },
        'system_snmp_sysinfo': {
            'params': [
            ],
            'urls': [
                '/cli/global/system/snmp/sysinfo'
            ]
        },
        'system_snmp_user': {
            'params': [
                'user'
            ],
            'urls': [
                '/cli/global/system/snmp/user/{user}'
            ]
        },
        'pm_devprof_adom': {
            'params': [
                'adom'
            ],
            'urls': [
                '/pm/devprof/adom/{adom}'
            ]
        },
        'pm_devprof': {
            'params': [
                'pkg_path',
                'adom'
            ],
            'urls': [
                '/pm/devprof/adom/{adom}/{pkg_path}'
            ]
        },
        'system_route': {
            'params': [
                'route'
            ],
            'urls': [
                '/cli/global/system/route/{route}'
            ]
        },
        'system_connector': {
            'params': [
            ],
            'urls': [
                '/cli/global/system/connector'
            ]
        },
        'devprof_device_profile_fortianalyzer': {
            'params': [
                'devprof',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/devprof/{devprof}/device/profile/fortianalyzer'
            ]
        },
        'devprof_device_profile_fortiguard': {
            'params': [
                'devprof',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/devprof/{devprof}/device/profile/fortiguard'
            ]
        },
        'system_performance': {
            'params': [
            ],
            'urls': [
                '/cli/global/system/performance'
            ]
        },
        'system_dns': {
            'params': [
            ],
            'urls': [
                '/cli/global/system/dns'
            ]
        },
        'system_fortiview_autocache': {
            'params': [
            ],
            'urls': [
                '/cli/global/system/fortiview/auto-cache'
            ]
        },
        'system_fortiview_setting': {
            'params': [
            ],
            'urls': [
                '/cli/global/system/fortiview/setting'
            ]
        },
        'pm_pkg_schedule': {
            'params': [
                'pkg_name_path',
                'adom'
            ],
            'urls': [
                '/pm/pkg/adom/{adom}/{pkg_name_path}/schedule',
                '/pm/pkg/global/{pkg_name_path}/schedule'
            ]
        },
        'webfilter_categories': {
            'params': [
                'categories',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/webfilter/categories/{categories}',
                '/pm/config/global/obj/webfilter/categories/{categories}'
            ]
        },
        'webfilter_content': {
            'params': [
                'content',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/webfilter/content/{content}',
                '/pm/config/global/obj/webfilter/content/{content}'
            ]
        },
        'webfilter_contentheader': {
            'params': [
                'content-header',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/webfilter/content-header/{content-header}',
                '/pm/config/global/obj/webfilter/content-header/{content-header}'
            ]
        },
        'webfilter_contentheader_entries': {
            'params': [
                'content-header',
                'entries',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/webfilter/content-header/{content-header}/entries/{entries}',
                '/pm/config/global/obj/webfilter/content-header/{content-header}/entries/{entries}'
            ]
        },
        'webfilter_content_entries': {
            'params': [
                'content',
                'entries',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/webfilter/content/{content}/entries/{entries}',
                '/pm/config/global/obj/webfilter/content/{content}/entries/{entries}'
            ]
        },
        'webfilter_ftgdlocalcat': {
            'params': [
                'ftgd-local-cat',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/webfilter/ftgd-local-cat/{ftgd-local-cat}',
                '/pm/config/global/obj/webfilter/ftgd-local-cat/{ftgd-local-cat}'
            ]
        },
        'webfilter_ftgdlocalrating': {
            'params': [
                'ftgd-local-rating',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/webfilter/ftgd-local-rating/{ftgd-local-rating}',
                '/pm/config/global/obj/webfilter/ftgd-local-rating/{ftgd-local-rating}'
            ]
        },
        'webfilter_profile': {
            'params': [
                'profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/webfilter/profile/{profile}',
                '/pm/config/global/obj/webfilter/profile/{profile}'
            ]
        },
        'webfilter_profile_ftgdwf': {
            'params': [
                'profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/webfilter/profile/{profile}/ftgd-wf',
                '/pm/config/global/obj/webfilter/profile/{profile}/ftgd-wf'
            ]
        },
        'webfilter_profile_ftgdwf_filters': {
            'params': [
                'profile',
                'filters',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/webfilter/profile/{profile}/ftgd-wf/filters/{filters}',
                '/pm/config/global/obj/webfilter/profile/{profile}/ftgd-wf/filters/{filters}'
            ]
        },
        'webfilter_profile_ftgdwf_quota': {
            'params': [
                'profile',
                'quota',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/webfilter/profile/{profile}/ftgd-wf/quota/{quota}',
                '/pm/config/global/obj/webfilter/profile/{profile}/ftgd-wf/quota/{quota}'
            ]
        },
        'webfilter_profile_override': {
            'params': [
                'profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/webfilter/profile/{profile}/override',
                '/pm/config/global/obj/webfilter/profile/{profile}/override'
            ]
        },
        'webfilter_profile_urlextraction': {
            'params': [
                'profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/webfilter/profile/{profile}/url-extraction',
                '/pm/config/global/obj/webfilter/profile/{profile}/url-extraction'
            ]
        },
        'webfilter_profile_web': {
            'params': [
                'profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/webfilter/profile/{profile}/web',
                '/pm/config/global/obj/webfilter/profile/{profile}/web'
            ]
        },
        'webfilter_profile_youtubechannelfilter': {
            'params': [
                'profile',
                'youtube-channel-filter',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/webfilter/profile/{profile}/youtube-channel-filter/{youtube-channel-filter}',
                '/pm/config/global/obj/webfilter/profile/{profile}/youtube-channel-filter/{youtube-channel-filter}'
            ]
        },
        'webfilter_urlfilter': {
            'params': [
                'urlfilter',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/webfilter/urlfilter/{urlfilter}',
                '/pm/config/global/obj/webfilter/urlfilter/{urlfilter}'
            ]
        },
        'webfilter_urlfilter_entries': {
            'params': [
                'urlfilter',
                'entries',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/webfilter/urlfilter/{urlfilter}/entries/{entries}',
                '/pm/config/global/obj/webfilter/urlfilter/{urlfilter}/entries/{entries}'
            ]
        },
        'fmupdate_webspam_fgdsetting': {
            'params': [
            ],
            'urls': [
                '/cli/global/fmupdate/web-spam/fgd-setting'
            ]
        },
        'fmupdate_webspam_fgdsetting_serveroverride': {
            'params': [
            ],
            'urls': [
                '/cli/global/fmupdate/web-spam/fgd-setting/server-override'
            ]
        },
        'fmupdate_webspam_fgdsetting_serveroverride_servlist': {
            'params': [
                'servlist'
            ],
            'urls': [
                '/cli/global/fmupdate/web-spam/fgd-setting/server-override/servlist/{servlist}'
            ]
        },
        'fmupdate_webspam_webproxy': {
            'params': [
            ],
            'urls': [
                '/cli/global/fmupdate/web-spam/web-proxy'
            ]
        },
        'system_fips': {
            'params': [
            ],
            'urls': [
                '/cli/global/system/fips'
            ]
        },
        'fmupdate_avips_advancedlog': {
            'params': [
            ],
            'urls': [
                '/cli/global/fmupdate/av-ips/advanced-log'
            ]
        },
        'fmupdate_avips_webproxy': {
            'params': [
            ],
            'urls': [
                '/cli/global/fmupdate/av-ips/web-proxy'
            ]
        },
        'sys_status': {
            'params': [
            ],
            'urls': [
                '/sys/status'
            ]
        },
        'wanopt_authgroup': {
            'params': [
                'auth-group',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/wanopt/auth-group/{auth-group}',
                '/pm/config/global/obj/wanopt/auth-group/{auth-group}'
            ]
        },
        'wanopt_peer': {
            'params': [
                'peer',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/wanopt/peer/{peer}',
                '/pm/config/global/obj/wanopt/peer/{peer}'
            ]
        },
        'wanopt_profile': {
            'params': [
                'profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/wanopt/profile/{profile}',
                '/pm/config/global/obj/wanopt/profile/{profile}'
            ]
        },
        'wanopt_profile_cifs': {
            'params': [
                'profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/wanopt/profile/{profile}/cifs',
                '/pm/config/global/obj/wanopt/profile/{profile}/cifs'
            ]
        },
        'wanopt_profile_ftp': {
            'params': [
                'profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/wanopt/profile/{profile}/ftp',
                '/pm/config/global/obj/wanopt/profile/{profile}/ftp'
            ]
        },
        'wanopt_profile_http': {
            'params': [
                'profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/wanopt/profile/{profile}/http',
                '/pm/config/global/obj/wanopt/profile/{profile}/http'
            ]
        },
        'wanopt_profile_mapi': {
            'params': [
                'profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/wanopt/profile/{profile}/mapi',
                '/pm/config/global/obj/wanopt/profile/{profile}/mapi'
            ]
        },
        'wanopt_profile_tcp': {
            'params': [
                'profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/wanopt/profile/{profile}/tcp',
                '/pm/config/global/obj/wanopt/profile/{profile}/tcp'
            ]
        },
        'ips_custom': {
            'params': [
                'custom',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/ips/custom/{custom}',
                '/pm/config/global/obj/ips/custom/{custom}'
            ]
        },
        'ips_sensor': {
            'params': [
                'sensor',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/ips/sensor/{sensor}',
                '/pm/config/global/obj/ips/sensor/{sensor}'
            ]
        },
        'ips_sensor_entries': {
            'params': [
                'sensor',
                'entries',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/ips/sensor/{sensor}/entries/{entries}',
                '/pm/config/global/obj/ips/sensor/{sensor}/entries/{entries}'
            ]
        },
        'ips_sensor_entries_exemptip': {
            'params': [
                'sensor',
                'entries',
                'exempt-ip',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/ips/sensor/{sensor}/entries/{entries}/exempt-ip/{exempt-ip}',
                '/pm/config/global/obj/ips/sensor/{sensor}/entries/{entries}/exempt-ip/{exempt-ip}'
            ]
        },
        'ips_sensor_filter': {
            'params': [
                'sensor',
                'filter',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/ips/sensor/{sensor}/filter/{filter}',
                '/pm/config/global/obj/ips/sensor/{sensor}/filter/{filter}'
            ]
        },
        'ips_sensor_override': {
            'params': [
                'sensor',
                'override',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/ips/sensor/{sensor}/override/{override}',
                '/pm/config/global/obj/ips/sensor/{sensor}/override/{override}'
            ]
        },
        'ips_sensor_override_exemptip': {
            'params': [
                'sensor',
                'override',
                'exempt-ip',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/ips/sensor/{sensor}/override/{override}/exempt-ip/{exempt-ip}',
                '/pm/config/global/obj/ips/sensor/{sensor}/override/{override}/exempt-ip/{exempt-ip}'
            ]
        },
        'dvmdb_script': {
            'params': [
                'script',
                'adom'
            ],
            'urls': [
                '/dvmdb/adom/{adom}/script/{script}',
                '/dvmdb/global/script/{script}',
                '/dvmdb/script/{script}'
            ]
        },
        'dvmdb_script_scriptschedule': {
            'params': [
                'script',
                'script_schedule',
                'adom'
            ],
            'urls': [
                '/dvmdb/adom/{adom}/script/{script}/script_schedule/{script_schedule}',
                '/dvmdb/global/script/{script}/script_schedule/{script_schedule}',
                '/dvmdb/script/{script}/script_schedule/{script_schedule}'
            ]
        },
        'dvmdb_script_log_latest': {
            'params': [
                'adom'
            ],
            'urls': [
                '/dvmdb/adom/{adom}/script/log/latest',
                '/dvmdb/global/script/log/latest'
            ]
        },
        'dvmdb_script_log_latest_device': {
            'params': [
                'device_name',
                'adom'
            ],
            'urls': [
                '/dvmdb/adom/{adom}/script/log/latest/device/{device_name}',
                '/dvmdb/script/log/latest/device/{device_name}'
            ]
        },
        'dvmdb_script_log_list': {
            'params': [
                'adom'
            ],
            'urls': [
                '/dvmdb/adom/{adom}/script/log/list',
                '/dvmdb/global/script/log/list'
            ]
        },
        'dvmdb_script_log_list_device': {
            'params': [
                'device_name',
                'adom'
            ],
            'urls': [
                '/dvmdb/adom/{adom}/script/log/list/device/{device_name}',
                '/dvmdb/script/log/list/device/{device_name}'
            ]
        },
        'dvmdb_script_log_output_device_logid': {
            'params': [
                'device',
                'log_id',
                'adom'
            ],
            'urls': [
                '/dvmdb/adom/{adom}/script/log/output/device/{device}/logid/{log_id}',
                '/dvmdb/script/log/output/device/{device}/logid/{log_id}'
            ]
        },
        'dvmdb_script_log_output_logid': {
            'params': [
                'log_id',
                'adom'
            ],
            'urls': [
                '/dvmdb/adom/{adom}/script/log/output/logid/{log_id}',
                '/dvmdb/global/script/log/output/logid/{log_id}'
            ]
        },
        'dvmdb_script_log_summary': {
            'params': [
                'adom'
            ],
            'urls': [
                '/dvmdb/adom/{adom}/script/log/summary',
                '/dvmdb/global/script/log/summary'
            ]
        },
        'dvmdb_script_log_summary_device': {
            'params': [
                'device_name',
                'adom'
            ],
            'urls': [
                '/dvmdb/adom/{adom}/script/log/summary/device/{device_name}',
                '/dvmdb/script/log/summary/device/{device_name}'
            ]
        },
        'adom_options': {
            'params': [
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/adom/options',
                '/pm/config/global/obj/adom/options'
            ]
        },
        'dvmdb_workflow': {
            'params': [
                'workflow',
                'adom'
            ],
            'urls': [
                '/dvmdb/adom/{adom}/workflow/{workflow}',
                '/dvmdb/global/workflow/{workflow}',
                '/dvmdb/workflow/{workflow}'
            ]
        },
        'dvmdb_workflow_wflog': {
            'params': [
                'workflow',
                'wflog',
                'adom'
            ],
            'urls': [
                '/dvmdb/adom/{adom}/workflow/{workflow}/wflog/{wflog}',
                '/dvmdb/global/workflow/{workflow}/wflog/{wflog}',
                '/dvmdb/workflow/{workflow}/wflog/{wflog}'
            ]
        },
        'system_alertevent': {
            'params': [
                'alert-event'
            ],
            'urls': [
                '/cli/global/system/alert-event/{alert-event}'
            ]
        },
        'system_alertevent_alertdestination': {
            'params': [
                'alert-event',
                'alert-destination'
            ],
            'urls': [
                '/cli/global/system/alert-event/{alert-event}/alert-destination/{alert-destination}'
            ]
        },
        'fmupdate_diskquota': {
            'params': [
            ],
            'urls': [
                '/cli/global/fmupdate/disk-quota'
            ]
        },
        'vpnmgr_node': {
            'params': [
                'node',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/vpnmgr/node/{node}',
                '/pm/config/global/obj/vpnmgr/node/{node}'
            ]
        },
        'vpnmgr_node_iprange': {
            'params': [
                'node',
                'ip-range',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/vpnmgr/node/{node}/ip-range/{ip-range}',
                '/pm/config/global/obj/vpnmgr/node/{node}/ip-range/{ip-range}'
            ]
        },
        'vpnmgr_node_ipv4excluderange': {
            'params': [
                'node',
                'ipv4-exclude-range',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/vpnmgr/node/{node}/ipv4-exclude-range/{ipv4-exclude-range}',
                '/pm/config/global/obj/vpnmgr/node/{node}/ipv4-exclude-range/{ipv4-exclude-range}'
            ]
        },
        'vpnmgr_node_protectedsubnet': {
            'params': [
                'node',
                'protected_subnet',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/vpnmgr/node/{node}/protected_subnet/{protected_subnet}',
                '/pm/config/global/obj/vpnmgr/node/{node}/protected_subnet/{protected_subnet}'
            ]
        },
        'vpnmgr_node_summaryaddr': {
            'params': [
                'node',
                'summary_addr',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/vpnmgr/node/{node}/summary_addr/{summary_addr}',
                '/pm/config/global/obj/vpnmgr/node/{node}/summary_addr/{summary_addr}'
            ]
        },
        'vpnmgr_vpntable': {
            'params': [
                'vpntable',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/vpnmgr/vpntable/{vpntable}',
                '/pm/config/global/obj/vpnmgr/vpntable/{vpntable}'
            ]
        },
        'system_metadata_admins': {
            'params': [
                'admins'
            ],
            'urls': [
                '/cli/global/system/metadata/admins/{admins}'
            ]
        },
        'spamfilter_bwl': {
            'params': [
                'bwl',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/spamfilter/bwl/{bwl}',
                '/pm/config/global/obj/spamfilter/bwl/{bwl}'
            ]
        },
        'spamfilter_bwl_entries': {
            'params': [
                'bwl',
                'entries',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/spamfilter/bwl/{bwl}/entries/{entries}',
                '/pm/config/global/obj/spamfilter/bwl/{bwl}/entries/{entries}'
            ]
        },
        'spamfilter_bword': {
            'params': [
                'bword',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/spamfilter/bword/{bword}',
                '/pm/config/global/obj/spamfilter/bword/{bword}'
            ]
        },
        'spamfilter_bword_entries': {
            'params': [
                'bword',
                'entries',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/spamfilter/bword/{bword}/entries/{entries}',
                '/pm/config/global/obj/spamfilter/bword/{bword}/entries/{entries}'
            ]
        },
        'spamfilter_dnsbl': {
            'params': [
                'dnsbl',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/spamfilter/dnsbl/{dnsbl}',
                '/pm/config/global/obj/spamfilter/dnsbl/{dnsbl}'
            ]
        },
        'spamfilter_dnsbl_entries': {
            'params': [
                'dnsbl',
                'entries',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/spamfilter/dnsbl/{dnsbl}/entries/{entries}',
                '/pm/config/global/obj/spamfilter/dnsbl/{dnsbl}/entries/{entries}'
            ]
        },
        'spamfilter_iptrust': {
            'params': [
                'iptrust',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/spamfilter/iptrust/{iptrust}',
                '/pm/config/global/obj/spamfilter/iptrust/{iptrust}'
            ]
        },
        'spamfilter_iptrust_entries': {
            'params': [
                'iptrust',
                'entries',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/spamfilter/iptrust/{iptrust}/entries/{entries}',
                '/pm/config/global/obj/spamfilter/iptrust/{iptrust}/entries/{entries}'
            ]
        },
        'spamfilter_mheader': {
            'params': [
                'mheader',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/spamfilter/mheader/{mheader}',
                '/pm/config/global/obj/spamfilter/mheader/{mheader}'
            ]
        },
        'spamfilter_mheader_entries': {
            'params': [
                'mheader',
                'entries',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/spamfilter/mheader/{mheader}/entries/{entries}',
                '/pm/config/global/obj/spamfilter/mheader/{mheader}/entries/{entries}'
            ]
        },
        'spamfilter_profile': {
            'params': [
                'profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/spamfilter/profile/{profile}',
                '/pm/config/global/obj/spamfilter/profile/{profile}'
            ]
        },
        'spamfilter_profile_gmail': {
            'params': [
                'profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/spamfilter/profile/{profile}/gmail',
                '/pm/config/global/obj/spamfilter/profile/{profile}/gmail'
            ]
        },
        'spamfilter_profile_imap': {
            'params': [
                'profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/spamfilter/profile/{profile}/imap',
                '/pm/config/global/obj/spamfilter/profile/{profile}/imap'
            ]
        },
        'spamfilter_profile_mapi': {
            'params': [
                'profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/spamfilter/profile/{profile}/mapi',
                '/pm/config/global/obj/spamfilter/profile/{profile}/mapi'
            ]
        },
        'spamfilter_profile_msnhotmail': {
            'params': [
                'profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/spamfilter/profile/{profile}/msn-hotmail',
                '/pm/config/global/obj/spamfilter/profile/{profile}/msn-hotmail'
            ]
        },
        'spamfilter_profile_pop3': {
            'params': [
                'profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/spamfilter/profile/{profile}/pop3',
                '/pm/config/global/obj/spamfilter/profile/{profile}/pop3'
            ]
        },
        'spamfilter_profile_smtp': {
            'params': [
                'profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/spamfilter/profile/{profile}/smtp',
                '/pm/config/global/obj/spamfilter/profile/{profile}/smtp'
            ]
        },
        'spamfilter_profile_yahoomail': {
            'params': [
                'profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/spamfilter/profile/{profile}/yahoo-mail',
                '/pm/config/global/obj/spamfilter/profile/{profile}/yahoo-mail'
            ]
        },
        'fmupdate_multilayer': {
            'params': [
            ],
            'urls': [
                '/cli/global/fmupdate/multilayer'
            ]
        },
        'dvmdb_metafields_adom': {
            'params': [
            ],
            'urls': [
                '/dvmdb/_meta_fields/adom'
            ]
        },
        'dvmdb_metafields_device': {
            'params': [
            ],
            'urls': [
                '/dvmdb/_meta_fields/device'
            ]
        },
        'dvmdb_metafields_group': {
            'params': [
            ],
            'urls': [
                '/dvmdb/_meta_fields/group'
            ]
        },
        'system_guiact': {
            'params': [
            ],
            'urls': [
                '/cli/global/system/guiact'
            ]
        },
        'antivirus_mmschecksum': {
            'params': [
                'mms-checksum',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/antivirus/mms-checksum/{mms-checksum}',
                '/pm/config/global/obj/antivirus/mms-checksum/{mms-checksum}'
            ]
        },
        'antivirus_mmschecksum_entries': {
            'params': [
                'mms-checksum',
                'entries',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/antivirus/mms-checksum/{mms-checksum}/entries/{entries}',
                '/pm/config/global/obj/antivirus/mms-checksum/{mms-checksum}/entries/{entries}'
            ]
        },
        'antivirus_notification': {
            'params': [
                'notification',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/antivirus/notification/{notification}',
                '/pm/config/global/obj/antivirus/notification/{notification}'
            ]
        },
        'antivirus_notification_entries': {
            'params': [
                'notification',
                'entries',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/antivirus/notification/{notification}/entries/{entries}',
                '/pm/config/global/obj/antivirus/notification/{notification}/entries/{entries}'
            ]
        },
        'antivirus_profile': {
            'params': [
                'profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/antivirus/profile/{profile}',
                '/pm/config/global/obj/antivirus/profile/{profile}'
            ]
        },
        'antivirus_profile_contentdisarm': {
            'params': [
                'profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/antivirus/profile/{profile}/content-disarm',
                '/pm/config/global/obj/antivirus/profile/{profile}/content-disarm'
            ]
        },
        'antivirus_profile_ftp': {
            'params': [
                'profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/antivirus/profile/{profile}/ftp',
                '/pm/config/global/obj/antivirus/profile/{profile}/ftp'
            ]
        },
        'antivirus_profile_http': {
            'params': [
                'profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/antivirus/profile/{profile}/http',
                '/pm/config/global/obj/antivirus/profile/{profile}/http'
            ]
        },
        'antivirus_profile_imap': {
            'params': [
                'profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/antivirus/profile/{profile}/imap',
                '/pm/config/global/obj/antivirus/profile/{profile}/imap'
            ]
        },
        'antivirus_profile_mapi': {
            'params': [
                'profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/antivirus/profile/{profile}/mapi',
                '/pm/config/global/obj/antivirus/profile/{profile}/mapi'
            ]
        },
        'antivirus_profile_nacquar': {
            'params': [
                'profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/antivirus/profile/{profile}/nac-quar',
                '/pm/config/global/obj/antivirus/profile/{profile}/nac-quar'
            ]
        },
        'antivirus_profile_nntp': {
            'params': [
                'profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/antivirus/profile/{profile}/nntp',
                '/pm/config/global/obj/antivirus/profile/{profile}/nntp'
            ]
        },
        'antivirus_profile_pop3': {
            'params': [
                'profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/antivirus/profile/{profile}/pop3',
                '/pm/config/global/obj/antivirus/profile/{profile}/pop3'
            ]
        },
        'antivirus_profile_smb': {
            'params': [
                'profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/antivirus/profile/{profile}/smb',
                '/pm/config/global/obj/antivirus/profile/{profile}/smb'
            ]
        },
        'antivirus_profile_smtp': {
            'params': [
                'profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/antivirus/profile/{profile}/smtp',
                '/pm/config/global/obj/antivirus/profile/{profile}/smtp'
            ]
        },
        'switchcontroller_lldpprofile': {
            'params': [
                'lldp-profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/switch-controller/lldp-profile/{lldp-profile}',
                '/pm/config/global/obj/switch-controller/lldp-profile/{lldp-profile}'
            ]
        },
        'switchcontroller_lldpprofile_customtlvs': {
            'params': [
                'lldp-profile',
                'custom-tlvs',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/switch-controller/lldp-profile/{lldp-profile}/custom-tlvs/{custom-tlvs}',
                '/pm/config/global/obj/switch-controller/lldp-profile/{lldp-profile}/custom-tlvs/{custom-tlvs}'
            ]
        },
        'switchcontroller_lldpprofile_mednetworkpolicy': {
            'params': [
                'lldp-profile',
                'med-network-policy',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/switch-controller/lldp-profile/{lldp-profile}/med-network-policy/{med-network-policy}',
                '/pm/config/global/obj/switch-controller/lldp-profile/{lldp-profile}/med-network-policy/{med-network-policy}'
            ]
        },
        'switchcontroller_managedswitch': {
            'params': [
                'managed-switch',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/switch-controller/managed-switch/{managed-switch}',
                '/pm/config/global/obj/switch-controller/managed-switch/{managed-switch}'
            ]
        },
        'switchcontroller_managedswitch_ports': {
            'params': [
                'managed-switch',
                'ports',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/switch-controller/managed-switch/{managed-switch}/ports/{ports}',
                '/pm/config/global/obj/switch-controller/managed-switch/{managed-switch}/ports/{ports}'
            ]
        },
        'switchcontroller_qos_dot1pmap': {
            'params': [
                'dot1p-map',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/switch-controller/qos/dot1p-map/{dot1p-map}',
                '/pm/config/global/obj/switch-controller/qos/dot1p-map/{dot1p-map}'
            ]
        },
        'switchcontroller_qos_ipdscpmap': {
            'params': [
                'ip-dscp-map',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/switch-controller/qos/ip-dscp-map/{ip-dscp-map}',
                '/pm/config/global/obj/switch-controller/qos/ip-dscp-map/{ip-dscp-map}'
            ]
        },
        'switchcontroller_qos_ipdscpmap_map': {
            'params': [
                'ip-dscp-map',
                'map',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/switch-controller/qos/ip-dscp-map/{ip-dscp-map}/map/{map}',
                '/pm/config/global/obj/switch-controller/qos/ip-dscp-map/{ip-dscp-map}/map/{map}'
            ]
        },
        'switchcontroller_qos_qospolicy': {
            'params': [
                'qos-policy',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/switch-controller/qos/qos-policy/{qos-policy}',
                '/pm/config/global/obj/switch-controller/qos/qos-policy/{qos-policy}'
            ]
        },
        'switchcontroller_qos_queuepolicy': {
            'params': [
                'queue-policy',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/switch-controller/qos/queue-policy/{queue-policy}',
                '/pm/config/global/obj/switch-controller/qos/queue-policy/{queue-policy}'
            ]
        },
        'switchcontroller_qos_queuepolicy_cosqueue': {
            'params': [
                'queue-policy',
                'cos-queue',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/switch-controller/qos/queue-policy/{queue-policy}/cos-queue/{cos-queue}',
                '/pm/config/global/obj/switch-controller/qos/queue-policy/{queue-policy}/cos-queue/{cos-queue}'
            ]
        },
        'switchcontroller_securitypolicy_8021x': {
            'params': [
                '802-1X',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/switch-controller/security-policy/802-1X/{802-1X}',
                '/pm/config/global/obj/switch-controller/security-policy/802-1X/{802-1X}'
            ]
        },
        'switchcontroller_securitypolicy_captiveportal': {
            'params': [
                'captive-portal',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/switch-controller/security-policy/captive-portal/{captive-portal}',
                '/pm/config/global/obj/switch-controller/security-policy/captive-portal/{captive-portal}'
            ]
        },
        'switchcontroller_managedswitch_8021xsettings': {
            'params': [
                'device',
                'vdom',
                'managed-switch'
            ],
            'urls': [
                '/pm/config/device/{device}/vdom/{vdom}/switch-controller/managed-switch/{managed-switch}/802-1X-settings'
            ]
        },
        'switchcontroller_managedswitch_customcommand': {
            'params': [
                'device',
                'vdom',
                'managed-switch',
                'custom-command'
            ],
            'urls': [
                '/pm/config/device/{device}/vdom/{vdom}/switch-controller/managed-switch/{managed-switch}/custom-command/{custom-command}'
            ]
        },
        'switchcontroller_managedswitch_igmpsnooping': {
            'params': [
                'device',
                'vdom',
                'managed-switch'
            ],
            'urls': [
                '/pm/config/device/{device}/vdom/{vdom}/switch-controller/managed-switch/{managed-switch}/igmp-snooping'
            ]
        },
        'switchcontroller_managedswitch_mirror': {
            'params': [
                'device',
                'vdom',
                'managed-switch',
                'mirror'
            ],
            'urls': [
                '/pm/config/device/{device}/vdom/{vdom}/switch-controller/managed-switch/{managed-switch}/mirror/{mirror}'
            ]
        },
        'switchcontroller_managedswitch_stormcontrol': {
            'params': [
                'device',
                'vdom',
                'managed-switch'
            ],
            'urls': [
                '/pm/config/device/{device}/vdom/{vdom}/switch-controller/managed-switch/{managed-switch}/storm-control'
            ]
        },
        'switchcontroller_managedswitch_stpsettings': {
            'params': [
                'device',
                'vdom',
                'managed-switch'
            ],
            'urls': [
                '/pm/config/device/{device}/vdom/{vdom}/switch-controller/managed-switch/{managed-switch}/stp-settings'
            ]
        },
        'switchcontroller_managedswitch_switchlog': {
            'params': [
                'device',
                'vdom',
                'managed-switch'
            ],
            'urls': [
                '/pm/config/device/{device}/vdom/{vdom}/switch-controller/managed-switch/{managed-switch}/switch-log'
            ]
        },
        'switchcontroller_managedswitch_switchstpsettings': {
            'params': [
                'device',
                'vdom',
                'managed-switch'
            ],
            'urls': [
                '/pm/config/device/{device}/vdom/{vdom}/switch-controller/managed-switch/{managed-switch}/switch-stp-settings'
            ]
        },
        'system_status': {
            'params': [
            ],
            'urls': [
                '/cli/global/system/status'
            ]
        },
        'devprof_log_fortianalyzer_setting': {
            'params': [
                'devprof',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/devprof/{devprof}/log/fortianalyzer/setting'
            ]
        },
        'devprof_log_syslogd_filter': {
            'params': [
                'devprof',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/devprof/{devprof}/log/syslogd/filter'
            ]
        },
        'devprof_log_syslogd_setting': {
            'params': [
                'devprof',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/devprof/{devprof}/log/syslogd/setting'
            ]
        },
        'system_certificate_ca': {
            'params': [
                'ca'
            ],
            'urls': [
                '/cli/global/system/certificate/ca/{ca}'
            ]
        },
        'system_certificate_crl': {
            'params': [
                'crl'
            ],
            'urls': [
                '/cli/global/system/certificate/crl/{crl}'
            ]
        },
        'system_certificate_local': {
            'params': [
                'local'
            ],
            'urls': [
                '/cli/global/system/certificate/local/{local}'
            ]
        },
        'system_certificate_oftp': {
            'params': [
            ],
            'urls': [
                '/cli/global/system/certificate/oftp'
            ]
        },
        'system_certificate_remote': {
            'params': [
                'remote'
            ],
            'urls': [
                '/cli/global/system/certificate/remote/{remote}'
            ]
        },
        'system_certificate_ssh': {
            'params': [
                'ssh'
            ],
            'urls': [
                '/cli/global/system/certificate/ssh/{ssh}'
            ]
        },
        'firewall_address': {
            'params': [
                'address',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/address/{address}',
                '/pm/config/global/obj/firewall/address/{address}'
            ]
        },
        'firewall_address_dynamicmapping': {
            'params': [
                'address',
                'dynamic_mapping',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/address/{address}/dynamic_mapping/{dynamic_mapping}',
                '/pm/config/global/obj/firewall/address/{address}/dynamic_mapping/{dynamic_mapping}'
            ]
        },
        'firewall_address_list': {
            'params': [
                'address',
                'list',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/address/{address}/list/{list}',
                '/pm/config/global/obj/firewall/address/{address}/list/{list}'
            ]
        },
        'firewall_address_tagging': {
            'params': [
                'address',
                'tagging',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/address/{address}/tagging/{tagging}',
                '/pm/config/global/obj/firewall/address/{address}/tagging/{tagging}'
            ]
        },
        'firewall_address6': {
            'params': [
                'address6',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/address6/{address6}',
                '/pm/config/global/obj/firewall/address6/{address6}'
            ]
        },
        'firewall_address6template': {
            'params': [
                'address6-template',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/address6-template/{address6-template}',
                '/pm/config/global/obj/firewall/address6-template/{address6-template}'
            ]
        },
        'firewall_address6template_subnetsegment': {
            'params': [
                'address6-template',
                'subnet-segment',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/address6-template/{address6-template}/subnet-segment/{subnet-segment}',
                '/pm/config/global/obj/firewall/address6-template/{address6-template}/subnet-segment/{subnet-segment}'
            ]
        },
        'firewall_address6template_subnetsegment_values': {
            'params': [
                'address6-template',
                'subnet-segment',
                'values',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/address6-template/{address6-template}/subnet-segment/{subnet-segment}/values/{values}',
                '/pm/config/global/obj/firewall/address6-template/{address6-template}/subnet-segment/{subnet-segment}/values/{values}'
            ]
        },
        'firewall_address6_dynamicmapping': {
            'params': [
                'address6',
                'dynamic_mapping',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/address6/{address6}/dynamic_mapping/{dynamic_mapping}',
                '/pm/config/global/obj/firewall/address6/{address6}/dynamic_mapping/{dynamic_mapping}'
            ]
        },
        'firewall_address6_list': {
            'params': [
                'address6',
                'list',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/address6/{address6}/list/{list}',
                '/pm/config/global/obj/firewall/address6/{address6}/list/{list}'
            ]
        },
        'firewall_address6_subnetsegment': {
            'params': [
                'address6',
                'subnet-segment',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/address6/{address6}/subnet-segment/{subnet-segment}',
                '/pm/config/global/obj/firewall/address6/{address6}/subnet-segment/{subnet-segment}'
            ]
        },
        'firewall_address6_tagging': {
            'params': [
                'address6',
                'tagging',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/address6/{address6}/tagging/{tagging}',
                '/pm/config/global/obj/firewall/address6/{address6}/tagging/{tagging}'
            ]
        },
        'firewall_addrgrp': {
            'params': [
                'addrgrp',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/addrgrp/{addrgrp}',
                '/pm/config/global/obj/firewall/addrgrp/{addrgrp}'
            ]
        },
        'firewall_addrgrp_dynamicmapping': {
            'params': [
                'addrgrp',
                'dynamic_mapping',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/addrgrp/{addrgrp}/dynamic_mapping/{dynamic_mapping}',
                '/pm/config/global/obj/firewall/addrgrp/{addrgrp}/dynamic_mapping/{dynamic_mapping}'
            ]
        },
        'firewall_addrgrp_tagging': {
            'params': [
                'addrgrp',
                'tagging',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/addrgrp/{addrgrp}/tagging/{tagging}',
                '/pm/config/global/obj/firewall/addrgrp/{addrgrp}/tagging/{tagging}'
            ]
        },
        'firewall_addrgrp6': {
            'params': [
                'addrgrp6',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/addrgrp6/{addrgrp6}',
                '/pm/config/global/obj/firewall/addrgrp6/{addrgrp6}'
            ]
        },
        'firewall_addrgrp6_dynamicmapping': {
            'params': [
                'addrgrp6',
                'dynamic_mapping',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/addrgrp6/{addrgrp6}/dynamic_mapping/{dynamic_mapping}',
                '/pm/config/global/obj/firewall/addrgrp6/{addrgrp6}/dynamic_mapping/{dynamic_mapping}'
            ]
        },
        'firewall_addrgrp6_tagging': {
            'params': [
                'addrgrp6',
                'tagging',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/addrgrp6/{addrgrp6}/tagging/{tagging}',
                '/pm/config/global/obj/firewall/addrgrp6/{addrgrp6}/tagging/{tagging}'
            ]
        },
        'firewall_carrierendpointbwl': {
            'params': [
                'carrier-endpoint-bwl',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/carrier-endpoint-bwl/{carrier-endpoint-bwl}',
                '/pm/config/global/obj/firewall/carrier-endpoint-bwl/{carrier-endpoint-bwl}'
            ]
        },
        'firewall_carrierendpointbwl_entries': {
            'params': [
                'carrier-endpoint-bwl',
                'entries',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/carrier-endpoint-bwl/{carrier-endpoint-bwl}/entries/{entries}',
                '/pm/config/global/obj/firewall/carrier-endpoint-bwl/{carrier-endpoint-bwl}/entries/{entries}'
            ]
        },
        'firewall_gtp': {
            'params': [
                'gtp',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/gtp/{gtp}',
                '/pm/config/global/obj/firewall/gtp/{gtp}'
            ]
        },
        'firewall_gtp_apn': {
            'params': [
                'gtp',
                'apn',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/gtp/{gtp}/apn/{apn}',
                '/pm/config/global/obj/firewall/gtp/{gtp}/apn/{apn}'
            ]
        },
        'firewall_gtp_ieremovepolicy': {
            'params': [
                'gtp',
                'ie-remove-policy',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/gtp/{gtp}/ie-remove-policy/{ie-remove-policy}',
                '/pm/config/global/obj/firewall/gtp/{gtp}/ie-remove-policy/{ie-remove-policy}'
            ]
        },
        'firewall_gtp_ievalidation': {
            'params': [
                'gtp',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/gtp/{gtp}/ie-validation',
                '/pm/config/global/obj/firewall/gtp/{gtp}/ie-validation'
            ]
        },
        'firewall_gtp_imsi': {
            'params': [
                'gtp',
                'imsi',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/gtp/{gtp}/imsi/{imsi}',
                '/pm/config/global/obj/firewall/gtp/{gtp}/imsi/{imsi}'
            ]
        },
        'firewall_gtp_ippolicy': {
            'params': [
                'gtp',
                'ip-policy',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/gtp/{gtp}/ip-policy/{ip-policy}',
                '/pm/config/global/obj/firewall/gtp/{gtp}/ip-policy/{ip-policy}'
            ]
        },
        'firewall_gtp_messageratelimit': {
            'params': [
                'gtp',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/gtp/{gtp}/message-rate-limit',
                '/pm/config/global/obj/firewall/gtp/{gtp}/message-rate-limit'
            ]
        },
        'firewall_gtp_messageratelimitv0': {
            'params': [
                'gtp',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/gtp/{gtp}/message-rate-limit-v0',
                '/pm/config/global/obj/firewall/gtp/{gtp}/message-rate-limit-v0'
            ]
        },
        'firewall_gtp_messageratelimitv1': {
            'params': [
                'gtp',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/gtp/{gtp}/message-rate-limit-v1',
                '/pm/config/global/obj/firewall/gtp/{gtp}/message-rate-limit-v1'
            ]
        },
        'firewall_gtp_messageratelimitv2': {
            'params': [
                'gtp',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/gtp/{gtp}/message-rate-limit-v2',
                '/pm/config/global/obj/firewall/gtp/{gtp}/message-rate-limit-v2'
            ]
        },
        'firewall_gtp_noippolicy': {
            'params': [
                'gtp',
                'noip-policy',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/gtp/{gtp}/noip-policy/{noip-policy}',
                '/pm/config/global/obj/firewall/gtp/{gtp}/noip-policy/{noip-policy}'
            ]
        },
        'firewall_gtp_perapnshaper': {
            'params': [
                'gtp',
                'per-apn-shaper',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/gtp/{gtp}/per-apn-shaper/{per-apn-shaper}',
                '/pm/config/global/obj/firewall/gtp/{gtp}/per-apn-shaper/{per-apn-shaper}'
            ]
        },
        'firewall_gtp_policy': {
            'params': [
                'gtp',
                'policy',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/gtp/{gtp}/policy/{policy}',
                '/pm/config/global/obj/firewall/gtp/{gtp}/policy/{policy}'
            ]
        },
        'firewall_identitybasedroute': {
            'params': [
                'identity-based-route',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/identity-based-route/{identity-based-route}',
                '/pm/config/global/obj/firewall/identity-based-route/{identity-based-route}'
            ]
        },
        'firewall_identitybasedroute_rule': {
            'params': [
                'identity-based-route',
                'rule',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/identity-based-route/{identity-based-route}/rule/{rule}',
                '/pm/config/global/obj/firewall/identity-based-route/{identity-based-route}/rule/{rule}'
            ]
        },
        'firewall_internetservice': {
            'params': [
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/internet-service',
                '/pm/config/global/obj/firewall/internet-service'
            ]
        },
        'firewall_internetservicecustom': {
            'params': [
                'internet-service-custom',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/internet-service-custom/{internet-service-custom}',
                '/pm/config/global/obj/firewall/internet-service-custom/{internet-service-custom}'
            ]
        },
        'firewall_internetservicecustomgroup': {
            'params': [
                'internet-service-custom-group',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/internet-service-custom-group/{internet-service-custom-group}',
                '/pm/config/global/obj/firewall/internet-service-custom-group/{internet-service-custom-group}'
            ]
        },
        'firewall_internetservicecustom_disableentry': {
            'params': [
                'internet-service-custom',
                'disable-entry',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/internet-service-custom/{internet-service-custom}/disable-entry/{disable-entry}',
                '/pm/config/global/obj/firewall/internet-service-custom/{internet-service-custom}/disable-entry/{disable-entry}'
            ]
        },
        'firewall_internetservicecustom_disableentry_iprange': {
            'params': [
                'internet-service-custom',
                'disable-entry',
                'ip-range',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/internet-service-custom/{internet-service-custom}/disable-entry/{disable-entry}/ip-range/{ip-range}',
                '/pm/config/global/obj/firewall/internet-service-custom/{internet-service-custom}/disable-entry/{disable-entry}/ip-range/{ip-range}'
            ]
        },
        'firewall_internetservicecustom_entry': {
            'params': [
                'internet-service-custom',
                'entry',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/internet-service-custom/{internet-service-custom}/entry/{entry}',
                '/pm/config/global/obj/firewall/internet-service-custom/{internet-service-custom}/entry/{entry}'
            ]
        },
        'firewall_internetservicecustom_entry_portrange': {
            'params': [
                'internet-service-custom',
                'entry',
                'port-range',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/internet-service-custom/{internet-service-custom}/entry/{entry}/port-range/{port-range}',
                '/pm/config/global/obj/firewall/internet-service-custom/{internet-service-custom}/entry/{entry}/port-range/{port-range}'
            ]
        },
        'firewall_internetservicegroup': {
            'params': [
                'internet-service-group',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/internet-service-group/{internet-service-group}',
                '/pm/config/global/obj/firewall/internet-service-group/{internet-service-group}'
            ]
        },
        'firewall_internetservice_entry': {
            'params': [
                'entry',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/internet-service/entry/{entry}',
                '/pm/config/global/obj/firewall/internet-service/entry/{entry}'
            ]
        },
        'firewall_ippool': {
            'params': [
                'ippool',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/ippool/{ippool}',
                '/pm/config/global/obj/firewall/ippool/{ippool}'
            ]
        },
        'firewall_ippool_dynamicmapping': {
            'params': [
                'ippool',
                'dynamic_mapping',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/ippool/{ippool}/dynamic_mapping/{dynamic_mapping}',
                '/pm/config/global/obj/firewall/ippool/{ippool}/dynamic_mapping/{dynamic_mapping}'
            ]
        },
        'firewall_ippool6': {
            'params': [
                'ippool6',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/ippool6/{ippool6}',
                '/pm/config/global/obj/firewall/ippool6/{ippool6}'
            ]
        },
        'firewall_ippool6_dynamicmapping': {
            'params': [
                'ippool6',
                'dynamic_mapping',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/ippool6/{ippool6}/dynamic_mapping/{dynamic_mapping}',
                '/pm/config/global/obj/firewall/ippool6/{ippool6}/dynamic_mapping/{dynamic_mapping}'
            ]
        },
        'firewall_ldbmonitor': {
            'params': [
                'ldb-monitor',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/ldb-monitor/{ldb-monitor}',
                '/pm/config/global/obj/firewall/ldb-monitor/{ldb-monitor}'
            ]
        },
        'firewall_mmsprofile': {
            'params': [
                'mms-profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/mms-profile/{mms-profile}',
                '/pm/config/global/obj/firewall/mms-profile/{mms-profile}'
            ]
        },
        'firewall_mmsprofile_dupe': {
            'params': [
                'mms-profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/mms-profile/{mms-profile}/dupe',
                '/pm/config/global/obj/firewall/mms-profile/{mms-profile}/dupe'
            ]
        },
        'firewall_mmsprofile_flood': {
            'params': [
                'mms-profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/mms-profile/{mms-profile}/flood',
                '/pm/config/global/obj/firewall/mms-profile/{mms-profile}/flood'
            ]
        },
        'firewall_mmsprofile_notifmsisdn': {
            'params': [
                'mms-profile',
                'notif-msisdn',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/mms-profile/{mms-profile}/notif-msisdn/{notif-msisdn}',
                '/pm/config/global/obj/firewall/mms-profile/{mms-profile}/notif-msisdn/{notif-msisdn}'
            ]
        },
        'firewall_mmsprofile_notification': {
            'params': [
                'mms-profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/mms-profile/{mms-profile}/notification',
                '/pm/config/global/obj/firewall/mms-profile/{mms-profile}/notification'
            ]
        },
        'firewall_multicastaddress': {
            'params': [
                'multicast-address',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/multicast-address/{multicast-address}',
                '/pm/config/global/obj/firewall/multicast-address/{multicast-address}'
            ]
        },
        'firewall_multicastaddress_tagging': {
            'params': [
                'multicast-address',
                'tagging',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/multicast-address/{multicast-address}/tagging/{tagging}',
                '/pm/config/global/obj/firewall/multicast-address/{multicast-address}/tagging/{tagging}'
            ]
        },
        'firewall_multicastaddress6': {
            'params': [
                'multicast-address6',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/multicast-address6/{multicast-address6}',
                '/pm/config/global/obj/firewall/multicast-address6/{multicast-address6}'
            ]
        },
        'firewall_multicastaddress6_tagging': {
            'params': [
                'multicast-address6',
                'tagging',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/multicast-address6/{multicast-address6}/tagging/{tagging}',
                '/pm/config/global/obj/firewall/multicast-address6/{multicast-address6}/tagging/{tagging}'
            ]
        },
        'firewall_profilegroup': {
            'params': [
                'profile-group',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/profile-group/{profile-group}',
                '/pm/config/global/obj/firewall/profile-group/{profile-group}'
            ]
        },
        'firewall_profileprotocoloptions': {
            'params': [
                'profile-protocol-options',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/profile-protocol-options/{profile-protocol-options}',
                '/pm/config/global/obj/firewall/profile-protocol-options/{profile-protocol-options}'
            ]
        },
        'firewall_profileprotocoloptions_dns': {
            'params': [
                'profile-protocol-options',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/profile-protocol-options/{profile-protocol-options}/dns',
                '/pm/config/global/obj/firewall/profile-protocol-options/{profile-protocol-options}/dns'
            ]
        },
        'firewall_profileprotocoloptions_ftp': {
            'params': [
                'profile-protocol-options',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/profile-protocol-options/{profile-protocol-options}/ftp',
                '/pm/config/global/obj/firewall/profile-protocol-options/{profile-protocol-options}/ftp'
            ]
        },
        'firewall_profileprotocoloptions_http': {
            'params': [
                'profile-protocol-options',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/profile-protocol-options/{profile-protocol-options}/http',
                '/pm/config/global/obj/firewall/profile-protocol-options/{profile-protocol-options}/http'
            ]
        },
        'firewall_profileprotocoloptions_imap': {
            'params': [
                'profile-protocol-options',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/profile-protocol-options/{profile-protocol-options}/imap',
                '/pm/config/global/obj/firewall/profile-protocol-options/{profile-protocol-options}/imap'
            ]
        },
        'firewall_profileprotocoloptions_mailsignature': {
            'params': [
                'profile-protocol-options',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/profile-protocol-options/{profile-protocol-options}/mail-signature',
                '/pm/config/global/obj/firewall/profile-protocol-options/{profile-protocol-options}/mail-signature'
            ]
        },
        'firewall_profileprotocoloptions_mapi': {
            'params': [
                'profile-protocol-options',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/profile-protocol-options/{profile-protocol-options}/mapi',
                '/pm/config/global/obj/firewall/profile-protocol-options/{profile-protocol-options}/mapi'
            ]
        },
        'firewall_profileprotocoloptions_nntp': {
            'params': [
                'profile-protocol-options',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/profile-protocol-options/{profile-protocol-options}/nntp',
                '/pm/config/global/obj/firewall/profile-protocol-options/{profile-protocol-options}/nntp'
            ]
        },
        'firewall_profileprotocoloptions_pop3': {
            'params': [
                'profile-protocol-options',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/profile-protocol-options/{profile-protocol-options}/pop3',
                '/pm/config/global/obj/firewall/profile-protocol-options/{profile-protocol-options}/pop3'
            ]
        },
        'firewall_profileprotocoloptions_smtp': {
            'params': [
                'profile-protocol-options',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/profile-protocol-options/{profile-protocol-options}/smtp',
                '/pm/config/global/obj/firewall/profile-protocol-options/{profile-protocol-options}/smtp'
            ]
        },
        'firewall_proxyaddress': {
            'params': [
                'proxy-address',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/proxy-address/{proxy-address}',
                '/pm/config/global/obj/firewall/proxy-address/{proxy-address}'
            ]
        },
        'firewall_proxyaddress_headergroup': {
            'params': [
                'proxy-address',
                'header-group',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/proxy-address/{proxy-address}/header-group/{header-group}',
                '/pm/config/global/obj/firewall/proxy-address/{proxy-address}/header-group/{header-group}'
            ]
        },
        'firewall_proxyaddress_tagging': {
            'params': [
                'proxy-address',
                'tagging',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/proxy-address/{proxy-address}/tagging/{tagging}',
                '/pm/config/global/obj/firewall/proxy-address/{proxy-address}/tagging/{tagging}'
            ]
        },
        'firewall_proxyaddrgrp': {
            'params': [
                'proxy-addrgrp',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/proxy-addrgrp/{proxy-addrgrp}',
                '/pm/config/global/obj/firewall/proxy-addrgrp/{proxy-addrgrp}'
            ]
        },
        'firewall_proxyaddrgrp_tagging': {
            'params': [
                'proxy-addrgrp',
                'tagging',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/proxy-addrgrp/{proxy-addrgrp}/tagging/{tagging}',
                '/pm/config/global/obj/firewall/proxy-addrgrp/{proxy-addrgrp}/tagging/{tagging}'
            ]
        },
        'firewall_schedule_group': {
            'params': [
                'group',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/schedule/group/{group}',
                '/pm/config/global/obj/firewall/schedule/group/{group}'
            ]
        },
        'firewall_schedule_onetime': {
            'params': [
                'onetime',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/schedule/onetime/{onetime}',
                '/pm/config/global/obj/firewall/schedule/onetime/{onetime}'
            ]
        },
        'firewall_schedule_recurring': {
            'params': [
                'recurring',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/schedule/recurring/{recurring}',
                '/pm/config/global/obj/firewall/schedule/recurring/{recurring}'
            ]
        },
        'firewall_service_category': {
            'params': [
                'category',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/service/category/{category}',
                '/pm/config/global/obj/firewall/service/category/{category}'
            ]
        },
        'firewall_service_custom': {
            'params': [
                'custom',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/service/custom/{custom}',
                '/pm/config/global/obj/firewall/service/custom/{custom}'
            ]
        },
        'firewall_service_group': {
            'params': [
                'group',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/service/group/{group}',
                '/pm/config/global/obj/firewall/service/group/{group}'
            ]
        },
        'firewall_shaper_peripshaper': {
            'params': [
                'per-ip-shaper',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/shaper/per-ip-shaper/{per-ip-shaper}',
                '/pm/config/global/obj/firewall/shaper/per-ip-shaper/{per-ip-shaper}'
            ]
        },
        'firewall_shaper_trafficshaper': {
            'params': [
                'traffic-shaper',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/shaper/traffic-shaper/{traffic-shaper}',
                '/pm/config/global/obj/firewall/shaper/traffic-shaper/{traffic-shaper}'
            ]
        },
        'firewall_shapingprofile': {
            'params': [
                'shaping-profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/shaping-profile/{shaping-profile}',
                '/pm/config/global/obj/firewall/shaping-profile/{shaping-profile}'
            ]
        },
        'firewall_shapingprofile_shapingentries': {
            'params': [
                'shaping-profile',
                'shaping-entries',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/shaping-profile/{shaping-profile}/shaping-entries/{shaping-entries}',
                '/pm/config/global/obj/firewall/shaping-profile/{shaping-profile}/shaping-entries/{shaping-entries}'
            ]
        },
        'firewall_sslsshprofile': {
            'params': [
                'ssl-ssh-profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/ssl-ssh-profile/{ssl-ssh-profile}',
                '/pm/config/global/obj/firewall/ssl-ssh-profile/{ssl-ssh-profile}'
            ]
        },
        'firewall_sslsshprofile_ftps': {
            'params': [
                'ssl-ssh-profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/ssl-ssh-profile/{ssl-ssh-profile}/ftps',
                '/pm/config/global/obj/firewall/ssl-ssh-profile/{ssl-ssh-profile}/ftps'
            ]
        },
        'firewall_sslsshprofile_https': {
            'params': [
                'ssl-ssh-profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/ssl-ssh-profile/{ssl-ssh-profile}/https',
                '/pm/config/global/obj/firewall/ssl-ssh-profile/{ssl-ssh-profile}/https'
            ]
        },
        'firewall_sslsshprofile_imaps': {
            'params': [
                'ssl-ssh-profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/ssl-ssh-profile/{ssl-ssh-profile}/imaps',
                '/pm/config/global/obj/firewall/ssl-ssh-profile/{ssl-ssh-profile}/imaps'
            ]
        },
        'firewall_sslsshprofile_pop3s': {
            'params': [
                'ssl-ssh-profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/ssl-ssh-profile/{ssl-ssh-profile}/pop3s',
                '/pm/config/global/obj/firewall/ssl-ssh-profile/{ssl-ssh-profile}/pop3s'
            ]
        },
        'firewall_sslsshprofile_smtps': {
            'params': [
                'ssl-ssh-profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/ssl-ssh-profile/{ssl-ssh-profile}/smtps',
                '/pm/config/global/obj/firewall/ssl-ssh-profile/{ssl-ssh-profile}/smtps'
            ]
        },
        'firewall_sslsshprofile_ssh': {
            'params': [
                'ssl-ssh-profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/ssl-ssh-profile/{ssl-ssh-profile}/ssh',
                '/pm/config/global/obj/firewall/ssl-ssh-profile/{ssl-ssh-profile}/ssh'
            ]
        },
        'firewall_sslsshprofile_ssl': {
            'params': [
                'ssl-ssh-profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/ssl-ssh-profile/{ssl-ssh-profile}/ssl',
                '/pm/config/global/obj/firewall/ssl-ssh-profile/{ssl-ssh-profile}/ssl'
            ]
        },
        'firewall_sslsshprofile_sslexempt': {
            'params': [
                'ssl-ssh-profile',
                'ssl-exempt',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/ssl-ssh-profile/{ssl-ssh-profile}/ssl-exempt/{ssl-exempt}',
                '/pm/config/global/obj/firewall/ssl-ssh-profile/{ssl-ssh-profile}/ssl-exempt/{ssl-exempt}'
            ]
        },
        'firewall_sslsshprofile_sslserver': {
            'params': [
                'ssl-ssh-profile',
                'ssl-server',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/ssl-ssh-profile/{ssl-ssh-profile}/ssl-server/{ssl-server}',
                '/pm/config/global/obj/firewall/ssl-ssh-profile/{ssl-ssh-profile}/ssl-server/{ssl-server}'
            ]
        },
        'firewall_vip': {
            'params': [
                'vip',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/vip/{vip}',
                '/pm/config/global/obj/firewall/vip/{vip}'
            ]
        },
        'firewall_vip_dynamicmapping': {
            'params': [
                'vip',
                'dynamic_mapping',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/vip/{vip}/dynamic_mapping/{dynamic_mapping}',
                '/pm/config/global/obj/firewall/vip/{vip}/dynamic_mapping/{dynamic_mapping}'
            ]
        },
        'firewall_vip_dynamicmapping_realservers': {
            'params': [
                'vip',
                'dynamic_mapping',
                'realservers',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/vip/{vip}/dynamic_mapping/{dynamic_mapping}/realservers/{realservers}',
                '/pm/config/global/obj/firewall/vip/{vip}/dynamic_mapping/{dynamic_mapping}/realservers/{realservers}'
            ]
        },
        'firewall_vip_dynamicmapping_sslciphersuites': {
            'params': [
                'vip',
                'dynamic_mapping',
                'ssl-cipher-suites',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/vip/{vip}/dynamic_mapping/{dynamic_mapping}/ssl-cipher-suites/{ssl-cipher-suites}',
                '/pm/config/global/obj/firewall/vip/{vip}/dynamic_mapping/{dynamic_mapping}/ssl-cipher-suites/{ssl-cipher-suites}'
            ]
        },
        'firewall_vip_realservers': {
            'params': [
                'vip',
                'realservers',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/vip/{vip}/realservers/{realservers}',
                '/pm/config/global/obj/firewall/vip/{vip}/realservers/{realservers}'
            ]
        },
        'firewall_vip_sslciphersuites': {
            'params': [
                'vip',
                'ssl-cipher-suites',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/vip/{vip}/ssl-cipher-suites/{ssl-cipher-suites}',
                '/pm/config/global/obj/firewall/vip/{vip}/ssl-cipher-suites/{ssl-cipher-suites}'
            ]
        },
        'firewall_vip_sslserverciphersuites': {
            'params': [
                'vip',
                'ssl-server-cipher-suites',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/vip/{vip}/ssl-server-cipher-suites/{ssl-server-cipher-suites}',
                '/pm/config/global/obj/firewall/vip/{vip}/ssl-server-cipher-suites/{ssl-server-cipher-suites}'
            ]
        },
        'firewall_vip46': {
            'params': [
                'vip46',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/vip46/{vip46}',
                '/pm/config/global/obj/firewall/vip46/{vip46}'
            ]
        },
        'firewall_vip46_dynamicmapping': {
            'params': [
                'vip46',
                'dynamic_mapping',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/vip46/{vip46}/dynamic_mapping/{dynamic_mapping}',
                '/pm/config/global/obj/firewall/vip46/{vip46}/dynamic_mapping/{dynamic_mapping}'
            ]
        },
        'firewall_vip46_realservers': {
            'params': [
                'vip46',
                'realservers',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/vip46/{vip46}/realservers/{realservers}',
                '/pm/config/global/obj/firewall/vip46/{vip46}/realservers/{realservers}'
            ]
        },
        'firewall_vip6': {
            'params': [
                'vip6',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/vip6/{vip6}',
                '/pm/config/global/obj/firewall/vip6/{vip6}'
            ]
        },
        'firewall_vip6_dynamicmapping': {
            'params': [
                'vip6',
                'dynamic_mapping',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/vip6/{vip6}/dynamic_mapping/{dynamic_mapping}',
                '/pm/config/global/obj/firewall/vip6/{vip6}/dynamic_mapping/{dynamic_mapping}'
            ]
        },
        'firewall_vip6_realservers': {
            'params': [
                'vip6',
                'realservers',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/vip6/{vip6}/realservers/{realservers}',
                '/pm/config/global/obj/firewall/vip6/{vip6}/realservers/{realservers}'
            ]
        },
        'firewall_vip6_sslciphersuites': {
            'params': [
                'vip6',
                'ssl-cipher-suites',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/vip6/{vip6}/ssl-cipher-suites/{ssl-cipher-suites}',
                '/pm/config/global/obj/firewall/vip6/{vip6}/ssl-cipher-suites/{ssl-cipher-suites}'
            ]
        },
        'firewall_vip6_sslserverciphersuites': {
            'params': [
                'vip6',
                'ssl-server-cipher-suites',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/vip6/{vip6}/ssl-server-cipher-suites/{ssl-server-cipher-suites}',
                '/pm/config/global/obj/firewall/vip6/{vip6}/ssl-server-cipher-suites/{ssl-server-cipher-suites}'
            ]
        },
        'firewall_vip64': {
            'params': [
                'vip64',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/vip64/{vip64}',
                '/pm/config/global/obj/firewall/vip64/{vip64}'
            ]
        },
        'firewall_vip64_dynamicmapping': {
            'params': [
                'vip64',
                'dynamic_mapping',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/vip64/{vip64}/dynamic_mapping/{dynamic_mapping}',
                '/pm/config/global/obj/firewall/vip64/{vip64}/dynamic_mapping/{dynamic_mapping}'
            ]
        },
        'firewall_vip64_realservers': {
            'params': [
                'vip64',
                'realservers',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/vip64/{vip64}/realservers/{realservers}',
                '/pm/config/global/obj/firewall/vip64/{vip64}/realservers/{realservers}'
            ]
        },
        'firewall_vipgrp': {
            'params': [
                'vipgrp',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/vipgrp/{vipgrp}',
                '/pm/config/global/obj/firewall/vipgrp/{vipgrp}'
            ]
        },
        'firewall_vipgrp_dynamicmapping': {
            'params': [
                'vipgrp',
                'dynamic_mapping',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/vipgrp/{vipgrp}/dynamic_mapping/{dynamic_mapping}',
                '/pm/config/global/obj/firewall/vipgrp/{vipgrp}/dynamic_mapping/{dynamic_mapping}'
            ]
        },
        'firewall_vipgrp46': {
            'params': [
                'vipgrp46',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/vipgrp46/{vipgrp46}',
                '/pm/config/global/obj/firewall/vipgrp46/{vipgrp46}'
            ]
        },
        'firewall_vipgrp6': {
            'params': [
                'vipgrp6',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/vipgrp6/{vipgrp6}',
                '/pm/config/global/obj/firewall/vipgrp6/{vipgrp6}'
            ]
        },
        'firewall_vipgrp64': {
            'params': [
                'vipgrp64',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/vipgrp64/{vipgrp64}',
                '/pm/config/global/obj/firewall/vipgrp64/{vipgrp64}'
            ]
        },
        'firewall_wildcardfqdn_custom': {
            'params': [
                'custom',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/wildcard-fqdn/custom/{custom}',
                '/pm/config/global/obj/firewall/wildcard-fqdn/custom/{custom}'
            ]
        },
        'firewall_wildcardfqdn_group': {
            'params': [
                'group',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/firewall/wildcard-fqdn/group/{group}',
                '/pm/config/global/obj/firewall/wildcard-fqdn/group/{group}'
            ]
        },
        'system_alertconsole': {
            'params': [
            ],
            'urls': [
                '/cli/global/system/alert-console'
            ]
        },
        'fmupdate_publicnetwork': {
            'params': [
            ],
            'urls': [
                '/cli/global/fmupdate/publicnetwork'
            ]
        },
        'metafields_system_admin_user': {
            'params': [
            ],
            'urls': [
                '/cli/global/_meta_fields/system/admin/user'
            ]
        },
        'system_logfetch_clientprofile': {
            'params': [
                'client-profile'
            ],
            'urls': [
                '/cli/global/system/log-fetch/client-profile/{client-profile}'
            ]
        },
        'system_logfetch_clientprofile_devicefilter': {
            'params': [
                'client-profile',
                'device-filter'
            ],
            'urls': [
                '/cli/global/system/log-fetch/client-profile/{client-profile}/device-filter/{device-filter}'
            ]
        },
        'system_logfetch_clientprofile_logfilter': {
            'params': [
                'client-profile',
                'log-filter'
            ],
            'urls': [
                '/cli/global/system/log-fetch/client-profile/{client-profile}/log-filter/{log-filter}'
            ]
        },
        'system_logfetch_serversettings': {
            'params': [
            ],
            'urls': [
                '/cli/global/system/log-fetch/server-settings'
            ]
        },
        'footer_consolidated_policy': {
            'params': [
                'policy',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/global/footer/consolidated/policy/{policy}'
            ]
        },
        'footer_policy': {
            'params': [
                'policy',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/global/footer/policy/{policy}'
            ]
        },
        'footer_policy_identitybasedpolicy': {
            'params': [
                'policy',
                'identity-based-policy',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/global/footer/policy/{policy}/identity-based-policy/{identity-based-policy}'
            ]
        },
        'footer_policy6': {
            'params': [
                'policy6',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/global/footer/policy6/{policy6}'
            ]
        },
        'footer_policy6_identitybasedpolicy6': {
            'params': [
                'policy6',
                'identity-based-policy6',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/global/footer/policy6/{policy6}/identity-based-policy6/{identity-based-policy6}'
            ]
        },
        'footer_shapingpolicy': {
            'params': [
                'shaping-policy',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/global/footer/shaping-policy/{shaping-policy}'
            ]
        },
        'header_consolidated_policy': {
            'params': [
                'policy',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/global/header/consolidated/policy/{policy}'
            ]
        },
        'header_policy': {
            'params': [
                'policy',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/global/header/policy/{policy}'
            ]
        },
        'header_policy_identitybasedpolicy': {
            'params': [
                'policy',
                'identity-based-policy',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/global/header/policy/{policy}/identity-based-policy/{identity-based-policy}'
            ]
        },
        'header_policy6': {
            'params': [
                'policy6',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/global/header/policy6/{policy6}'
            ]
        },
        'header_policy6_identitybasedpolicy6': {
            'params': [
                'policy6',
                'identity-based-policy6',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/global/header/policy6/{policy6}/identity-based-policy6/{identity-based-policy6}'
            ]
        },
        'header_shapingpolicy': {
            'params': [
                'shaping-policy',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/global/header/shaping-policy/{shaping-policy}'
            ]
        },
        'pkg_footer_consolidated_policy': {
            'params': [
                'pkg',
                'policy'
            ],
            'urls': [
                '/pm/config/global/pkg/{pkg}/global/footer/consolidated/policy/{policy}'
            ]
        },
        'pkg_footer_policy': {
            'params': [
                'pkg',
                'policy'
            ],
            'urls': [
                '/pm/config/global/pkg/{pkg}/global/footer/policy/{policy}'
            ]
        },
        'pkg_footer_policy_identitybasedpolicy': {
            'params': [
                'pkg',
                'policy',
                'identity-based-policy'
            ],
            'urls': [
                '/pm/config/global/pkg/{pkg}/global/footer/policy/{policy}/identity-based-policy/{identity-based-policy}'
            ]
        },
        'pkg_footer_policy6': {
            'params': [
                'pkg',
                'policy6'
            ],
            'urls': [
                '/pm/config/global/pkg/{pkg}/global/footer/policy6/{policy6}'
            ]
        },
        'pkg_footer_policy6_identitybasedpolicy6': {
            'params': [
                'pkg',
                'policy6',
                'identity-based-policy6'
            ],
            'urls': [
                '/pm/config/global/pkg/{pkg}/global/footer/policy6/{policy6}/identity-based-policy6/{identity-based-policy6}'
            ]
        },
        'pkg_footer_shapingpolicy': {
            'params': [
                'pkg',
                'shaping-policy'
            ],
            'urls': [
                '/pm/config/global/pkg/{pkg}/global/footer/shaping-policy/{shaping-policy}'
            ]
        },
        'pkg_header_consolidated_policy': {
            'params': [
                'pkg',
                'policy'
            ],
            'urls': [
                '/pm/config/global/pkg/{pkg}/global/header/consolidated/policy/{policy}'
            ]
        },
        'pkg_header_policy': {
            'params': [
                'pkg',
                'policy'
            ],
            'urls': [
                '/pm/config/global/pkg/{pkg}/global/header/policy/{policy}'
            ]
        },
        'pkg_header_policy_identitybasedpolicy': {
            'params': [
                'pkg',
                'policy',
                'identity-based-policy'
            ],
            'urls': [
                '/pm/config/global/pkg/{pkg}/global/header/policy/{policy}/identity-based-policy/{identity-based-policy}'
            ]
        },
        'pkg_header_policy6': {
            'params': [
                'pkg',
                'policy6'
            ],
            'urls': [
                '/pm/config/global/pkg/{pkg}/global/header/policy6/{policy6}'
            ]
        },
        'pkg_header_policy6_identitybasedpolicy6': {
            'params': [
                'pkg',
                'policy6',
                'identity-based-policy6'
            ],
            'urls': [
                '/pm/config/global/pkg/{pkg}/global/header/policy6/{policy6}/identity-based-policy6/{identity-based-policy6}'
            ]
        },
        'pkg_header_shapingpolicy': {
            'params': [
                'pkg',
                'shaping-policy'
            ],
            'urls': [
                '/pm/config/global/pkg/{pkg}/global/header/shaping-policy/{shaping-policy}'
            ]
        },
        'system_report_autocache': {
            'params': [
            ],
            'urls': [
                '/cli/global/system/report/auto-cache'
            ]
        },
        'system_report_estbrowsetime': {
            'params': [
            ],
            'urls': [
                '/cli/global/system/report/est-browse-time'
            ]
        },
        'system_report_group': {
            'params': [
                'group'
            ],
            'urls': [
                '/cli/global/system/report/group/{group}'
            ]
        },
        'system_report_group_chartalternative': {
            'params': [
                'group',
                'chart-alternative'
            ],
            'urls': [
                '/cli/global/system/report/group/{group}/chart-alternative/{chart-alternative}'
            ]
        },
        'system_report_group_groupby': {
            'params': [
                'group',
                'group-by'
            ],
            'urls': [
                '/cli/global/system/report/group/{group}/group-by/{group-by}'
            ]
        },
        'system_report_setting': {
            'params': [
            ],
            'urls': [
                '/cli/global/system/report/setting'
            ]
        },
        'waf_mainclass': {
            'params': [
                'main-class',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/waf/main-class/{main-class}',
                '/pm/config/global/obj/waf/main-class/{main-class}'
            ]
        },
        'waf_profile': {
            'params': [
                'profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/waf/profile/{profile}',
                '/pm/config/global/obj/waf/profile/{profile}'
            ]
        },
        'waf_profile_addresslist': {
            'params': [
                'profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/waf/profile/{profile}/address-list',
                '/pm/config/global/obj/waf/profile/{profile}/address-list'
            ]
        },
        'waf_profile_constraint': {
            'params': [
                'profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/waf/profile/{profile}/constraint',
                '/pm/config/global/obj/waf/profile/{profile}/constraint'
            ]
        },
        'waf_profile_constraint_contentlength': {
            'params': [
                'profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/waf/profile/{profile}/constraint/content-length',
                '/pm/config/global/obj/waf/profile/{profile}/constraint/content-length'
            ]
        },
        'waf_profile_constraint_exception': {
            'params': [
                'profile',
                'exception',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/waf/profile/{profile}/constraint/exception/{exception}',
                '/pm/config/global/obj/waf/profile/{profile}/constraint/exception/{exception}'
            ]
        },
        'waf_profile_constraint_headerlength': {
            'params': [
                'profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/waf/profile/{profile}/constraint/header-length',
                '/pm/config/global/obj/waf/profile/{profile}/constraint/header-length'
            ]
        },
        'waf_profile_constraint_hostname': {
            'params': [
                'profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/waf/profile/{profile}/constraint/hostname',
                '/pm/config/global/obj/waf/profile/{profile}/constraint/hostname'
            ]
        },
        'waf_profile_constraint_linelength': {
            'params': [
                'profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/waf/profile/{profile}/constraint/line-length',
                '/pm/config/global/obj/waf/profile/{profile}/constraint/line-length'
            ]
        },
        'waf_profile_constraint_malformed': {
            'params': [
                'profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/waf/profile/{profile}/constraint/malformed',
                '/pm/config/global/obj/waf/profile/{profile}/constraint/malformed'
            ]
        },
        'waf_profile_constraint_maxcookie': {
            'params': [
                'profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/waf/profile/{profile}/constraint/max-cookie',
                '/pm/config/global/obj/waf/profile/{profile}/constraint/max-cookie'
            ]
        },
        'waf_profile_constraint_maxheaderline': {
            'params': [
                'profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/waf/profile/{profile}/constraint/max-header-line',
                '/pm/config/global/obj/waf/profile/{profile}/constraint/max-header-line'
            ]
        },
        'waf_profile_constraint_maxrangesegment': {
            'params': [
                'profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/waf/profile/{profile}/constraint/max-range-segment',
                '/pm/config/global/obj/waf/profile/{profile}/constraint/max-range-segment'
            ]
        },
        'waf_profile_constraint_maxurlparam': {
            'params': [
                'profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/waf/profile/{profile}/constraint/max-url-param',
                '/pm/config/global/obj/waf/profile/{profile}/constraint/max-url-param'
            ]
        },
        'waf_profile_constraint_method': {
            'params': [
                'profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/waf/profile/{profile}/constraint/method',
                '/pm/config/global/obj/waf/profile/{profile}/constraint/method'
            ]
        },
        'waf_profile_constraint_paramlength': {
            'params': [
                'profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/waf/profile/{profile}/constraint/param-length',
                '/pm/config/global/obj/waf/profile/{profile}/constraint/param-length'
            ]
        },
        'waf_profile_constraint_urlparamlength': {
            'params': [
                'profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/waf/profile/{profile}/constraint/url-param-length',
                '/pm/config/global/obj/waf/profile/{profile}/constraint/url-param-length'
            ]
        },
        'waf_profile_constraint_version': {
            'params': [
                'profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/waf/profile/{profile}/constraint/version',
                '/pm/config/global/obj/waf/profile/{profile}/constraint/version'
            ]
        },
        'waf_profile_method': {
            'params': [
                'profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/waf/profile/{profile}/method',
                '/pm/config/global/obj/waf/profile/{profile}/method'
            ]
        },
        'waf_profile_method_methodpolicy': {
            'params': [
                'profile',
                'method-policy',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/waf/profile/{profile}/method/method-policy/{method-policy}',
                '/pm/config/global/obj/waf/profile/{profile}/method/method-policy/{method-policy}'
            ]
        },
        'waf_profile_signature': {
            'params': [
                'profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/waf/profile/{profile}/signature',
                '/pm/config/global/obj/waf/profile/{profile}/signature'
            ]
        },
        'waf_profile_signature_customsignature': {
            'params': [
                'profile',
                'custom-signature',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/waf/profile/{profile}/signature/custom-signature/{custom-signature}',
                '/pm/config/global/obj/waf/profile/{profile}/signature/custom-signature/{custom-signature}'
            ]
        },
        'waf_profile_signature_mainclass': {
            'params': [
                'profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/waf/profile/{profile}/signature/main-class',
                '/pm/config/global/obj/waf/profile/{profile}/signature/main-class'
            ]
        },
        'waf_profile_urlaccess': {
            'params': [
                'profile',
                'url-access',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/waf/profile/{profile}/url-access/{url-access}',
                '/pm/config/global/obj/waf/profile/{profile}/url-access/{url-access}'
            ]
        },
        'waf_profile_urlaccess_accesspattern': {
            'params': [
                'profile',
                'url-access',
                'access-pattern',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/waf/profile/{profile}/url-access/{url-access}/access-pattern/{access-pattern}',
                '/pm/config/global/obj/waf/profile/{profile}/url-access/{url-access}/access-pattern/{access-pattern}'
            ]
        },
        'waf_signature': {
            'params': [
                'signature',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/waf/signature/{signature}',
                '/pm/config/global/obj/waf/signature/{signature}'
            ]
        },
        'waf_subclass': {
            'params': [
                'sub-class',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/waf/sub-class/{sub-class}',
                '/pm/config/global/obj/waf/sub-class/{sub-class}'
            ]
        },
        'certificate_template': {
            'params': [
                'template',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/certificate/template/{template}',
                '/pm/config/global/obj/certificate/template/{template}'
            ]
        },
        'system_customlanguage': {
            'params': [
                'custom-language',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/system/custom-language/{custom-language}',
                '/pm/config/global/obj/system/custom-language/{custom-language}'
            ]
        },
        'system_dhcp_server': {
            'params': [
                'server',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/system/dhcp/server/{server}',
                '/pm/config/global/obj/system/dhcp/server/{server}'
            ]
        },
        'system_dhcp_server_excluderange': {
            'params': [
                'server',
                'exclude-range',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/system/dhcp/server/{server}/exclude-range/{exclude-range}',
                '/pm/config/global/obj/system/dhcp/server/{server}/exclude-range/{exclude-range}'
            ]
        },
        'system_dhcp_server_iprange': {
            'params': [
                'server',
                'ip-range',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/system/dhcp/server/{server}/ip-range/{ip-range}',
                '/pm/config/global/obj/system/dhcp/server/{server}/ip-range/{ip-range}'
            ]
        },
        'system_dhcp_server_options': {
            'params': [
                'server',
                'options',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/system/dhcp/server/{server}/options/{options}',
                '/pm/config/global/obj/system/dhcp/server/{server}/options/{options}'
            ]
        },
        'system_dhcp_server_reservedaddress': {
            'params': [
                'server',
                'reserved-address',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/system/dhcp/server/{server}/reserved-address/{reserved-address}',
                '/pm/config/global/obj/system/dhcp/server/{server}/reserved-address/{reserved-address}'
            ]
        },
        'system_externalresource': {
            'params': [
                'external-resource',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/system/external-resource/{external-resource}',
                '/pm/config/global/obj/system/external-resource/{external-resource}'
            ]
        },
        'system_fortiguard': {
            'params': [
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/system/fortiguard',
                '/pm/config/global/obj/system/fortiguard'
            ]
        },
        'system_geoipcountry': {
            'params': [
                'geoip-country',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/system/geoip-country/{geoip-country}',
                '/pm/config/global/obj/system/geoip-country/{geoip-country}'
            ]
        },
        'system_geoipoverride': {
            'params': [
                'geoip-override',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/system/geoip-override/{geoip-override}',
                '/pm/config/global/obj/system/geoip-override/{geoip-override}'
            ]
        },
        'system_geoipoverride_iprange': {
            'params': [
                'geoip-override',
                'ip-range',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/system/geoip-override/{geoip-override}/ip-range/{ip-range}',
                '/pm/config/global/obj/system/geoip-override/{geoip-override}/ip-range/{ip-range}'
            ]
        },
        'system_meta': {
            'params': [
                'meta',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/system/meta/{meta}',
                '/pm/config/global/obj/system/meta/{meta}'
            ]
        },
        'system_meta_sysmetafields': {
            'params': [
                'meta',
                'sys_meta_fields',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/system/meta/{meta}/sys_meta_fields/{sys_meta_fields}',
                '/pm/config/global/obj/system/meta/{meta}/sys_meta_fields/{sys_meta_fields}'
            ]
        },
        'system_objecttagging': {
            'params': [
                'object-tagging',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/system/object-tagging/{object-tagging}',
                '/pm/config/global/obj/system/object-tagging/{object-tagging}'
            ]
        },
        'system_replacemsggroup': {
            'params': [
                'replacemsg-group',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/system/replacemsg-group/{replacemsg-group}',
                '/pm/config/global/obj/system/replacemsg-group/{replacemsg-group}'
            ]
        },
        'system_replacemsggroup_admin': {
            'params': [
                'replacemsg-group',
                'admin',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/system/replacemsg-group/{replacemsg-group}/admin/{admin}',
                '/pm/config/global/obj/system/replacemsg-group/{replacemsg-group}/admin/{admin}'
            ]
        },
        'system_replacemsggroup_alertmail': {
            'params': [
                'replacemsg-group',
                'alertmail',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/system/replacemsg-group/{replacemsg-group}/alertmail/{alertmail}',
                '/pm/config/global/obj/system/replacemsg-group/{replacemsg-group}/alertmail/{alertmail}'
            ]
        },
        'system_replacemsggroup_auth': {
            'params': [
                'replacemsg-group',
                'auth',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/system/replacemsg-group/{replacemsg-group}/auth/{auth}',
                '/pm/config/global/obj/system/replacemsg-group/{replacemsg-group}/auth/{auth}'
            ]
        },
        'system_replacemsggroup_custommessage': {
            'params': [
                'replacemsg-group',
                'custom-message',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/system/replacemsg-group/{replacemsg-group}/custom-message/{custom-message}',
                '/pm/config/global/obj/system/replacemsg-group/{replacemsg-group}/custom-message/{custom-message}'
            ]
        },
        'system_replacemsggroup_devicedetectionportal': {
            'params': [
                'replacemsg-group',
                'device-detection-portal',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/system/replacemsg-group/{replacemsg-group}/device-detection-portal/{device-detection-portal}',
                '/pm/config/global/obj/system/replacemsg-group/{replacemsg-group}/device-detection-portal/{device-detection-portal}'
            ]
        },
        'system_replacemsggroup_ec': {
            'params': [
                'replacemsg-group',
                'ec',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/system/replacemsg-group/{replacemsg-group}/ec/{ec}',
                '/pm/config/global/obj/system/replacemsg-group/{replacemsg-group}/ec/{ec}'
            ]
        },
        'system_replacemsggroup_fortiguardwf': {
            'params': [
                'replacemsg-group',
                'fortiguard-wf',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/system/replacemsg-group/{replacemsg-group}/fortiguard-wf/{fortiguard-wf}',
                '/pm/config/global/obj/system/replacemsg-group/{replacemsg-group}/fortiguard-wf/{fortiguard-wf}'
            ]
        },
        'system_replacemsggroup_ftp': {
            'params': [
                'replacemsg-group',
                'ftp',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/system/replacemsg-group/{replacemsg-group}/ftp/{ftp}',
                '/pm/config/global/obj/system/replacemsg-group/{replacemsg-group}/ftp/{ftp}'
            ]
        },
        'system_replacemsggroup_http': {
            'params': [
                'replacemsg-group',
                'http',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/system/replacemsg-group/{replacemsg-group}/http/{http}',
                '/pm/config/global/obj/system/replacemsg-group/{replacemsg-group}/http/{http}'
            ]
        },
        'system_replacemsggroup_icap': {
            'params': [
                'replacemsg-group',
                'icap',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/system/replacemsg-group/{replacemsg-group}/icap/{icap}',
                '/pm/config/global/obj/system/replacemsg-group/{replacemsg-group}/icap/{icap}'
            ]
        },
        'system_replacemsggroup_mail': {
            'params': [
                'replacemsg-group',
                'mail',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/system/replacemsg-group/{replacemsg-group}/mail/{mail}',
                '/pm/config/global/obj/system/replacemsg-group/{replacemsg-group}/mail/{mail}'
            ]
        },
        'system_replacemsggroup_mm1': {
            'params': [
                'replacemsg-group',
                'mm1',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/system/replacemsg-group/{replacemsg-group}/mm1/{mm1}',
                '/pm/config/global/obj/system/replacemsg-group/{replacemsg-group}/mm1/{mm1}'
            ]
        },
        'system_replacemsggroup_mm3': {
            'params': [
                'replacemsg-group',
                'mm3',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/system/replacemsg-group/{replacemsg-group}/mm3/{mm3}',
                '/pm/config/global/obj/system/replacemsg-group/{replacemsg-group}/mm3/{mm3}'
            ]
        },
        'system_replacemsggroup_mm4': {
            'params': [
                'replacemsg-group',
                'mm4',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/system/replacemsg-group/{replacemsg-group}/mm4/{mm4}',
                '/pm/config/global/obj/system/replacemsg-group/{replacemsg-group}/mm4/{mm4}'
            ]
        },
        'system_replacemsggroup_mm7': {
            'params': [
                'replacemsg-group',
                'mm7',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/system/replacemsg-group/{replacemsg-group}/mm7/{mm7}',
                '/pm/config/global/obj/system/replacemsg-group/{replacemsg-group}/mm7/{mm7}'
            ]
        },
        'system_replacemsggroup_mms': {
            'params': [
                'replacemsg-group',
                'mms',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/system/replacemsg-group/{replacemsg-group}/mms/{mms}',
                '/pm/config/global/obj/system/replacemsg-group/{replacemsg-group}/mms/{mms}'
            ]
        },
        'system_replacemsggroup_nacquar': {
            'params': [
                'replacemsg-group',
                'nac-quar',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/system/replacemsg-group/{replacemsg-group}/nac-quar/{nac-quar}',
                '/pm/config/global/obj/system/replacemsg-group/{replacemsg-group}/nac-quar/{nac-quar}'
            ]
        },
        'system_replacemsggroup_nntp': {
            'params': [
                'replacemsg-group',
                'nntp',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/system/replacemsg-group/{replacemsg-group}/nntp/{nntp}',
                '/pm/config/global/obj/system/replacemsg-group/{replacemsg-group}/nntp/{nntp}'
            ]
        },
        'system_replacemsggroup_spam': {
            'params': [
                'replacemsg-group',
                'spam',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/system/replacemsg-group/{replacemsg-group}/spam/{spam}',
                '/pm/config/global/obj/system/replacemsg-group/{replacemsg-group}/spam/{spam}'
            ]
        },
        'system_replacemsggroup_sslvpn': {
            'params': [
                'replacemsg-group',
                'sslvpn',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/system/replacemsg-group/{replacemsg-group}/sslvpn/{sslvpn}',
                '/pm/config/global/obj/system/replacemsg-group/{replacemsg-group}/sslvpn/{sslvpn}'
            ]
        },
        'system_replacemsggroup_trafficquota': {
            'params': [
                'replacemsg-group',
                'traffic-quota',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/system/replacemsg-group/{replacemsg-group}/traffic-quota/{traffic-quota}',
                '/pm/config/global/obj/system/replacemsg-group/{replacemsg-group}/traffic-quota/{traffic-quota}'
            ]
        },
        'system_replacemsggroup_utm': {
            'params': [
                'replacemsg-group',
                'utm',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/system/replacemsg-group/{replacemsg-group}/utm/{utm}',
                '/pm/config/global/obj/system/replacemsg-group/{replacemsg-group}/utm/{utm}'
            ]
        },
        'system_replacemsggroup_webproxy': {
            'params': [
                'replacemsg-group',
                'webproxy',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/system/replacemsg-group/{replacemsg-group}/webproxy/{webproxy}',
                '/pm/config/global/obj/system/replacemsg-group/{replacemsg-group}/webproxy/{webproxy}'
            ]
        },
        'system_replacemsgimage': {
            'params': [
                'replacemsg-image',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/system/replacemsg-image/{replacemsg-image}',
                '/pm/config/global/obj/system/replacemsg-image/{replacemsg-image}'
            ]
        },
        'system_sdnconnector': {
            'params': [
                'sdn-connector',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/system/sdn-connector/{sdn-connector}',
                '/pm/config/global/obj/system/sdn-connector/{sdn-connector}'
            ]
        },
        'system_sdnconnector_externalip': {
            'params': [
                'sdn-connector',
                'external-ip',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/system/sdn-connector/{sdn-connector}/external-ip/{external-ip}',
                '/pm/config/global/obj/system/sdn-connector/{sdn-connector}/external-ip/{external-ip}'
            ]
        },
        'system_sdnconnector_nic': {
            'params': [
                'sdn-connector',
                'nic',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/system/sdn-connector/{sdn-connector}/nic/{nic}',
                '/pm/config/global/obj/system/sdn-connector/{sdn-connector}/nic/{nic}'
            ]
        },
        'system_sdnconnector_nic_ip': {
            'params': [
                'sdn-connector',
                'nic',
                'ip',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/system/sdn-connector/{sdn-connector}/nic/{nic}/ip/{ip}',
                '/pm/config/global/obj/system/sdn-connector/{sdn-connector}/nic/{nic}/ip/{ip}'
            ]
        },
        'system_sdnconnector_route': {
            'params': [
                'sdn-connector',
                'route',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/system/sdn-connector/{sdn-connector}/route/{route}',
                '/pm/config/global/obj/system/sdn-connector/{sdn-connector}/route/{route}'
            ]
        },
        'system_sdnconnector_routetable': {
            'params': [
                'sdn-connector',
                'route-table',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/system/sdn-connector/{sdn-connector}/route-table/{route-table}',
                '/pm/config/global/obj/system/sdn-connector/{sdn-connector}/route-table/{route-table}'
            ]
        },
        'system_sdnconnector_routetable_route': {
            'params': [
                'sdn-connector',
                'route-table',
                'route',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/system/sdn-connector/{sdn-connector}/route-table/{route-table}/route/{route}',
                '/pm/config/global/obj/system/sdn-connector/{sdn-connector}/route-table/{route-table}/route/{route}'
            ]
        },
        'system_smsserver': {
            'params': [
                'sms-server',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/system/sms-server/{sms-server}',
                '/pm/config/global/obj/system/sms-server/{sms-server}'
            ]
        },
        'system_virtualwirepair': {
            'params': [
                'virtual-wire-pair',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/system/virtual-wire-pair/{virtual-wire-pair}',
                '/pm/config/global/obj/system/virtual-wire-pair/{virtual-wire-pair}'
            ]
        },
        'template': {
            'params': [
                'template',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/cli/template/{template}',
                '/pm/config/global/obj/cli/template/{template}'
            ]
        },
        'templategroup': {
            'params': [
                'template-group',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/cli/template-group/{template-group}',
                '/pm/config/global/obj/cli/template-group/{template-group}'
            ]
        },
        'dvmdb_group': {
            'params': [
                'group',
                'adom'
            ],
            'urls': [
                '/dvmdb/adom/{adom}/group/{group}',
                '/dvmdb/group/{group}'
            ]
        },
        'wanprof_system_virtualwanlink': {
            'params': [
                'wanprof',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/wanprof/{wanprof}/system/virtual-wan-link'
            ]
        },
        'wanprof_system_virtualwanlink_healthcheck': {
            'params': [
                'wanprof',
                'health-check',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/wanprof/{wanprof}/system/virtual-wan-link/health-check/{health-check}'
            ]
        },
        'wanprof_system_virtualwanlink_healthcheck_sla': {
            'params': [
                'wanprof',
                'health-check',
                'sla',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/wanprof/{wanprof}/system/virtual-wan-link/health-check/{health-check}/sla/{sla}'
            ]
        },
        'wanprof_system_virtualwanlink_members': {
            'params': [
                'wanprof',
                'members',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/wanprof/{wanprof}/system/virtual-wan-link/members/{members}'
            ]
        },
        'wanprof_system_virtualwanlink_service': {
            'params': [
                'wanprof',
                'service',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/wanprof/{wanprof}/system/virtual-wan-link/service/{service}'
            ]
        },
        'wanprof_system_virtualwanlink_service_sla': {
            'params': [
                'wanprof',
                'service',
                'sla',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/wanprof/{wanprof}/system/virtual-wan-link/service/{service}/sla/{sla}'
            ]
        },
        'sshfilter_profile': {
            'params': [
                'profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/ssh-filter/profile/{profile}',
                '/pm/config/global/obj/ssh-filter/profile/{profile}'
            ]
        },
        'sshfilter_profile_shellcommands': {
            'params': [
                'profile',
                'shell-commands',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/ssh-filter/profile/{profile}/shell-commands/{shell-commands}',
                '/pm/config/global/obj/ssh-filter/profile/{profile}/shell-commands/{shell-commands}'
            ]
        },
        'system_dm': {
            'params': [
            ],
            'urls': [
                '/cli/global/system/dm'
            ]
        },
        'fsp_vlan': {
            'params': [
                'vlan',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/fsp/vlan/{vlan}',
                '/pm/config/global/obj/fsp/vlan/{vlan}'
            ]
        },
        'fsp_vlan_dhcpserver': {
            'params': [
                'vlan',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/fsp/vlan/{vlan}/dhcp-server',
                '/pm/config/global/obj/fsp/vlan/{vlan}/dhcp-server'
            ]
        },
        'fsp_vlan_dhcpserver_excluderange': {
            'params': [
                'vlan',
                'exclude-range',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/fsp/vlan/{vlan}/dhcp-server/exclude-range/{exclude-range}',
                '/pm/config/global/obj/fsp/vlan/{vlan}/dhcp-server/exclude-range/{exclude-range}'
            ]
        },
        'fsp_vlan_dhcpserver_iprange': {
            'params': [
                'vlan',
                'ip-range',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/fsp/vlan/{vlan}/dhcp-server/ip-range/{ip-range}',
                '/pm/config/global/obj/fsp/vlan/{vlan}/dhcp-server/ip-range/{ip-range}'
            ]
        },
        'fsp_vlan_dhcpserver_options': {
            'params': [
                'vlan',
                'options',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/fsp/vlan/{vlan}/dhcp-server/options/{options}',
                '/pm/config/global/obj/fsp/vlan/{vlan}/dhcp-server/options/{options}'
            ]
        },
        'fsp_vlan_dhcpserver_reservedaddress': {
            'params': [
                'vlan',
                'reserved-address',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/fsp/vlan/{vlan}/dhcp-server/reserved-address/{reserved-address}',
                '/pm/config/global/obj/fsp/vlan/{vlan}/dhcp-server/reserved-address/{reserved-address}'
            ]
        },
        'fsp_vlan_dynamicmapping': {
            'params': [
                'vlan',
                'dynamic_mapping',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/fsp/vlan/{vlan}/dynamic_mapping/{dynamic_mapping}',
                '/pm/config/global/obj/fsp/vlan/{vlan}/dynamic_mapping/{dynamic_mapping}'
            ]
        },
        'fsp_vlan_dynamicmapping_dhcpserver': {
            'params': [
                'vlan',
                'dynamic_mapping',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/fsp/vlan/{vlan}/dynamic_mapping/{dynamic_mapping}/dhcp-server',
                '/pm/config/global/obj/fsp/vlan/{vlan}/dynamic_mapping/{dynamic_mapping}/dhcp-server'
            ]
        },
        'fsp_vlan_dynamicmapping_dhcpserver_excluderange': {
            'params': [
                'vlan',
                'dynamic_mapping',
                'exclude-range',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/fsp/vlan/{vlan}/dynamic_mapping/{dynamic_mapping}/dhcp-server/exclude-range/{exclude-range}',
                '/pm/config/global/obj/fsp/vlan/{vlan}/dynamic_mapping/{dynamic_mapping}/dhcp-server/exclude-range/{exclude-range}'
            ]
        },
        'fsp_vlan_dynamicmapping_dhcpserver_iprange': {
            'params': [
                'vlan',
                'dynamic_mapping',
                'ip-range',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/fsp/vlan/{vlan}/dynamic_mapping/{dynamic_mapping}/dhcp-server/ip-range/{ip-range}',
                '/pm/config/global/obj/fsp/vlan/{vlan}/dynamic_mapping/{dynamic_mapping}/dhcp-server/ip-range/{ip-range}'
            ]
        },
        'fsp_vlan_dynamicmapping_dhcpserver_options': {
            'params': [
                'vlan',
                'dynamic_mapping',
                'options',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/fsp/vlan/{vlan}/dynamic_mapping/{dynamic_mapping}/dhcp-server/options/{options}',
                '/pm/config/global/obj/fsp/vlan/{vlan}/dynamic_mapping/{dynamic_mapping}/dhcp-server/options/{options}'
            ]
        },
        'fsp_vlan_dynamicmapping_dhcpserver_reservedaddress': {
            'params': [
                'vlan',
                'dynamic_mapping',
                'reserved-address',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/fsp/vlan/{vlan}/dynamic_mapping/{dynamic_mapping}/dhcp-server/reserved-address/{reserved-address}',
                '/pm/config/global/obj/fsp/vlan/{vlan}/dynamic_mapping/{dynamic_mapping}/dhcp-server/reserved-address/{reserved-address}'
            ]
        },
        'fsp_vlan_dynamicmapping_interface': {
            'params': [
                'vlan',
                'dynamic_mapping',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/fsp/vlan/{vlan}/dynamic_mapping/{dynamic_mapping}/interface',
                '/pm/config/global/obj/fsp/vlan/{vlan}/dynamic_mapping/{dynamic_mapping}/interface'
            ]
        },
        'fsp_vlan_interface': {
            'params': [
                'vlan',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/fsp/vlan/{vlan}/interface',
                '/pm/config/global/obj/fsp/vlan/{vlan}/interface'
            ]
        },
        'fsp_vlan_interface_ipv6': {
            'params': [
                'vlan',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/fsp/vlan/{vlan}/interface/ipv6',
                '/pm/config/global/obj/fsp/vlan/{vlan}/interface/ipv6'
            ]
        },
        'fsp_vlan_interface_secondaryip': {
            'params': [
                'vlan',
                'secondaryip',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/fsp/vlan/{vlan}/interface/secondaryip/{secondaryip}',
                '/pm/config/global/obj/fsp/vlan/{vlan}/interface/secondaryip/{secondaryip}'
            ]
        },
        'fsp_vlan_interface_vrrp': {
            'params': [
                'vlan',
                'vrrp',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/fsp/vlan/{vlan}/interface/vrrp/{vrrp}',
                '/pm/config/global/obj/fsp/vlan/{vlan}/interface/vrrp/{vrrp}'
            ]
        },
        'system_sql': {
            'params': [
            ],
            'urls': [
                '/cli/global/system/sql'
            ]
        },
        'system_sql_customindex': {
            'params': [
                'custom-index'
            ],
            'urls': [
                '/cli/global/system/sql/custom-index/{custom-index}'
            ]
        },
        'system_sql_tsindexfield': {
            'params': [
                'ts-index-field'
            ],
            'urls': [
                '/cli/global/system/sql/ts-index-field/{ts-index-field}'
            ]
        },
        'system_passwordpolicy': {
            'params': [
            ],
            'urls': [
                '/cli/global/system/password-policy'
            ]
        },
        'pm_wanprof_adom': {
            'params': [
                'adom'
            ],
            'urls': [
                '/pm/wanprof/adom/{adom}'
            ]
        },
        'pm_wanprof': {
            'params': [
                'pkg_path',
                'adom'
            ],
            'urls': [
                '/pm/wanprof/adom/{adom}/{pkg_path}'
            ]
        },
        'fmupdate_fdssetting': {
            'params': [
            ],
            'urls': [
                '/cli/global/fmupdate/fds-setting'
            ]
        },
        'fmupdate_fdssetting_pushoverride': {
            'params': [
            ],
            'urls': [
                '/cli/global/fmupdate/fds-setting/push-override'
            ]
        },
        'fmupdate_fdssetting_pushoverridetoclient': {
            'params': [
            ],
            'urls': [
                '/cli/global/fmupdate/fds-setting/push-override-to-client'
            ]
        },
        'fmupdate_fdssetting_pushoverridetoclient_announceip': {
            'params': [
                'announce-ip'
            ],
            'urls': [
                '/cli/global/fmupdate/fds-setting/push-override-to-client/announce-ip/{announce-ip}'
            ]
        },
        'fmupdate_fdssetting_serveroverride': {
            'params': [
            ],
            'urls': [
                '/cli/global/fmupdate/fds-setting/server-override'
            ]
        },
        'fmupdate_fdssetting_serveroverride_servlist': {
            'params': [
                'servlist'
            ],
            'urls': [
                '/cli/global/fmupdate/fds-setting/server-override/servlist/{servlist}'
            ]
        },
        'fmupdate_fdssetting_updateschedule': {
            'params': [
            ],
            'urls': [
                '/cli/global/fmupdate/fds-setting/update-schedule'
            ]
        },
        'fmupdate_serveroverridestatus': {
            'params': [
            ],
            'urls': [
                '/cli/global/fmupdate/server-override-status'
            ]
        },
        'pm_pkg_adom': {
            'params': [
                'adom'
            ],
            'urls': [
                '/pm/pkg/adom/{adom}'
            ]
        },
        'pm_pkg': {
            'params': [
                'pkg_path',
                'adom'
            ],
            'urls': [
                '/pm/pkg/adom/{adom}/{pkg_path}',
                '/pm/pkg/global/{pkg_path}'
            ]
        },
        'pm_pkg_global': {
            'params': [
            ],
            'urls': [
                '/pm/pkg/global'
            ]
        },
        'system_autodelete': {
            'params': [
            ],
            'urls': [
                '/cli/global/system/auto-delete'
            ]
        },
        'system_autodelete_dlpfilesautodeletion': {
            'params': [
            ],
            'urls': [
                '/cli/global/system/auto-delete/dlp-files-auto-deletion'
            ]
        },
        'system_autodelete_logautodeletion': {
            'params': [
            ],
            'urls': [
                '/cli/global/system/auto-delete/log-auto-deletion'
            ]
        },
        'system_autodelete_quarantinefilesautodeletion': {
            'params': [
            ],
            'urls': [
                '/cli/global/system/auto-delete/quarantine-files-auto-deletion'
            ]
        },
        'system_autodelete_reportautodeletion': {
            'params': [
            ],
            'urls': [
                '/cli/global/system/auto-delete/report-auto-deletion'
            ]
        },
        'devprof_system_centralmanagement': {
            'params': [
                'devprof',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/devprof/{devprof}/system/central-management'
            ]
        },
        'devprof_system_centralmanagement_serverlist': {
            'params': [
                'devprof',
                'server-list',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/devprof/{devprof}/system/central-management/server-list/{server-list}'
            ]
        },
        'devprof_system_dns': {
            'params': [
                'devprof',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/devprof/{devprof}/system/dns'
            ]
        },
        'devprof_system_emailserver': {
            'params': [
                'devprof',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/devprof/{devprof}/system/email-server'
            ]
        },
        'devprof_system_global': {
            'params': [
                'devprof',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/devprof/{devprof}/system/global'
            ]
        },
        'devprof_system_ntp': {
            'params': [
                'devprof',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/devprof/{devprof}/system/ntp'
            ]
        },
        'devprof_system_ntp_ntpserver': {
            'params': [
                'devprof',
                'ntpserver',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/devprof/{devprof}/system/ntp/ntpserver/{ntpserver}'
            ]
        },
        'devprof_system_replacemsg_admin': {
            'params': [
                'devprof',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/devprof/{devprof}/system/replacemsg/admin'
            ]
        },
        'devprof_system_replacemsg_alertmail': {
            'params': [
                'devprof',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/devprof/{devprof}/system/replacemsg/alertmail'
            ]
        },
        'devprof_system_replacemsg_auth': {
            'params': [
                'devprof',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/devprof/{devprof}/system/replacemsg/auth'
            ]
        },
        'devprof_system_replacemsg_devicedetectionportal': {
            'params': [
                'devprof',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/devprof/{devprof}/system/replacemsg/device-detection-portal'
            ]
        },
        'devprof_system_replacemsg_ec': {
            'params': [
                'devprof',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/devprof/{devprof}/system/replacemsg/ec'
            ]
        },
        'devprof_system_replacemsg_fortiguardwf': {
            'params': [
                'devprof',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/devprof/{devprof}/system/replacemsg/fortiguard-wf'
            ]
        },
        'devprof_system_replacemsg_ftp': {
            'params': [
                'devprof',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/devprof/{devprof}/system/replacemsg/ftp'
            ]
        },
        'devprof_system_replacemsg_http': {
            'params': [
                'devprof',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/devprof/{devprof}/system/replacemsg/http'
            ]
        },
        'devprof_system_replacemsg_mail': {
            'params': [
                'devprof',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/devprof/{devprof}/system/replacemsg/mail'
            ]
        },
        'devprof_system_replacemsg_mms': {
            'params': [
                'devprof',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/devprof/{devprof}/system/replacemsg/mms'
            ]
        },
        'devprof_system_replacemsg_nacquar': {
            'params': [
                'devprof',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/devprof/{devprof}/system/replacemsg/nac-quar'
            ]
        },
        'devprof_system_replacemsg_nntp': {
            'params': [
                'devprof',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/devprof/{devprof}/system/replacemsg/nntp'
            ]
        },
        'devprof_system_replacemsg_spam': {
            'params': [
                'devprof',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/devprof/{devprof}/system/replacemsg/spam'
            ]
        },
        'devprof_system_replacemsg_sslvpn': {
            'params': [
                'devprof',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/devprof/{devprof}/system/replacemsg/sslvpn'
            ]
        },
        'devprof_system_replacemsg_trafficquota': {
            'params': [
                'devprof',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/devprof/{devprof}/system/replacemsg/traffic-quota'
            ]
        },
        'devprof_system_replacemsg_utm': {
            'params': [
                'devprof',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/devprof/{devprof}/system/replacemsg/utm'
            ]
        },
        'devprof_system_replacemsg_webproxy': {
            'params': [
                'devprof',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/devprof/{devprof}/system/replacemsg/webproxy'
            ]
        },
        'devprof_system_snmp_community': {
            'params': [
                'devprof',
                'community',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/devprof/{devprof}/system/snmp/community/{community}'
            ]
        },
        'devprof_system_snmp_community_hosts': {
            'params': [
                'devprof',
                'community',
                'hosts',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/devprof/{devprof}/system/snmp/community/{community}/hosts/{hosts}'
            ]
        },
        'devprof_system_snmp_community_hosts6': {
            'params': [
                'devprof',
                'community',
                'hosts6',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/devprof/{devprof}/system/snmp/community/{community}/hosts6/{hosts6}'
            ]
        },
        'devprof_system_snmp_sysinfo': {
            'params': [
                'devprof',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/devprof/{devprof}/system/snmp/sysinfo'
            ]
        },
        'devprof_system_snmp_user': {
            'params': [
                'devprof',
                'user',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/devprof/{devprof}/system/snmp/user/{user}'
            ]
        },
        'system_locallog_disk_filter': {
            'params': [
            ],
            'urls': [
                '/cli/global/system/locallog/disk/filter'
            ]
        },
        'system_locallog_disk_setting': {
            'params': [
            ],
            'urls': [
                '/cli/global/system/locallog/disk/setting'
            ]
        },
        'system_locallog_fortianalyzer_filter': {
            'params': [
            ],
            'urls': [
                '/cli/global/system/locallog/fortianalyzer/filter'
            ]
        },
        'system_locallog_fortianalyzer_setting': {
            'params': [
            ],
            'urls': [
                '/cli/global/system/locallog/fortianalyzer/setting'
            ]
        },
        'system_locallog_fortianalyzer2_filter': {
            'params': [
            ],
            'urls': [
                '/cli/global/system/locallog/fortianalyzer2/filter'
            ]
        },
        'system_locallog_fortianalyzer2_setting': {
            'params': [
            ],
            'urls': [
                '/cli/global/system/locallog/fortianalyzer2/setting'
            ]
        },
        'system_locallog_fortianalyzer3_filter': {
            'params': [
            ],
            'urls': [
                '/cli/global/system/locallog/fortianalyzer3/filter'
            ]
        },
        'system_locallog_fortianalyzer3_setting': {
            'params': [
            ],
            'urls': [
                '/cli/global/system/locallog/fortianalyzer3/setting'
            ]
        },
        'system_locallog_memory_filter': {
            'params': [
            ],
            'urls': [
                '/cli/global/system/locallog/memory/filter'
            ]
        },
        'system_locallog_memory_setting': {
            'params': [
            ],
            'urls': [
                '/cli/global/system/locallog/memory/setting'
            ]
        },
        'system_locallog_setting': {
            'params': [
            ],
            'urls': [
                '/cli/global/system/locallog/setting'
            ]
        },
        'system_locallog_syslogd_filter': {
            'params': [
            ],
            'urls': [
                '/cli/global/system/locallog/syslogd/filter'
            ]
        },
        'system_locallog_syslogd_setting': {
            'params': [
            ],
            'urls': [
                '/cli/global/system/locallog/syslogd/setting'
            ]
        },
        'system_locallog_syslogd2_filter': {
            'params': [
            ],
            'urls': [
                '/cli/global/system/locallog/syslogd2/filter'
            ]
        },
        'system_locallog_syslogd2_setting': {
            'params': [
            ],
            'urls': [
                '/cli/global/system/locallog/syslogd2/setting'
            ]
        },
        'system_locallog_syslogd3_filter': {
            'params': [
            ],
            'urls': [
                '/cli/global/system/locallog/syslogd3/filter'
            ]
        },
        'system_locallog_syslogd3_setting': {
            'params': [
            ],
            'urls': [
                '/cli/global/system/locallog/syslogd3/setting'
            ]
        },
        'system_saml': {
            'params': [
            ],
            'urls': [
                '/cli/global/system/saml'
            ]
        },
        'system_saml_serviceproviders': {
            'params': [
                'service-providers'
            ],
            'urls': [
                '/cli/global/system/saml/service-providers/{service-providers}'
            ]
        },
        'bleprofile': {
            'params': [
                'ble-profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/wireless-controller/ble-profile/{ble-profile}',
                '/pm/config/global/obj/wireless-controller/ble-profile/{ble-profile}'
            ]
        },
        'bonjourprofile': {
            'params': [
                'bonjour-profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/wireless-controller/bonjour-profile/{bonjour-profile}',
                '/pm/config/global/obj/wireless-controller/bonjour-profile/{bonjour-profile}'
            ]
        },
        'bonjourprofile_policylist': {
            'params': [
                'bonjour-profile',
                'policy-list',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/wireless-controller/bonjour-profile/{bonjour-profile}/policy-list/{policy-list}',
                '/pm/config/global/obj/wireless-controller/bonjour-profile/{bonjour-profile}/policy-list/{policy-list}'
            ]
        },
        'hotspot20_anqp3gppcellular': {
            'params': [
                'anqp-3gpp-cellular',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/wireless-controller/hotspot20/anqp-3gpp-cellular/{anqp-3gpp-cellular}',
                '/pm/config/global/obj/wireless-controller/hotspot20/anqp-3gpp-cellular/{anqp-3gpp-cellular}'
            ]
        },
        'hotspot20_anqp3gppcellular_mccmnclist': {
            'params': [
                'anqp-3gpp-cellular',
                'mcc-mnc-list',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/wireless-controller/hotspot20/anqp-3gpp-cellular/{anqp-3gpp-cellular}/mcc-mnc-list/{mcc-mnc-list}',
                '/pm/config/global/obj/wireless-controller/hotspot20/anqp-3gpp-cellular/{anqp-3gpp-cellular}/mcc-mnc-list/{mcc-mnc-list}'
            ]
        },
        'hotspot20_anqpipaddresstype': {
            'params': [
                'anqp-ip-address-type',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/wireless-controller/hotspot20/anqp-ip-address-type/{anqp-ip-address-type}',
                '/pm/config/global/obj/wireless-controller/hotspot20/anqp-ip-address-type/{anqp-ip-address-type}'
            ]
        },
        'hotspot20_anqpnairealm': {
            'params': [
                'anqp-nai-realm',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/wireless-controller/hotspot20/anqp-nai-realm/{anqp-nai-realm}',
                '/pm/config/global/obj/wireless-controller/hotspot20/anqp-nai-realm/{anqp-nai-realm}'
            ]
        },
        'hotspot20_anqpnairealm_nailist': {
            'params': [
                'anqp-nai-realm',
                'nai-list',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/wireless-controller/hotspot20/anqp-nai-realm/{anqp-nai-realm}/nai-list/{nai-list}',
                '/pm/config/global/obj/wireless-controller/hotspot20/anqp-nai-realm/{anqp-nai-realm}/nai-list/{nai-list}'
            ]
        },
        'hotspot20_anqpnairealm_nailist_eapmethod': {
            'params': [
                'anqp-nai-realm',
                'nai-list',
                'eap-method',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/wireless-controller/hotspot20/anqp-nai-realm/{anqp-nai-realm}/nai-list/{nai-list}/eap-method/{eap-method}',
                '/pm/config/global/obj/wireless-controller/hotspot20/anqp-nai-realm/{anqp-nai-realm}/nai-list/{nai-list}/eap-method/{eap-method}'
            ]
        },
        'hotspot20_anqpnairealm_nailist_eapmethod_authparam': {
            'params': [
                'anqp-nai-realm',
                'nai-list',
                'eap-method',
                'auth-param',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/wireless-controller/hotspot20/anqp-nai-realm/{anqp-nai-realm}/nai-list/{nai-list}/eap-method/{eap-method}/auth-param/{auth-param}',
                '/pm/config/global/obj/wireless-controller/hotspot20/anqp-nai-realm/{anqp-nai-realm}/nai-list/{nai-list}/eap-method/{eap-method}/auth-param/{auth-param}'
            ]
        },
        'hotspot20_anqpnetworkauthtype': {
            'params': [
                'anqp-network-auth-type',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/wireless-controller/hotspot20/anqp-network-auth-type/{anqp-network-auth-type}',
                '/pm/config/global/obj/wireless-controller/hotspot20/anqp-network-auth-type/{anqp-network-auth-type}'
            ]
        },
        'hotspot20_anqproamingconsortium': {
            'params': [
                'anqp-roaming-consortium',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/wireless-controller/hotspot20/anqp-roaming-consortium/{anqp-roaming-consortium}',
                '/pm/config/global/obj/wireless-controller/hotspot20/anqp-roaming-consortium/{anqp-roaming-consortium}'
            ]
        },
        'hotspot20_anqproamingconsortium_oilist': {
            'params': [
                'anqp-roaming-consortium',
                'oi-list',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/wireless-controller/hotspot20/anqp-roaming-consortium/{anqp-roaming-consortium}/oi-list/{oi-list}',
                '/pm/config/global/obj/wireless-controller/hotspot20/anqp-roaming-consortium/{anqp-roaming-consortium}/oi-list/{oi-list}'
            ]
        },
        'hotspot20_anqpvenuename': {
            'params': [
                'anqp-venue-name',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/wireless-controller/hotspot20/anqp-venue-name/{anqp-venue-name}',
                '/pm/config/global/obj/wireless-controller/hotspot20/anqp-venue-name/{anqp-venue-name}'
            ]
        },
        'hotspot20_anqpvenuename_valuelist': {
            'params': [
                'anqp-venue-name',
                'value-list',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/wireless-controller/hotspot20/anqp-venue-name/{anqp-venue-name}/value-list/{value-list}',
                '/pm/config/global/obj/wireless-controller/hotspot20/anqp-venue-name/{anqp-venue-name}/value-list/{value-list}'
            ]
        },
        'hotspot20_h2qpconncapability': {
            'params': [
                'h2qp-conn-capability',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/wireless-controller/hotspot20/h2qp-conn-capability/{h2qp-conn-capability}',
                '/pm/config/global/obj/wireless-controller/hotspot20/h2qp-conn-capability/{h2qp-conn-capability}'
            ]
        },
        'hotspot20_h2qpoperatorname': {
            'params': [
                'h2qp-operator-name',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/wireless-controller/hotspot20/h2qp-operator-name/{h2qp-operator-name}',
                '/pm/config/global/obj/wireless-controller/hotspot20/h2qp-operator-name/{h2qp-operator-name}'
            ]
        },
        'hotspot20_h2qpoperatorname_valuelist': {
            'params': [
                'h2qp-operator-name',
                'value-list',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/wireless-controller/hotspot20/h2qp-operator-name/{h2qp-operator-name}/value-list/{value-list}',
                '/pm/config/global/obj/wireless-controller/hotspot20/h2qp-operator-name/{h2qp-operator-name}/value-list/{value-list}'
            ]
        },
        'hotspot20_h2qposuprovider': {
            'params': [
                'h2qp-osu-provider',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/wireless-controller/hotspot20/h2qp-osu-provider/{h2qp-osu-provider}',
                '/pm/config/global/obj/wireless-controller/hotspot20/h2qp-osu-provider/{h2qp-osu-provider}'
            ]
        },
        'hotspot20_h2qposuprovider_friendlyname': {
            'params': [
                'h2qp-osu-provider',
                'friendly-name',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/wireless-controller/hotspot20/h2qp-osu-provider/{h2qp-osu-provider}/friendly-name/{friendly-name}',
                '/pm/config/global/obj/wireless-controller/hotspot20/h2qp-osu-provider/{h2qp-osu-provider}/friendly-name/{friendly-name}'
            ]
        },
        'hotspot20_h2qposuprovider_servicedescription': {
            'params': [
                'h2qp-osu-provider',
                'service-description',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/wireless-controller/hotspot20/h2qp-osu-provider/{h2qp-osu-provider}/service-description/{service-description}',
                '/pm/config/global/obj/wireless-controller/hotspot20/h2qp-osu-provider/{h2qp-osu-provider}/service-description/{service-description}'
            ]
        },
        'hotspot20_h2qpwanmetric': {
            'params': [
                'h2qp-wan-metric',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/wireless-controller/hotspot20/h2qp-wan-metric/{h2qp-wan-metric}',
                '/pm/config/global/obj/wireless-controller/hotspot20/h2qp-wan-metric/{h2qp-wan-metric}'
            ]
        },
        'hotspot20_hsprofile': {
            'params': [
                'hs-profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/wireless-controller/hotspot20/hs-profile/{hs-profile}',
                '/pm/config/global/obj/wireless-controller/hotspot20/hs-profile/{hs-profile}'
            ]
        },
        'hotspot20_qosmap': {
            'params': [
                'qos-map',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/wireless-controller/hotspot20/qos-map/{qos-map}',
                '/pm/config/global/obj/wireless-controller/hotspot20/qos-map/{qos-map}'
            ]
        },
        'hotspot20_qosmap_dscpexcept': {
            'params': [
                'qos-map',
                'dscp-except',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/wireless-controller/hotspot20/qos-map/{qos-map}/dscp-except/{dscp-except}',
                '/pm/config/global/obj/wireless-controller/hotspot20/qos-map/{qos-map}/dscp-except/{dscp-except}'
            ]
        },
        'hotspot20_qosmap_dscprange': {
            'params': [
                'qos-map',
                'dscp-range',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/wireless-controller/hotspot20/qos-map/{qos-map}/dscp-range/{dscp-range}',
                '/pm/config/global/obj/wireless-controller/hotspot20/qos-map/{qos-map}/dscp-range/{dscp-range}'
            ]
        },
        'qosprofile': {
            'params': [
                'qos-profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/wireless-controller/qos-profile/{qos-profile}',
                '/pm/config/global/obj/wireless-controller/qos-profile/{qos-profile}'
            ]
        },
        'vap': {
            'params': [
                'vap',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/wireless-controller/vap/{vap}',
                '/pm/config/global/obj/wireless-controller/vap/{vap}'
            ]
        },
        'vapgroup': {
            'params': [
                'vap-group',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/wireless-controller/vap-group/{vap-group}',
                '/pm/config/global/obj/wireless-controller/vap-group/{vap-group}'
            ]
        },
        'vap_dynamicmapping': {
            'params': [
                'vap',
                'dynamic_mapping',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/wireless-controller/vap/{vap}/dynamic_mapping/{dynamic_mapping}',
                '/pm/config/global/obj/wireless-controller/vap/{vap}/dynamic_mapping/{dynamic_mapping}'
            ]
        },
        'vap_macfilterlist': {
            'params': [
                'vap',
                'mac-filter-list',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/wireless-controller/vap/{vap}/mac-filter-list/{mac-filter-list}',
                '/pm/config/global/obj/wireless-controller/vap/{vap}/mac-filter-list/{mac-filter-list}'
            ]
        },
        'vap_mpskkey': {
            'params': [
                'vap',
                'mpsk-key',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/wireless-controller/vap/{vap}/mpsk-key/{mpsk-key}',
                '/pm/config/global/obj/wireless-controller/vap/{vap}/mpsk-key/{mpsk-key}'
            ]
        },
        'vap_portalmessageoverrides': {
            'params': [
                'vap',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/wireless-controller/vap/{vap}/portal-message-overrides',
                '/pm/config/global/obj/wireless-controller/vap/{vap}/portal-message-overrides'
            ]
        },
        'vap_vlanpool': {
            'params': [
                'vap',
                'vlan-pool',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/wireless-controller/vap/{vap}/vlan-pool/{vlan-pool}',
                '/pm/config/global/obj/wireless-controller/vap/{vap}/vlan-pool/{vlan-pool}'
            ]
        },
        'widsprofile': {
            'params': [
                'wids-profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/wireless-controller/wids-profile/{wids-profile}',
                '/pm/config/global/obj/wireless-controller/wids-profile/{wids-profile}'
            ]
        },
        'wtpprofile': {
            'params': [
                'wtp-profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/wireless-controller/wtp-profile/{wtp-profile}',
                '/pm/config/global/obj/wireless-controller/wtp-profile/{wtp-profile}'
            ]
        },
        'wtpprofile_denymaclist': {
            'params': [
                'wtp-profile',
                'deny-mac-list',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/wireless-controller/wtp-profile/{wtp-profile}/deny-mac-list/{deny-mac-list}',
                '/pm/config/global/obj/wireless-controller/wtp-profile/{wtp-profile}/deny-mac-list/{deny-mac-list}'
            ]
        },
        'wtpprofile_lan': {
            'params': [
                'wtp-profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/wireless-controller/wtp-profile/{wtp-profile}/lan',
                '/pm/config/global/obj/wireless-controller/wtp-profile/{wtp-profile}/lan'
            ]
        },
        'wtpprofile_lbs': {
            'params': [
                'wtp-profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/wireless-controller/wtp-profile/{wtp-profile}/lbs',
                '/pm/config/global/obj/wireless-controller/wtp-profile/{wtp-profile}/lbs'
            ]
        },
        'wtpprofile_platform': {
            'params': [
                'wtp-profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/wireless-controller/wtp-profile/{wtp-profile}/platform',
                '/pm/config/global/obj/wireless-controller/wtp-profile/{wtp-profile}/platform'
            ]
        },
        'wtpprofile_radio1': {
            'params': [
                'wtp-profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/wireless-controller/wtp-profile/{wtp-profile}/radio-1',
                '/pm/config/global/obj/wireless-controller/wtp-profile/{wtp-profile}/radio-1'
            ]
        },
        'wtpprofile_radio2': {
            'params': [
                'wtp-profile',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/wireless-controller/wtp-profile/{wtp-profile}/radio-2',
                '/pm/config/global/obj/wireless-controller/wtp-profile/{wtp-profile}/radio-2'
            ]
        },
        'wtpprofile_splittunnelingacl': {
            'params': [
                'wtp-profile',
                'split-tunneling-acl',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/wireless-controller/wtp-profile/{wtp-profile}/split-tunneling-acl/{split-tunneling-acl}',
                '/pm/config/global/obj/wireless-controller/wtp-profile/{wtp-profile}/split-tunneling-acl/{split-tunneling-acl}'
            ]
        },
        'dynamic_address': {
            'params': [
                'address',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/dynamic/address/{address}',
                '/pm/config/global/obj/dynamic/address/{address}'
            ]
        },
        'dynamic_address_dynamicaddrmapping': {
            'params': [
                'address',
                'dynamic_addr_mapping',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/dynamic/address/{address}/dynamic_addr_mapping/{dynamic_addr_mapping}',
                '/pm/config/global/obj/dynamic/address/{address}/dynamic_addr_mapping/{dynamic_addr_mapping}'
            ]
        },
        'dynamic_certificate_local': {
            'params': [
                'local',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/dynamic/certificate/local/{local}',
                '/pm/config/global/obj/dynamic/certificate/local/{local}'
            ]
        },
        'dynamic_certificate_local_dynamicmapping': {
            'params': [
                'local',
                'dynamic_mapping',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/dynamic/certificate/local/{local}/dynamic_mapping/{dynamic_mapping}',
                '/pm/config/global/obj/dynamic/certificate/local/{local}/dynamic_mapping/{dynamic_mapping}'
            ]
        },
        'dynamic_interface': {
            'params': [
                'interface',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/dynamic/interface/{interface}',
                '/pm/config/global/obj/dynamic/interface/{interface}'
            ]
        },
        'dynamic_interface_dynamicmapping': {
            'params': [
                'interface',
                'dynamic_mapping',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/dynamic/interface/{interface}/dynamic_mapping/{dynamic_mapping}',
                '/pm/config/global/obj/dynamic/interface/{interface}/dynamic_mapping/{dynamic_mapping}'
            ]
        },
        'dynamic_ippool': {
            'params': [
                'ippool',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/dynamic/ippool/{ippool}',
                '/pm/config/global/obj/dynamic/ippool/{ippool}'
            ]
        },
        'dynamic_multicast_interface': {
            'params': [
                'interface',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/dynamic/multicast/interface/{interface}',
                '/pm/config/global/obj/dynamic/multicast/interface/{interface}'
            ]
        },
        'dynamic_multicast_interface_dynamicmapping': {
            'params': [
                'interface',
                'dynamic_mapping',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/dynamic/multicast/interface/{interface}/dynamic_mapping/{dynamic_mapping}',
                '/pm/config/global/obj/dynamic/multicast/interface/{interface}/dynamic_mapping/{dynamic_mapping}'
            ]
        },
        'dynamic_vip': {
            'params': [
                'vip',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/dynamic/vip/{vip}',
                '/pm/config/global/obj/dynamic/vip/{vip}'
            ]
        },
        'dynamic_virtualwanlink_members': {
            'params': [
                'members',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/dynamic/virtual-wan-link/members/{members}',
                '/pm/config/global/obj/dynamic/virtual-wan-link/members/{members}'
            ]
        },
        'dynamic_virtualwanlink_members_dynamicmapping': {
            'params': [
                'members',
                'dynamic_mapping',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/dynamic/virtual-wan-link/members/{members}/dynamic_mapping/{dynamic_mapping}',
                '/pm/config/global/obj/dynamic/virtual-wan-link/members/{members}/dynamic_mapping/{dynamic_mapping}'
            ]
        },
        'dynamic_virtualwanlink_server': {
            'params': [
                'server',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/dynamic/virtual-wan-link/server/{server}',
                '/pm/config/global/obj/dynamic/virtual-wan-link/server/{server}'
            ]
        },
        'dynamic_virtualwanlink_server_dynamicmapping': {
            'params': [
                'server',
                'dynamic_mapping',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/dynamic/virtual-wan-link/server/{server}/dynamic_mapping/{dynamic_mapping}',
                '/pm/config/global/obj/dynamic/virtual-wan-link/server/{server}/dynamic_mapping/{dynamic_mapping}'
            ]
        },
        'dynamic_vpntunnel': {
            'params': [
                'vpntunnel',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/dynamic/vpntunnel/{vpntunnel}',
                '/pm/config/global/obj/dynamic/vpntunnel/{vpntunnel}'
            ]
        },
        'dynamic_vpntunnel_dynamicmapping': {
            'params': [
                'vpntunnel',
                'dynamic_mapping',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/dynamic/vpntunnel/{vpntunnel}/dynamic_mapping/{dynamic_mapping}',
                '/pm/config/global/obj/dynamic/vpntunnel/{vpntunnel}/dynamic_mapping/{dynamic_mapping}'
            ]
        },
        'dlp_filepattern': {
            'params': [
                'filepattern',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/dlp/filepattern/{filepattern}',
                '/pm/config/global/obj/dlp/filepattern/{filepattern}'
            ]
        },
        'dlp_filepattern_entries': {
            'params': [
                'filepattern',
                'entries',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/dlp/filepattern/{filepattern}/entries/{entries}',
                '/pm/config/global/obj/dlp/filepattern/{filepattern}/entries/{entries}'
            ]
        },
        'dlp_fpsensitivity': {
            'params': [
                'fp-sensitivity',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/dlp/fp-sensitivity/{fp-sensitivity}',
                '/pm/config/global/obj/dlp/fp-sensitivity/{fp-sensitivity}'
            ]
        },
        'dlp_sensor': {
            'params': [
                'sensor',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/dlp/sensor/{sensor}',
                '/pm/config/global/obj/dlp/sensor/{sensor}'
            ]
        },
        'dlp_sensor_filter': {
            'params': [
                'sensor',
                'filter',
                'adom'
            ],
            'urls': [
                '/pm/config/adom/{adom}/obj/dlp/sensor/{sensor}/filter/{filter}',
                '/pm/config/global/obj/dlp/sensor/{sensor}/filter/{filter}'
            ]
        },
        'system_backup_allsettings': {
            'params': [
            ],
            'urls': [
                '/cli/global/system/backup/all-settings'
            ]
        },
        'dvmdb_adom': {
            'params': [
                'adom'
            ],
            'urls': [
                '/dvmdb/adom/{adom}'
            ]
        },
        'system_ntp': {
            'params': [
            ],
            'urls': [
                '/cli/global/system/ntp'
            ]
        },
        'system_ntp_ntpserver': {
            'params': [
                'ntpserver'
            ],
            'urls': [
                '/cli/global/system/ntp/ntpserver/{ntpserver}'
            ]
        },
        'system_global': {
            'params': [
            ],
            'urls': [
                '/cli/global/system/global'
            ]
        },
        'fmupdate_fctservices': {
            'params': [
            ],
            'urls': [
                '/cli/global/fmupdate/fct-services'
            ]
        },
        'task_task': {
            'params': [
                'task'
            ],
            'urls': [
                '/task/task/{task}'
            ]
        },
        'task_task_history': {
            'params': [
                'task',
                'history'
            ],
            'urls': [
                '/task/task/{task}/history/{history}'
            ]
        },
        'task_task_line': {
            'params': [
                'task',
                'line'
            ],
            'urls': [
                '/task/task/{task}/line/{line}'
            ]
        },
        'system_mail': {
            'params': [
                'mail'
            ],
            'urls': [
                '/cli/global/system/mail/{mail}'
            ]
        },
        'system_interface': {
            'params': [
                'interface'
            ],
            'urls': [
                '/cli/global/system/interface/{interface}'
            ]
        },
        'system_interface_ipv6': {
            'params': [
                'interface'
            ],
            'urls': [
                '/cli/global/system/interface/{interface}/ipv6'
            ]
        },
        'dvmdb_workspace_dirty': {
            'params': [
                'adom'
            ],
            'urls': [
                '/dvmdb/adom/{adom}/workspace/dirty',
                '/dvmdb/global/workspace/dirty'
            ]
        },
        'dvmdb_workspace_dirty_dev': {
            'params': [
                'device_name',
                'adom'
            ],
            'urls': [
                '/dvmdb/adom/{adom}/workspace/dirty/dev/{device_name}'
            ]
        },
        'dvmdb_workspace_lockinfo': {
            'params': [
                'adom'
            ],
            'urls': [
                '/dvmdb/adom/{adom}/workspace/lockinfo',
                '/dvmdb/global/workspace/lockinfo'
            ]
        },
        'dvmdb_workspace_lockinfo_dev': {
            'params': [
                'device_name',
                'adom'
            ],
            'urls': [
                '/dvmdb/adom/{adom}/workspace/lockinfo/dev/{device_name}'
            ]
        },
        'dvmdb_workspace_lockinfo_obj': {
            'params': [
                'object_url_name',
                'adom'
            ],
            'urls': [
                '/dvmdb/adom/{adom}/workspace/lockinfo/obj/{object_url_name}',
                '/dvmdb/global/workspace/lockinfo/obj/{object_url_name}'
            ]
        },
        'dvmdb_workspace_lockinfo_pkg': {
            'params': [
                'package_path_name',
                'adom'
            ],
            'urls': [
                '/dvmdb/adom/{adom}/workspace/lockinfo/pkg/{package_path_name}',
                '/dvmdb/global/workspace/lockinfo/pkg/{package_path_name}'
            ]
        },
        'system_alertemail': {
            'params': [
            ],
            'urls': [
                '/cli/global/system/alertemail'
            ]
        }
    }

    module_arg_spec = {
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
        'facts': {
            'required': True,
            'type': 'dict',
            'options': {
                'selector': {
                    'required': True,
                    'type': 'str',
                    'choices': [
                        'dnsfilter_domainfilter',
                        'dnsfilter_domainfilter_entries',
                        'dnsfilter_profile',
                        'dnsfilter_profile_domainfilter',
                        'dnsfilter_profile_ftgddns',
                        'dnsfilter_profile_ftgddns_filters',
                        'webproxy_forwardserver',
                        'webproxy_forwardservergroup',
                        'webproxy_forwardservergroup_serverlist',
                        'webproxy_profile',
                        'webproxy_profile_headers',
                        'webproxy_wisp',
                        'log_customfield',
                        'fmupdate_customurllist',
                        'system_route6',
                        'voip_profile',
                        'voip_profile_sccp',
                        'voip_profile_sip',
                        'icap_profile',
                        'icap_server',
                        'fmupdate_service',
                        'fmupdate_serveraccesspriorities',
                        'fmupdate_serveraccesspriorities_privateserver',
                        'dvmdb_device',
                        'dvmdb_device_haslave',
                        'dvmdb_device_vdom',
                        'gtp_apn',
                        'gtp_apngrp',
                        'gtp_iewhitelist',
                        'gtp_iewhitelist_entries',
                        'gtp_messagefilterv0v1',
                        'gtp_messagefilterv2',
                        'gtp_tunnellimit',
                        'application_categories',
                        'application_custom',
                        'application_group',
                        'application_list',
                        'application_list_entries',
                        'application_list_entries_parameters',
                        'vpn_certificate_ca',
                        'vpn_certificate_ocspserver',
                        'vpn_certificate_remote',
                        'vpnsslweb_hostchecksoftware',
                        'vpnsslweb_hostchecksoftware_checkitemlist',
                        'vpnsslweb_portal',
                        'vpnsslweb_portal_bookmarkgroup',
                        'vpnsslweb_portal_bookmarkgroup_bookmarks',
                        'vpnsslweb_portal_bookmarkgroup_bookmarks_formdata',
                        'vpnsslweb_portal_macaddrcheckrule',
                        'vpnsslweb_portal_oschecklist',
                        'vpnsslweb_portal_splitdns',
                        'vpnsslweb_realm',
                        'pkg_firewall_centralsnatmap',
                        'pkg_firewall_dospolicy',
                        'pkg_firewall_dospolicy_anomaly',
                        'pkg_firewall_dospolicy6',
                        'pkg_firewall_dospolicy6_anomaly',
                        'pkg_firewall_interfacepolicy',
                        'pkg_firewall_interfacepolicy6',
                        'pkg_firewall_localinpolicy',
                        'pkg_firewall_localinpolicy6',
                        'pkg_firewall_multicastpolicy',
                        'pkg_firewall_multicastpolicy6',
                        'pkg_firewall_policy',
                        'pkg_firewall_policy_vpndstnode',
                        'pkg_firewall_policy_vpnsrcnode',
                        'pkg_firewall_policy46',
                        'pkg_firewall_policy6',
                        'pkg_firewall_policy64',
                        'pkg_firewall_proxypolicy',
                        'pkg_firewall_shapingpolicy',
                        'dvmdb_revision',
                        'system_ha',
                        'system_ha_peer',
                        'system_admin_group',
                        'system_admin_group_member',
                        'system_admin_ldap',
                        'system_admin_ldap_adom',
                        'system_admin_profile',
                        'system_admin_profile_datamaskcustomfields',
                        'system_admin_radius',
                        'system_admin_setting',
                        'system_admin_tacacs',
                        'system_admin_user',
                        'system_admin_user_adom',
                        'system_admin_user_adomexclude',
                        'system_admin_user_appfilter',
                        'system_admin_user_dashboard',
                        'system_admin_user_dashboardtabs',
                        'system_admin_user_ipsfilter',
                        'system_admin_user_metadata',
                        'system_admin_user_policypackage',
                        'system_admin_user_restrictdevvdom',
                        'system_admin_user_webfilter',
                        'system_workflow_approvalmatrix',
                        'system_workflow_approvalmatrix_approver',
                        'system_syslog',
                        'fmupdate_analyzer_virusreport',
                        'sys_ha_status',
                        'system_log_alert',
                        'system_log_ioc',
                        'system_log_maildomain',
                        'system_log_settings',
                        'system_log_settings_rollinganalyzer',
                        'system_log_settings_rollinglocal',
                        'system_log_settings_rollingregular',
                        'pkg_central_dnat',
                        'user_adgrp',
                        'user_device',
                        'user_devicecategory',
                        'user_devicegroup',
                        'user_devicegroup_dynamicmapping',
                        'user_devicegroup_tagging',
                        'user_device_dynamicmapping',
                        'user_device_tagging',
                        'user_fortitoken',
                        'user_fsso',
                        'user_fssopolling',
                        'user_fssopolling_adgrp',
                        'user_fsso_dynamicmapping',
                        'user_group',
                        'user_group_guest',
                        'user_group_match',
                        'user_ldap',
                        'user_ldap_dynamicmapping',
                        'user_local',
                        'user_passwordpolicy',
                        'user_peer',
                        'user_peergrp',
                        'user_pop3',
                        'user_pxgrid',
                        'user_radius',
                        'user_radius_accountingserver',
                        'user_radius_dynamicmapping',
                        'user_securityexemptlist',
                        'user_securityexemptlist_rule',
                        'user_tacacs',
                        'user_tacacs_dynamicmapping',
                        'system_snmp_community',
                        'system_snmp_community_hosts',
                        'system_snmp_community_hosts6',
                        'system_snmp_sysinfo',
                        'system_snmp_user',
                        'pm_devprof_adom',
                        'pm_devprof',
                        'system_route',
                        'system_connector',
                        'devprof_device_profile_fortianalyzer',
                        'devprof_device_profile_fortiguard',
                        'system_performance',
                        'system_dns',
                        'system_fortiview_autocache',
                        'system_fortiview_setting',
                        'pm_pkg_schedule',
                        'webfilter_categories',
                        'webfilter_content',
                        'webfilter_contentheader',
                        'webfilter_contentheader_entries',
                        'webfilter_content_entries',
                        'webfilter_ftgdlocalcat',
                        'webfilter_ftgdlocalrating',
                        'webfilter_profile',
                        'webfilter_profile_ftgdwf',
                        'webfilter_profile_ftgdwf_filters',
                        'webfilter_profile_ftgdwf_quota',
                        'webfilter_profile_override',
                        'webfilter_profile_urlextraction',
                        'webfilter_profile_web',
                        'webfilter_profile_youtubechannelfilter',
                        'webfilter_urlfilter',
                        'webfilter_urlfilter_entries',
                        'fmupdate_webspam_fgdsetting',
                        'fmupdate_webspam_fgdsetting_serveroverride',
                        'fmupdate_webspam_fgdsetting_serveroverride_servlist',
                        'fmupdate_webspam_webproxy',
                        'system_fips',
                        'fmupdate_avips_advancedlog',
                        'fmupdate_avips_webproxy',
                        'sys_status',
                        'wanopt_authgroup',
                        'wanopt_peer',
                        'wanopt_profile',
                        'wanopt_profile_cifs',
                        'wanopt_profile_ftp',
                        'wanopt_profile_http',
                        'wanopt_profile_mapi',
                        'wanopt_profile_tcp',
                        'ips_custom',
                        'ips_sensor',
                        'ips_sensor_entries',
                        'ips_sensor_entries_exemptip',
                        'ips_sensor_filter',
                        'ips_sensor_override',
                        'ips_sensor_override_exemptip',
                        'dvmdb_script',
                        'dvmdb_script_scriptschedule',
                        'dvmdb_script_log_latest',
                        'dvmdb_script_log_latest_device',
                        'dvmdb_script_log_list',
                        'dvmdb_script_log_list_device',
                        'dvmdb_script_log_output_device_logid',
                        'dvmdb_script_log_output_logid',
                        'dvmdb_script_log_summary',
                        'dvmdb_script_log_summary_device',
                        'adom_options',
                        'dvmdb_workflow',
                        'dvmdb_workflow_wflog',
                        'system_alertevent',
                        'system_alertevent_alertdestination',
                        'fmupdate_diskquota',
                        'vpnmgr_node',
                        'vpnmgr_node_iprange',
                        'vpnmgr_node_ipv4excluderange',
                        'vpnmgr_node_protectedsubnet',
                        'vpnmgr_node_summaryaddr',
                        'vpnmgr_vpntable',
                        'system_metadata_admins',
                        'spamfilter_bwl',
                        'spamfilter_bwl_entries',
                        'spamfilter_bword',
                        'spamfilter_bword_entries',
                        'spamfilter_dnsbl',
                        'spamfilter_dnsbl_entries',
                        'spamfilter_iptrust',
                        'spamfilter_iptrust_entries',
                        'spamfilter_mheader',
                        'spamfilter_mheader_entries',
                        'spamfilter_profile',
                        'spamfilter_profile_gmail',
                        'spamfilter_profile_imap',
                        'spamfilter_profile_mapi',
                        'spamfilter_profile_msnhotmail',
                        'spamfilter_profile_pop3',
                        'spamfilter_profile_smtp',
                        'spamfilter_profile_yahoomail',
                        'fmupdate_multilayer',
                        'dvmdb_metafields_adom',
                        'dvmdb_metafields_device',
                        'dvmdb_metafields_group',
                        'system_guiact',
                        'antivirus_mmschecksum',
                        'antivirus_mmschecksum_entries',
                        'antivirus_notification',
                        'antivirus_notification_entries',
                        'antivirus_profile',
                        'antivirus_profile_contentdisarm',
                        'antivirus_profile_ftp',
                        'antivirus_profile_http',
                        'antivirus_profile_imap',
                        'antivirus_profile_mapi',
                        'antivirus_profile_nacquar',
                        'antivirus_profile_nntp',
                        'antivirus_profile_pop3',
                        'antivirus_profile_smb',
                        'antivirus_profile_smtp',
                        'switchcontroller_lldpprofile',
                        'switchcontroller_lldpprofile_customtlvs',
                        'switchcontroller_lldpprofile_mednetworkpolicy',
                        'switchcontroller_managedswitch',
                        'switchcontroller_managedswitch_ports',
                        'switchcontroller_qos_dot1pmap',
                        'switchcontroller_qos_ipdscpmap',
                        'switchcontroller_qos_ipdscpmap_map',
                        'switchcontroller_qos_qospolicy',
                        'switchcontroller_qos_queuepolicy',
                        'switchcontroller_qos_queuepolicy_cosqueue',
                        'switchcontroller_securitypolicy_8021x',
                        'switchcontroller_securitypolicy_captiveportal',
                        'switchcontroller_managedswitch_8021xsettings',
                        'switchcontroller_managedswitch_customcommand',
                        'switchcontroller_managedswitch_igmpsnooping',
                        'switchcontroller_managedswitch_mirror',
                        'switchcontroller_managedswitch_stormcontrol',
                        'switchcontroller_managedswitch_stpsettings',
                        'switchcontroller_managedswitch_switchlog',
                        'switchcontroller_managedswitch_switchstpsettings',
                        'system_status',
                        'devprof_log_fortianalyzer_setting',
                        'devprof_log_syslogd_filter',
                        'devprof_log_syslogd_setting',
                        'system_certificate_ca',
                        'system_certificate_crl',
                        'system_certificate_local',
                        'system_certificate_oftp',
                        'system_certificate_remote',
                        'system_certificate_ssh',
                        'firewall_address',
                        'firewall_address_dynamicmapping',
                        'firewall_address_list',
                        'firewall_address_tagging',
                        'firewall_address6',
                        'firewall_address6template',
                        'firewall_address6template_subnetsegment',
                        'firewall_address6template_subnetsegment_values',
                        'firewall_address6_dynamicmapping',
                        'firewall_address6_list',
                        'firewall_address6_subnetsegment',
                        'firewall_address6_tagging',
                        'firewall_addrgrp',
                        'firewall_addrgrp_dynamicmapping',
                        'firewall_addrgrp_tagging',
                        'firewall_addrgrp6',
                        'firewall_addrgrp6_dynamicmapping',
                        'firewall_addrgrp6_tagging',
                        'firewall_carrierendpointbwl',
                        'firewall_carrierendpointbwl_entries',
                        'firewall_gtp',
                        'firewall_gtp_apn',
                        'firewall_gtp_ieremovepolicy',
                        'firewall_gtp_ievalidation',
                        'firewall_gtp_imsi',
                        'firewall_gtp_ippolicy',
                        'firewall_gtp_messageratelimit',
                        'firewall_gtp_messageratelimitv0',
                        'firewall_gtp_messageratelimitv1',
                        'firewall_gtp_messageratelimitv2',
                        'firewall_gtp_noippolicy',
                        'firewall_gtp_perapnshaper',
                        'firewall_gtp_policy',
                        'firewall_identitybasedroute',
                        'firewall_identitybasedroute_rule',
                        'firewall_internetservice',
                        'firewall_internetservicecustom',
                        'firewall_internetservicecustomgroup',
                        'firewall_internetservicecustom_disableentry',
                        'firewall_internetservicecustom_disableentry_iprange',
                        'firewall_internetservicecustom_entry',
                        'firewall_internetservicecustom_entry_portrange',
                        'firewall_internetservicegroup',
                        'firewall_internetservice_entry',
                        'firewall_ippool',
                        'firewall_ippool_dynamicmapping',
                        'firewall_ippool6',
                        'firewall_ippool6_dynamicmapping',
                        'firewall_ldbmonitor',
                        'firewall_mmsprofile',
                        'firewall_mmsprofile_dupe',
                        'firewall_mmsprofile_flood',
                        'firewall_mmsprofile_notifmsisdn',
                        'firewall_mmsprofile_notification',
                        'firewall_multicastaddress',
                        'firewall_multicastaddress_tagging',
                        'firewall_multicastaddress6',
                        'firewall_multicastaddress6_tagging',
                        'firewall_profilegroup',
                        'firewall_profileprotocoloptions',
                        'firewall_profileprotocoloptions_dns',
                        'firewall_profileprotocoloptions_ftp',
                        'firewall_profileprotocoloptions_http',
                        'firewall_profileprotocoloptions_imap',
                        'firewall_profileprotocoloptions_mailsignature',
                        'firewall_profileprotocoloptions_mapi',
                        'firewall_profileprotocoloptions_nntp',
                        'firewall_profileprotocoloptions_pop3',
                        'firewall_profileprotocoloptions_smtp',
                        'firewall_proxyaddress',
                        'firewall_proxyaddress_headergroup',
                        'firewall_proxyaddress_tagging',
                        'firewall_proxyaddrgrp',
                        'firewall_proxyaddrgrp_tagging',
                        'firewall_schedule_group',
                        'firewall_schedule_onetime',
                        'firewall_schedule_recurring',
                        'firewall_service_category',
                        'firewall_service_custom',
                        'firewall_service_group',
                        'firewall_shaper_peripshaper',
                        'firewall_shaper_trafficshaper',
                        'firewall_shapingprofile',
                        'firewall_shapingprofile_shapingentries',
                        'firewall_sslsshprofile',
                        'firewall_sslsshprofile_ftps',
                        'firewall_sslsshprofile_https',
                        'firewall_sslsshprofile_imaps',
                        'firewall_sslsshprofile_pop3s',
                        'firewall_sslsshprofile_smtps',
                        'firewall_sslsshprofile_ssh',
                        'firewall_sslsshprofile_ssl',
                        'firewall_sslsshprofile_sslexempt',
                        'firewall_sslsshprofile_sslserver',
                        'firewall_vip',
                        'firewall_vip_dynamicmapping',
                        'firewall_vip_dynamicmapping_realservers',
                        'firewall_vip_dynamicmapping_sslciphersuites',
                        'firewall_vip_realservers',
                        'firewall_vip_sslciphersuites',
                        'firewall_vip_sslserverciphersuites',
                        'firewall_vip46',
                        'firewall_vip46_dynamicmapping',
                        'firewall_vip46_realservers',
                        'firewall_vip6',
                        'firewall_vip6_dynamicmapping',
                        'firewall_vip6_realservers',
                        'firewall_vip6_sslciphersuites',
                        'firewall_vip6_sslserverciphersuites',
                        'firewall_vip64',
                        'firewall_vip64_dynamicmapping',
                        'firewall_vip64_realservers',
                        'firewall_vipgrp',
                        'firewall_vipgrp_dynamicmapping',
                        'firewall_vipgrp46',
                        'firewall_vipgrp6',
                        'firewall_vipgrp64',
                        'firewall_wildcardfqdn_custom',
                        'firewall_wildcardfqdn_group',
                        'system_alertconsole',
                        'fmupdate_publicnetwork',
                        'metafields_system_admin_user',
                        'system_logfetch_clientprofile',
                        'system_logfetch_clientprofile_devicefilter',
                        'system_logfetch_clientprofile_logfilter',
                        'system_logfetch_serversettings',
                        'footer_consolidated_policy',
                        'footer_policy',
                        'footer_policy_identitybasedpolicy',
                        'footer_policy6',
                        'footer_policy6_identitybasedpolicy6',
                        'footer_shapingpolicy',
                        'header_consolidated_policy',
                        'header_policy',
                        'header_policy_identitybasedpolicy',
                        'header_policy6',
                        'header_policy6_identitybasedpolicy6',
                        'header_shapingpolicy',
                        'pkg_footer_consolidated_policy',
                        'pkg_footer_policy',
                        'pkg_footer_policy_identitybasedpolicy',
                        'pkg_footer_policy6',
                        'pkg_footer_policy6_identitybasedpolicy6',
                        'pkg_footer_shapingpolicy',
                        'pkg_header_consolidated_policy',
                        'pkg_header_policy',
                        'pkg_header_policy_identitybasedpolicy',
                        'pkg_header_policy6',
                        'pkg_header_policy6_identitybasedpolicy6',
                        'pkg_header_shapingpolicy',
                        'system_report_autocache',
                        'system_report_estbrowsetime',
                        'system_report_group',
                        'system_report_group_chartalternative',
                        'system_report_group_groupby',
                        'system_report_setting',
                        'waf_mainclass',
                        'waf_profile',
                        'waf_profile_addresslist',
                        'waf_profile_constraint',
                        'waf_profile_constraint_contentlength',
                        'waf_profile_constraint_exception',
                        'waf_profile_constraint_headerlength',
                        'waf_profile_constraint_hostname',
                        'waf_profile_constraint_linelength',
                        'waf_profile_constraint_malformed',
                        'waf_profile_constraint_maxcookie',
                        'waf_profile_constraint_maxheaderline',
                        'waf_profile_constraint_maxrangesegment',
                        'waf_profile_constraint_maxurlparam',
                        'waf_profile_constraint_method',
                        'waf_profile_constraint_paramlength',
                        'waf_profile_constraint_urlparamlength',
                        'waf_profile_constraint_version',
                        'waf_profile_method',
                        'waf_profile_method_methodpolicy',
                        'waf_profile_signature',
                        'waf_profile_signature_customsignature',
                        'waf_profile_signature_mainclass',
                        'waf_profile_urlaccess',
                        'waf_profile_urlaccess_accesspattern',
                        'waf_signature',
                        'waf_subclass',
                        'certificate_template',
                        'system_customlanguage',
                        'system_dhcp_server',
                        'system_dhcp_server_excluderange',
                        'system_dhcp_server_iprange',
                        'system_dhcp_server_options',
                        'system_dhcp_server_reservedaddress',
                        'system_externalresource',
                        'system_fortiguard',
                        'system_geoipcountry',
                        'system_geoipoverride',
                        'system_geoipoverride_iprange',
                        'system_meta',
                        'system_meta_sysmetafields',
                        'system_objecttagging',
                        'system_replacemsggroup',
                        'system_replacemsggroup_admin',
                        'system_replacemsggroup_alertmail',
                        'system_replacemsggroup_auth',
                        'system_replacemsggroup_custommessage',
                        'system_replacemsggroup_devicedetectionportal',
                        'system_replacemsggroup_ec',
                        'system_replacemsggroup_fortiguardwf',
                        'system_replacemsggroup_ftp',
                        'system_replacemsggroup_http',
                        'system_replacemsggroup_icap',
                        'system_replacemsggroup_mail',
                        'system_replacemsggroup_mm1',
                        'system_replacemsggroup_mm3',
                        'system_replacemsggroup_mm4',
                        'system_replacemsggroup_mm7',
                        'system_replacemsggroup_mms',
                        'system_replacemsggroup_nacquar',
                        'system_replacemsggroup_nntp',
                        'system_replacemsggroup_spam',
                        'system_replacemsggroup_sslvpn',
                        'system_replacemsggroup_trafficquota',
                        'system_replacemsggroup_utm',
                        'system_replacemsggroup_webproxy',
                        'system_replacemsgimage',
                        'system_sdnconnector',
                        'system_sdnconnector_externalip',
                        'system_sdnconnector_nic',
                        'system_sdnconnector_nic_ip',
                        'system_sdnconnector_route',
                        'system_sdnconnector_routetable',
                        'system_sdnconnector_routetable_route',
                        'system_smsserver',
                        'system_virtualwirepair',
                        'template',
                        'templategroup',
                        'dvmdb_group',
                        'wanprof_system_virtualwanlink',
                        'wanprof_system_virtualwanlink_healthcheck',
                        'wanprof_system_virtualwanlink_healthcheck_sla',
                        'wanprof_system_virtualwanlink_members',
                        'wanprof_system_virtualwanlink_service',
                        'wanprof_system_virtualwanlink_service_sla',
                        'sshfilter_profile',
                        'sshfilter_profile_shellcommands',
                        'system_dm',
                        'fsp_vlan',
                        'fsp_vlan_dhcpserver',
                        'fsp_vlan_dhcpserver_excluderange',
                        'fsp_vlan_dhcpserver_iprange',
                        'fsp_vlan_dhcpserver_options',
                        'fsp_vlan_dhcpserver_reservedaddress',
                        'fsp_vlan_dynamicmapping',
                        'fsp_vlan_dynamicmapping_dhcpserver',
                        'fsp_vlan_dynamicmapping_dhcpserver_excluderange',
                        'fsp_vlan_dynamicmapping_dhcpserver_iprange',
                        'fsp_vlan_dynamicmapping_dhcpserver_options',
                        'fsp_vlan_dynamicmapping_dhcpserver_reservedaddress',
                        'fsp_vlan_dynamicmapping_interface',
                        'fsp_vlan_interface',
                        'fsp_vlan_interface_ipv6',
                        'fsp_vlan_interface_secondaryip',
                        'fsp_vlan_interface_vrrp',
                        'system_sql',
                        'system_sql_customindex',
                        'system_sql_tsindexfield',
                        'system_passwordpolicy',
                        'pm_wanprof_adom',
                        'pm_wanprof',
                        'fmupdate_fdssetting',
                        'fmupdate_fdssetting_pushoverride',
                        'fmupdate_fdssetting_pushoverridetoclient',
                        'fmupdate_fdssetting_pushoverridetoclient_announceip',
                        'fmupdate_fdssetting_serveroverride',
                        'fmupdate_fdssetting_serveroverride_servlist',
                        'fmupdate_fdssetting_updateschedule',
                        'fmupdate_serveroverridestatus',
                        'pm_pkg_adom',
                        'pm_pkg',
                        'pm_pkg_global',
                        'system_autodelete',
                        'system_autodelete_dlpfilesautodeletion',
                        'system_autodelete_logautodeletion',
                        'system_autodelete_quarantinefilesautodeletion',
                        'system_autodelete_reportautodeletion',
                        'devprof_system_centralmanagement',
                        'devprof_system_centralmanagement_serverlist',
                        'devprof_system_dns',
                        'devprof_system_emailserver',
                        'devprof_system_global',
                        'devprof_system_ntp',
                        'devprof_system_ntp_ntpserver',
                        'devprof_system_replacemsg_admin',
                        'devprof_system_replacemsg_alertmail',
                        'devprof_system_replacemsg_auth',
                        'devprof_system_replacemsg_devicedetectionportal',
                        'devprof_system_replacemsg_ec',
                        'devprof_system_replacemsg_fortiguardwf',
                        'devprof_system_replacemsg_ftp',
                        'devprof_system_replacemsg_http',
                        'devprof_system_replacemsg_mail',
                        'devprof_system_replacemsg_mms',
                        'devprof_system_replacemsg_nacquar',
                        'devprof_system_replacemsg_nntp',
                        'devprof_system_replacemsg_spam',
                        'devprof_system_replacemsg_sslvpn',
                        'devprof_system_replacemsg_trafficquota',
                        'devprof_system_replacemsg_utm',
                        'devprof_system_replacemsg_webproxy',
                        'devprof_system_snmp_community',
                        'devprof_system_snmp_community_hosts',
                        'devprof_system_snmp_community_hosts6',
                        'devprof_system_snmp_sysinfo',
                        'devprof_system_snmp_user',
                        'system_locallog_disk_filter',
                        'system_locallog_disk_setting',
                        'system_locallog_fortianalyzer_filter',
                        'system_locallog_fortianalyzer_setting',
                        'system_locallog_fortianalyzer2_filter',
                        'system_locallog_fortianalyzer2_setting',
                        'system_locallog_fortianalyzer3_filter',
                        'system_locallog_fortianalyzer3_setting',
                        'system_locallog_memory_filter',
                        'system_locallog_memory_setting',
                        'system_locallog_setting',
                        'system_locallog_syslogd_filter',
                        'system_locallog_syslogd_setting',
                        'system_locallog_syslogd2_filter',
                        'system_locallog_syslogd2_setting',
                        'system_locallog_syslogd3_filter',
                        'system_locallog_syslogd3_setting',
                        'system_saml',
                        'system_saml_serviceproviders',
                        'bleprofile',
                        'bonjourprofile',
                        'bonjourprofile_policylist',
                        'hotspot20_anqp3gppcellular',
                        'hotspot20_anqp3gppcellular_mccmnclist',
                        'hotspot20_anqpipaddresstype',
                        'hotspot20_anqpnairealm',
                        'hotspot20_anqpnairealm_nailist',
                        'hotspot20_anqpnairealm_nailist_eapmethod',
                        'hotspot20_anqpnairealm_nailist_eapmethod_authparam',
                        'hotspot20_anqpnetworkauthtype',
                        'hotspot20_anqproamingconsortium',
                        'hotspot20_anqproamingconsortium_oilist',
                        'hotspot20_anqpvenuename',
                        'hotspot20_anqpvenuename_valuelist',
                        'hotspot20_h2qpconncapability',
                        'hotspot20_h2qpoperatorname',
                        'hotspot20_h2qpoperatorname_valuelist',
                        'hotspot20_h2qposuprovider',
                        'hotspot20_h2qposuprovider_friendlyname',
                        'hotspot20_h2qposuprovider_servicedescription',
                        'hotspot20_h2qpwanmetric',
                        'hotspot20_hsprofile',
                        'hotspot20_qosmap',
                        'hotspot20_qosmap_dscpexcept',
                        'hotspot20_qosmap_dscprange',
                        'qosprofile',
                        'vap',
                        'vapgroup',
                        'vap_dynamicmapping',
                        'vap_macfilterlist',
                        'vap_mpskkey',
                        'vap_portalmessageoverrides',
                        'vap_vlanpool',
                        'widsprofile',
                        'wtpprofile',
                        'wtpprofile_denymaclist',
                        'wtpprofile_lan',
                        'wtpprofile_lbs',
                        'wtpprofile_platform',
                        'wtpprofile_radio1',
                        'wtpprofile_radio2',
                        'wtpprofile_splittunnelingacl',
                        'dynamic_address',
                        'dynamic_address_dynamicaddrmapping',
                        'dynamic_certificate_local',
                        'dynamic_certificate_local_dynamicmapping',
                        'dynamic_interface',
                        'dynamic_interface_dynamicmapping',
                        'dynamic_ippool',
                        'dynamic_multicast_interface',
                        'dynamic_multicast_interface_dynamicmapping',
                        'dynamic_vip',
                        'dynamic_virtualwanlink_members',
                        'dynamic_virtualwanlink_members_dynamicmapping',
                        'dynamic_virtualwanlink_server',
                        'dynamic_virtualwanlink_server_dynamicmapping',
                        'dynamic_vpntunnel',
                        'dynamic_vpntunnel_dynamicmapping',
                        'dlp_filepattern',
                        'dlp_filepattern_entries',
                        'dlp_fpsensitivity',
                        'dlp_sensor',
                        'dlp_sensor_filter',
                        'system_backup_allsettings',
                        'dvmdb_adom',
                        'system_ntp',
                        'system_ntp_ntpserver',
                        'system_global',
                        'fmupdate_fctservices',
                        'task_task',
                        'task_task_history',
                        'task_task_line',
                        'system_mail',
                        'system_interface',
                        'system_interface_ipv6',
                        'dvmdb_workspace_dirty',
                        'dvmdb_workspace_dirty_dev',
                        'dvmdb_workspace_lockinfo',
                        'dvmdb_workspace_lockinfo_dev',
                        'dvmdb_workspace_lockinfo_obj',
                        'dvmdb_workspace_lockinfo_pkg',
                        'system_alertemail'
                    ]
                },
                'params': {
                    'required': False,
                    'type': 'dict'
                },
                'filter': {
                    'required': False,
                    'type': 'list'
                },
                'sortings': {
                    'required': False,
                    'type': 'list'
                },
                'fields': {
                    'required': False,
                    'type': 'list'
                },
                'option': {
                    'required': False,
                    'type': 'list'
                }
            }
        }
    }
    module = AnsibleModule(argument_spec=module_arg_spec,
                           supports_check_mode=False)
    fmgr = None
    if module._socket_path:
        connection = Connection(module._socket_path)
        fmgr = NAPIManager(None, None, None, None, module, connection)
        fmgr.process_fact(facts_metadata)
    else:
        module.fail_json(msg='MUST RUN IN HTTPAPI MODE')
    module.exit_json(meta=module.params)


if __name__ == '__main__':
    main()
