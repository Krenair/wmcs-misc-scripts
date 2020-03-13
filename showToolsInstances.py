import ipaddress
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

def is_valid_ipv4(ip):
    """
    Returns true if ip is a valid ipv4 address
    """
    try:
        ipaddress.IPv4Address(ip)
        return True
    except ipaddress.AddressValueError:
        return False


session = get_keystone_session('tools')
client = novaclient.Client("2.0", session=session, region_name='eqiad1-r')
for instance in client.servers.list():
    # Only provide internal IPs!
    if "public" in instance.addresses:
        # This is a nova-network instance
        for ip in instance.addresses["public"]:
            if ip["OS-EXT-IPS:type"] == "fixed" and is_valid_ipv4(ip["addr"]):
                print(str(ip["addr"]))
    else:
        # This is probably a neutron instance.  Export all fixed
        #  addresses (probably there's only one)
        for value in instance.addresses.values():
            for ip in value:
                if ip["OS-EXT-IPS:type"] == "fixed" and is_valid_ipv4(ip["addr"]):
                    print(str(ip["addr"]))

