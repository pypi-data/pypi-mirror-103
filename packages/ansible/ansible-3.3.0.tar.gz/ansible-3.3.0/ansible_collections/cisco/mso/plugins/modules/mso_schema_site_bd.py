#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2019, Dag Wieers (@dagwieers) <dag@wieers.com>
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: mso_schema_site_bd
short_description: Manage site-local Bridge Domains (BDs) in schema template
description:
- Manage site-local BDs in schema template on Cisco ACI Multi-Site.
author:
- Dag Wieers (@dagwieers)
options:
  schema:
    description:
    - The name of the schema.
    type: str
    required: yes
  site:
    description:
    - The name of the site.
    type: str
    required: yes
  template:
    description:
    - The name of the template.
    type: str
    required: yes
  bd:
    description:
    - The name of the BD to manage.
    type: str
    aliases: [ name ]
  host_route:
    description:
    - Whether host-based routing is enabled.
    type: bool
  svi_mac:
    description:
    - SVI MAC Address
    type: str
  state:
    description:
    - Use C(present) or C(absent) for adding or removing.
    - Use C(query) for listing an object or multiple objects.
    type: str
    choices: [ absent, present, query ]
    default: present
seealso:
- module: cisco.mso.mso_schema_site
- module: cisco.mso.mso_schema_site_bd_l3out
- module: cisco.mso.mso_schema_site_bd_subnet
- module: cisco.mso.mso_schema_template_bd
extends_documentation_fragment: cisco.mso.modules
'''

EXAMPLES = r'''
- name: Add a new site BD
  cisco.mso.mso_schema_site_bd:
    host: mso_host
    username: admin
    password: SomeSecretPassword
    schema: Schema1
    site: Site1
    template: Template1
    bd: BD1
    state: present
  delegate_to: localhost

- name: Remove a site BD
  cisco.mso.mso_schema_site_bd:
    host: mso_host
    username: admin
    password: SomeSecretPassword
    schema: Schema1
    site: Site1
    template: Template1
    bd: BD1
    state: absent
  delegate_to: localhost

- name: Query a specific site BD
  cisco.mso.mso_schema_site_bd:
    host: mso_host
    username: admin
    password: SomeSecretPassword
    schema: Schema1
    site: Site1
    template: Template1
    bd: BD1
    state: query
  delegate_to: localhost
  register: query_result

- name: Query all site BDs
  cisco.mso.mso_schema_site_bd:
    host: mso_host
    username: admin
    password: SomeSecretPassword
    schema: Schema1
    site: Site1
    template: Template1
    state: query
  delegate_to: localhost
  register: query_result
'''

RETURN = r'''
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.mso.plugins.module_utils.mso import MSOModule, mso_argument_spec


def main():
    argument_spec = mso_argument_spec()
    argument_spec.update(
        schema=dict(type='str', required=True),
        site=dict(type='str', required=True),
        template=dict(type='str', required=True),
        bd=dict(type='str', aliases=['name']),  # This parameter is not required for querying all objects
        host_route=dict(type='bool'),
        svi_mac=dict(type='str'),
        state=dict(type='str', default='present', choices=['absent', 'present', 'query']),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_if=[
            ['state', 'absent', ['bd']],
            ['state', 'present', ['bd']],
        ],
    )

    schema = module.params.get('schema')
    site = module.params.get('site')
    template = module.params.get('template').replace(' ', '')
    bd = module.params.get('bd')
    host_route = module.params.get('host_route')
    svi_mac = module.params.get('svi_mac')
    state = module.params.get('state')

    mso = MSOModule(module)

    # Get schema_id
    schema_obj = mso.get_obj('schemas', displayName=schema)
    if not schema_obj:
        mso.fail_json(msg="Provided schema '{0}' does not exist".format(schema))

    schema_path = 'schemas/{id}'.format(**schema_obj)
    schema_id = schema_obj.get('id')

    # Get template
    templates = [t.get('name') for t in schema_obj.get('templates')]
    if template not in templates:
        mso.fail_json(msg="Provided template '{0}' does not exist. Existing templates: {1}".format(template, ', '.join(templates)))

    # Get site
    site_id = mso.lookup_site(site)

    # Get site_idx
    if 'sites' not in schema_obj:
        mso.fail_json(msg="No site associated with template '{0}'. Associate the site with the template using mso_schema_site.".format(template))
    sites = [(s.get('siteId'), s.get('templateName')) for s in schema_obj.get('sites')]
    if (site_id, template) not in sites:
        mso.fail_json(msg="Provided site-template association '{0}-{1}' does not exist.".format(site, template))

    # Schema-access uses indexes
    site_idx = sites.index((site_id, template))
    # Path-based access uses site_id-template
    site_template = '{0}-{1}'.format(site_id, template)

    # Get BD
    bd_ref = mso.bd_ref(schema_id=schema_id, template=template, bd=bd)
    bds = [v.get('bdRef') for v in schema_obj.get('sites')[site_idx]['bds']]
    if bd is not None and bd_ref in bds:
        bd_idx = bds.index(bd_ref)
        bd_path = '/sites/{0}/bds/{1}'.format(site_template, bd)
        mso.existing = schema_obj.get('sites')[site_idx]['bds'][bd_idx]
        mso.existing['bdRef'] = mso.dict_from_ref(mso.existing.get('bdRef'))

    if state == 'query':
        if bd is None:
            mso.existing = schema_obj.get('sites')[site_idx]['bds']
            for bd in mso.existing:
                bd['bdRef'] = mso.dict_from_ref(bd.get('bdRef'))
        elif not mso.existing:
            mso.fail_json(msg="BD '{bd}' not found".format(bd=bd))
        mso.exit_json()

    bds_path = '/sites/{0}/bds'.format(site_template)
    ops = []

    mso.previous = mso.existing
    if state == 'absent':
        if mso.existing:
            mso.sent = mso.existing = {}
            ops.append(dict(op='remove', path=bd_path))

    elif state == 'present':
        if not mso.existing:
            if host_route is None:
                host_route = False

        payload = dict(
            bdRef=dict(
                schemaId=schema_id,
                templateName=template,
                bdName=bd,
            ),
            hostBasedRouting=host_route,
        )
        if svi_mac is not None:
            payload.update(mac=svi_mac)

        mso.sanitize(payload, collate=True)

        if mso.existing:
            ops.append(dict(op='replace', path=bd_path, value=mso.sent))
        else:
            ops.append(dict(op='add', path=bds_path + '/-', value=mso.sent))

        mso.existing = mso.proposed

    if not module.check_mode and mso.existing != mso.previous:
        mso.request(schema_path, method='PATCH', data=ops)

    mso.exit_json()


if __name__ == "__main__":
    main()
