from keystoneclient.session import Session as KeystoneSession
from keystoneclient.auth.identity.v3 import Password as KeystonePassword
from neutronclient.v2_0 import client as neutronclient

def get_keystone_session(project):
    return KeystoneSession(auth=KeystonePassword(
        auth_url="http://cloudcontrol1003.wikimedia.org:5000/v3",
        username="novaobserver",
        password=open('novaobserver_password').read(), # read-only guest account, password is public
        project_name=project,
        user_domain_name='default',
        project_domain_name='default'
    ))

session = get_keystone_session('bastion')
client = neutronclient.Client(session=session, region_name='eqiad1-r')
print(client)
print(client.list_quotas())
