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

from designateclient.v2.base import V2Controller


class PoolController(V2Controller):
    def list(self):
        url = '/pools'
        return self._get(url, response_key='pools')

client = designateclient.Client(session=get_keystone_session('wmflabsdotorg'))
for nameserver in PoolController(client).list():
    print(nameserver, dir(nameserver))
