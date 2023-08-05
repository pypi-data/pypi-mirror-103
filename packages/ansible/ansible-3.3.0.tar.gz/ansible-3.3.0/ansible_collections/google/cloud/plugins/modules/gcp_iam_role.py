#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2017 Google
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# ----------------------------------------------------------------------------
#
#     ***     AUTO GENERATED CODE    ***    AUTO GENERATED CODE     ***
#
# ----------------------------------------------------------------------------
#
#     This file is automatically generated by Magic Modules and manual
#     changes will be clobbered when the file is regenerated.
#
#     Please read more about how to change this file at
#     https://www.github.com/GoogleCloudPlatform/magic-modules
#
# ----------------------------------------------------------------------------

from __future__ import absolute_import, division, print_function

__metaclass__ = type

################################################################################
# Documentation
################################################################################

ANSIBLE_METADATA = {'metadata_version': '1.1', 'status': ["preview"], 'supported_by': 'community'}

DOCUMENTATION = '''
---
module: gcp_iam_role
description:
- A role in the Identity and Access Management API .
short_description: Creates a GCP Role
author: Google Inc. (@googlecloudplatform)
requirements:
- python >= 2.6
- requests >= 2.18.4
- google-auth >= 1.3.0
options:
  state:
    description:
    - Whether the given object should exist in GCP
    choices:
    - present
    - absent
    default: present
    type: str
  name:
    description:
    - The name of the role.
    required: true
    type: str
  title:
    description:
    - A human-readable title for the role. Typically this is limited to 100 UTF-8
      bytes.
    required: false
    type: str
  description:
    description:
    - Human-readable description for the role.
    required: false
    type: str
  included_permissions:
    description:
    - Names of permissions this role grants when bound in an IAM policy.
    elements: str
    required: false
    type: list
  stage:
    description:
    - The current launch stage of the role.
    - 'Some valid choices include: "ALPHA", "BETA", "GA", "DEPRECATED", "DISABLED",
      "EAP"'
    required: false
    type: str
  project:
    description:
    - The Google Cloud Platform project to use.
    type: str
  auth_kind:
    description:
    - The type of credential used.
    type: str
    required: true
    choices:
    - application
    - machineaccount
    - serviceaccount
  service_account_contents:
    description:
    - The contents of a Service Account JSON file, either in a dictionary or as a
      JSON string that represents it.
    type: jsonarg
  service_account_file:
    description:
    - The path of a Service Account JSON file if serviceaccount is selected as type.
    type: path
  service_account_email:
    description:
    - An optional service account email address if machineaccount is selected and
      the user does not wish to use the default email.
    type: str
  scopes:
    description:
    - Array of scopes to be used
    type: list
    elements: str
  env_type:
    description:
    - Specifies which Ansible environment you're running this module within.
    - This should not be set unless you know what you're doing.
    - This only alters the User Agent string for any API requests.
    type: str
'''

EXAMPLES = '''
- name: create a role
  google.cloud.gcp_iam_role:
    name: myCustomRole2
    title: My Custom Role
    description: My custom role description
    included_permissions:
    - iam.roles.list
    - iam.roles.create
    - iam.roles.delete
    project: test_project
    auth_kind: serviceaccount
    service_account_file: "/tmp/auth.pem"
    state: present
'''

RETURN = '''
name:
  description:
  - The name of the role.
  returned: success
  type: str
title:
  description:
  - A human-readable title for the role. Typically this is limited to 100 UTF-8 bytes.
  returned: success
  type: str
description:
  description:
  - Human-readable description for the role.
  returned: success
  type: str
includedPermissions:
  description:
  - Names of permissions this role grants when bound in an IAM policy.
  returned: success
  type: list
stage:
  description:
  - The current launch stage of the role.
  returned: success
  type: str
deleted:
  description:
  - The current deleted state of the role.
  returned: success
  type: bool
'''

################################################################################
# Imports
################################################################################

from ansible_collections.google.cloud.plugins.module_utils.gcp_utils import navigate_hash, GcpSession, GcpModule, GcpRequest, replace_resource_dict
import json

################################################################################
# Main
################################################################################


