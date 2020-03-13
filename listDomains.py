import yaml

from keystoneclient.session import Session as KeystoneSession
from keystoneclient.auth.identity.v3 import Password as KeystonePassword
from keystoneclient.v3 import Client as KeystoneClient
from designateclient.v2 import client as designateclient

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

for project in keystone_client.projects.list():
    session = get_keystone_session(project.name)
    if project.name != 'admin':
        client = designateclient.Client(session=session)
        for zone in client.zones.list():
            print(project.name, zone['name'])
#        client = novaclient.Client("2.0", session=session)
#        for server in client.servers.list():
#            print(project.name, server.name)
