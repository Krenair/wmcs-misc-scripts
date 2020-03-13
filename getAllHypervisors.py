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

hypervisors_seen = []
for project in keystone_client.projects.list():
    session = get_keystone_session(project.name)
    for region in ['eqiad', 'eqiad1-r']:
        client = novaclient.Client("2.0", session=session, region_name=region)
        if project.name != 'admin':
            for server in client.servers.list():
                hypervisor = getattr(server, 'OS-EXT-SRV-ATTR:hypervisor_hostname')
                if hypervisor not in hypervisors_seen:
                    hypervisors_seen.append(hypervisor)
                    print(hypervisor)
