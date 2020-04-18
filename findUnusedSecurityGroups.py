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

for project in keystone_client.projects.list():
    if project.name not in ['admin']:
        session = get_keystone_session(project.name)
        client = novaclient.Client("2.0", session=session)
        in_use = set()
        for server in client.servers.list():
            for sg in server.list_security_group():
                in_use.add(sg.name)

        for sg in client.security_groups.list():
            if sg.name not in in_use:
                print(project.name, sg.name)

