from keystoneclient.session import Session as KeystoneSession
from keystoneclient.auth.identity.v3 import Password as KeystonePassword
from keystoneclient.v3 import Client as KeystoneClient
#from novaclient import client as novaclient
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

session = get_keystone_session('admin')
#nclient = novaclient.Client("2.0", session=session, region_name='eqiad1-r')
#for s in nclient.servers.list():
#    print(s)

from designateclient.v2.base import V2Controller


client = designateclient.Client(session=session)
for zone in client.zones.list():
    print(zone, dir(zone))

