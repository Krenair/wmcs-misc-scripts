#!/usr/bin/python3
from keystoneclient.session import Session as KeystoneSession
from keystoneclient.auth.identity.v3 import Password as KeystonePassword
from novaclient import client as novaclient

client = novaclient.Client(
    "2.0",
    session=KeystoneSession(auth=KeystonePassword(
        auth_url="http://{host}:{port}/v3".format(host="cloudcontrol1003.wikimedia.org", port=5000),
        username="novaobserver",
        password=open('novaobserver_password').read(), # public password for guest 'novaobserver' account
        project_name='deployment-prep',
        user_domain_name='default',
        project_domain_name='default'
    ))
)

for instance in sorted(client.servers.list(), key=lambda instance: instance.name):
    print(instance.name)
