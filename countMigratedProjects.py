import collections
import yaml

from keystoneclient.session import Session as KeystoneSession
from keystoneclient.auth.identity.v3 import Password as KeystonePassword
from keystoneclient.v3 import Client as KeystoneClient
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

keystone_client = KeystoneClient(
    session=get_keystone_session('bastion'),
    endpoint="http://cloudcontrol1003.wikimedia.org:5000/v3",
    interface='public'
)

migrated = {}
non_migrated = {}
empty = []

for project in keystone_client.projects.list():
    if project.name != 'admin':
        session = get_keystone_session(project.name)
        c = collections.Counter()
        for region in ['eqiad', 'eqiad1-r']:
            client = novaclient.Client("2.0", session=session, region_name=region)
            for s in client.servers.list():
                c[region] += 1

        proj_migrated = c['eqiad'] == 0 and c['eqiad1-r'] > 0
        if sum(c.values()) == 0:
            empty.append(project.name)
        elif proj_migrated:
            migrated[project.name] = c
        else:
            non_migrated[project.name] = c

print('Migrated:')
for project_name, counts in sorted(migrated.items(), key=lambda t: sum(t[1].values())):
    if sum(counts.values()):
        print(project_name, counts)

print('')
print('Non-migrated:')
for project_name, counts in sorted(non_migrated.items(), key=lambda t: sum(t[1].values())):
    if sum(counts.values()):
        print(project_name, counts)

print('')
print('Empty:')
for project_name in empty:
    print(project_name)
