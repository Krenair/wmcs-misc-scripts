import collections

from keystoneclient.session import Session as KeystoneSession
from keystoneclient.auth.identity.v3 import Password as KeystonePassword
from keystoneclient.v3 import Client as KeystoneClient
from neutronclient.v2_0 import client as neutronclient

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
    if project.name != 'admin':
        session = get_keystone_session(project.name)
        client = neutronclient.Client(session=session, region_name='eqiad1-r')
        print(client)
#        print(dir(client))
        print(client.list_quotas())
#        for s in client.servers.list():
#            migrated.append(s.name)

