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

projects = [
    'automation-framework',
    'bstorm-test',
    'cloudinfra',
    'deployment-prep',
    'gerrit',
    'git',
    'hound',
    'integration',
    'phabricator',
    'puppet',
    'striker',
    'testlabs',
    'thumbor',
    'tools',
    'toolsbeta',
    'traffic',
    'wikifactmine',
    'wmcs-nfs'
]

t = 0
for project in projects:
    session = get_keystone_session(project)
    c = 0
    for region in ['eqiad', 'eqiad1-r']:
        client = novaclient.Client("2.0", session=session, region_name=region)
        for s in client.servers.list():
            c += 1
    print(project, c)
    t += c

print('Total', t)
