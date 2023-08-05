# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


class ModuleDocFragment(object):
    # Parameters for Service Now modules
    DOCUMENTATION = r'''
options:
    instance:
      description:
      - The ServiceNow instance name, without the domain, service-now.com.
      - If the value is not specified in the task, the value of environment variable C(SN_INSTANCE) will be used instead.
      required: false
      type: str
    host:
      description:
      - The ServiceNow hostname.
      - This value is FQDN for ServiceNow host.
      - If the value is not specified in the task, the value of environment variable C(SN_HOST) will be used instead.
      - Mutually exclusive with C(instance).
      type: str
    username:
      description:
      - Name of user for connection to ServiceNow.
      - Required whether using Basic or OAuth authentication.
      - If the value is not specified in the task, the value of environment variable C(SN_USERNAME) will be used instead.
      required: false
      type: str
    password:
      description:
      - Password for username.
      - Required whether using Basic or OAuth authentication.
      - If the value is not specified in the task, the value of environment variable C(SN_PASSWORD) will be used instead.
      required: false
      type: str
    client_id:
      description:
      - Client ID generated by ServiceNow.
      required: false
      type: str
    client_secret:
      description:
      - Client Secret associated with client id.
      required: false
      type: str
'''
