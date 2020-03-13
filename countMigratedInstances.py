import collections

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

migrated = 0
non_migrated = 0
tools_migrated = 0
tools_non_migrated = 0

for project in keystone_client.projects.list():
    if project.name != 'admin':
        session = get_keystone_session(project.name)
        project_non_migrated = len(novaclient.Client("2.0", session=session, region_name='eqiad').servers.list())
        non_migrated += project_non_migrated
        project_migrated = len(novaclient.Client("2.0", session=session, region_name='eqiad1-r').servers.list())
        migrated += project_migrated
        if project.name in ['tools', 'toolsbeta']:
            tools_migrated += project_migrated
            tools_non_migrated += project_non_migrated

print('Total instances found: {}'.format(migrated + non_migrated))

print('Total migrated: {}'.format(migrated))
print('Total non-migrated: {}'.format(non_migrated))

print('Tools/toolsbeta migrated: {}'.format(tools_migrated))
print('Tools/toolsbeta non-migrated: {}'.format(tools_non_migrated))

print('Migrated without tools/toolsbeta: {}'.format(migrated - tools_migrated))
print('Non-migrated without tools/toolsbeta: {}'.format(non_migrated - tools_non_migrated))
