from keystoneclient.session import Session as KeystoneSession
from keystoneclient.auth.identity.v3 import Password as KeystonePassword
from novaclient import client as novaclient

def get_keystone_session(project):
    return KeystoneSession(auth=KeystonePassword(
        auth_url="http://cloudcontrol1003.wikimedia.org:5000/v3",
        username="novaobserver",
        password=open('novaobserver_password').read(),
        project_name=project,
        user_domain_name='default',
        project_domain_name='default'
    ))

session = get_keystone_session('deployment-prep')
instances = []
for region in ['eqiad', 'eqiad1-r']:
    client = novaclient.Client("2.0", session=session, region_name=region)
    for s in client.servers.list():
        instances.append(s.name)

import re
import collections
groups = collections.defaultdict(list)
for instance in instances:
    m = re.search(r'^(([^0-9]?[^0-9\-])*)-?[0-9]+$', instance)
    if m:
        group = m.group(1)
    else:
        group = instance
    groups[group].append(instance)

for group, instance_list in groups.items():
    print("{}:".format(group))
    for instance in instance_list:
        print("    {}".format(instance))