def main():
    """Main function"""

    module = GcpModule(
        argument_spec=dict(
            state=dict(default='present', choices=['present', 'absent'], type='str'),
            name=dict(required=True, type='str'),
            title=dict(type='str'),
            description=dict(type='str'),
            included_permissions=dict(type='list', elements='str'),
            stage=dict(type='str'),
        )
    )

    if not module.params['scopes']:
        module.params['scopes'] = ['https://www.googleapis.com/auth/iam']

    state = module.params['state']

    fetch = fetch_resource(module, self_link(module))
    changed = False

    if fetch:
        if state == 'present':
            if is_different(module, fetch):
                update(module, self_link(module), fetch)
                fetch = fetch_resource(module, self_link(module))
                changed = True
        else:
            delete(module, self_link(module))
            fetch = {}
            changed = True
    else:
        if state == 'present':
            fetch = create(module, collection(module))
            changed = True
        else:
            fetch = {}

    fetch.update({'changed': changed})

    module.exit_json(**fetch)


def create(module, link):
    auth = GcpSession(module, 'iam')
    return return_if_object(module, auth.post(link, resource_to_create(module)))


def update(module, link, fetch):
    auth = GcpSession(module, 'iam')
    params = {'updateMask': updateMask(resource_to_request(module), response_to_hash(module, fetch))}
    request = resource_to_request(module)
    del request['name']
    return return_if_object(module, auth.put(link, request, params=params))


def updateMask(request, response):
    update_mask = []
    if request.get('name') != response.get('name'):
        update_mask.append('name')
    if request.get('title') != response.get('title'):
        update_mask.append('title')
    if request.get('description') != response.get('description'):
        update_mask.append('description')
    if request.get('includedPermissions') != response.get('includedPermissions'):
        update_mask.append('includedPermissions')
    if request.get('stage') != response.get('stage'):
        update_mask.append('stage')
    return ','.join(update_mask)


def delete(module, link):
    auth = GcpSession(module, 'iam')
    return return_if_object(module, auth.delete(link))


def resource_to_request(module):
    request = {
        u'name': module.params.get('name'),
        u'title': module.params.get('title'),
        u'description': module.params.get('description'),
        u'includedPermissions': module.params.get('included_permissions'),
        u'stage': module.params.get('stage'),
    }
    return_vals = {}
    for k, v in request.items():
        if v or v is False:
            return_vals[k] = v

    return return_vals


def fetch_resource(module, link, allow_not_found=True):
    auth = GcpSession(module, 'iam')
    return return_if_object(module, auth.get(link), allow_not_found)


def self_link(module):
    return "https://iam.googleapis.com/v1/projects/{project}/roles/{name}".format(**module.params)


def collection(module):
    return "https://iam.googleapis.com/v1/projects/{project}/roles".format(**module.params)


def return_if_object(module, response, allow_not_found=False):
    # If not found, return nothing.
    if allow_not_found and response.status_code == 404:
        return None

    # If no content, return nothing.
    if response.status_code == 204:
        return None

    try:
        module.raise_for_status(response)
        result = response.json()
    except getattr(json.decoder, 'JSONDecodeError', ValueError):
        module.fail_json(msg="Invalid JSON response with error: %s" % response.text)

    result = decode_response(result, module)

    if navigate_hash(result, ['error', 'errors']):
        module.fail_json(msg=navigate_hash(result, ['error', 'errors']))

    return result


def is_different(module, response):
    request = resource_to_request(module)
    response = response_to_hash(module, response)
    request = decode_response(request, module)

    # Remove all output-only from response.
    response_vals = {}
    for k, v in response.items():
        if k in request:
            response_vals[k] = v

    request_vals = {}
    for k, v in request.items():
        if k in response:
            request_vals[k] = v

    return GcpRequest(request_vals) != GcpRequest(response_vals)


# Remove unnecessary properties from the response.
# This is for doing comparisons with Ansible's current parameters.
def response_to_hash(module, response):
    return {
        u'name': response.get(u'name'),
        u'title': response.get(u'title'),
        u'description': response.get(u'description'),
        u'includedPermissions': response.get(u'includedPermissions'),
        u'stage': response.get(u'stage'),
        u'deleted': response.get(u'deleted'),
    }


def resource_to_create(module):
    role = resource_to_request(module)
    del role['name']
    return {'roleId': module.params['name'], 'role': role}


def decode_response(response, module):
    if 'name' in response:
        response['name'] = response['name'].split('/')[-1]
    return response


if __name__ == '__main__':
    main()
