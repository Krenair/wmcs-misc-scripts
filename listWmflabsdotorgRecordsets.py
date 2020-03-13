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

client = designateclient.Client(session=get_keystone_session('wmflabsdotorg'))
zone = client.zones.get('wmflabs.org.')
for recordset in client.recordsets.list(zone['id']):
    if recordset['type'] != 'A' or recordset['records'] != ['185.15.56.49']:
        print('|' + recordset['name'] + '|' + recordset['type'] + '|' + repr(recordset['records']) + '|' + repr(recordset['description']) + '|')
