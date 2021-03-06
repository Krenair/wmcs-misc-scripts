import sys
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

session = get_keystone_session(sys.argv[1])
client = novaclient.Client("2.0", session=session)
for server in client.servers.list():
    if sys.argv[2] in server.name:
        print(server.name, server, server.hostId)
