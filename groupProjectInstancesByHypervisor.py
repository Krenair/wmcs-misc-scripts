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

session = get_keystone_session('deployment-prep')
hypervisor_groups = collections.defaultdict(list)
for region in ['eqiad', 'eqiad1-r']:
    client = novaclient.Client("2.0", session=session, region_name=region)
    for server in client.servers.list():
        # OS-EXT-SRV-ATTR:host is the short name of the hypervisor, :hypervisor_hostname is the full FQDN including .eqiad.wmnet etc.
        hypervisor_groups[getattr(server, 'OS-EXT-SRV-ATTR:hypervisor_hostname')].append(server)

for hypervisor, instances in hypervisor_groups.items():
    print('{}:'.format(hypervisor))
    for instance in instances:
        print('    {instance.name}'.format(instance=instance))
