import collections
import yaml

from keystoneclient.session import Session as KeystoneSession
from keystoneclient.auth.identity.v3 import Password as KeystonePassword
from keystoneclient.v3 import Client as KeystoneClient
from novaclient import client as novaclient
from glanceclient import client as glanceclient

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

count = collections.Counter()
for project in keystone_client.projects.list():
    if project.name not in ['admin']:
        session = get_keystone_session(project.name)
        for region in ['eqiad1-r']:
            nclient = novaclient.Client("2.0", session=session, region_name=region)
            for s in nclient.servers.list():
                print(s.name, s.user_id)
                count[s.user_id] += 1

print('')
for creator, c in count.most_common():
    print(creator, c)
