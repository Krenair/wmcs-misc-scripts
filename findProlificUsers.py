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

roles = {}
for role in keystone_client.roles.list():
    roles[role.id] = role.name

import collections
user_adminships = collections.defaultdict(list)

for ra in keystone_client.role_assignments.list():
    role_name = roles[ra.role['id']]
    if role_name in ['projectadmin', 'user']:
        user_adminships[ra.user['id']].append(ra.scope['project']['id'])

user_admincount = collections.Counter()
for user, project_list in user_adminships.items():
    user_admincount[user] = len(project_list)

for user, admincount in user_admincount.most_common():
    if admincount > 5:
        print(user, admincount)

#for project in keystone_client.projects.list():
#    print(project, dir(project))
#    session = get_keystone_session(project.name)
#    client = novaclient.Client("2.0", session=session)
#    if project.name != 'admin':
#        for server in client.servers.list():
#            if 'cumin' in server.name:
#                print(project.name, server.name)
