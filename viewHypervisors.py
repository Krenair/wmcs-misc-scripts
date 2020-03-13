import collections
import sys

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

hypervisor_groups = collections.defaultdict(list)

for project in keystone_client.projects.list():
    if project.name != 'admin':
        session = get_keystone_session(project.name)
        for region in ['eqiad1-r']:
            client = novaclient.Client("2.0", session=session, region_name=region)
            for server in client.servers.list():
                # OS-EXT-SRV-ATTR:host is the short name of the hypervisor, :hypervisor_hostname is the full FQDN including .eqiad.wmnet etc.
                hypervisor_groups[getattr(server, 'OS-EXT-SRV-ATTR:hypervisor_hostname')].append(server.name + '.' + project.name + '.eqiad.wmflabs')

for hypervisor, instances in sorted(hypervisor_groups.items(), key=lambda t: t[0]):
    if len(sys.argv) > 1 and hypervisor not in sys.argv:
#        print(hypervisor, sys.argv)
        continue
    print('{}:'.format(hypervisor))
    for instance in instances:
        print('    {instance}'.format(instance=instance))
