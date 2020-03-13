from __future__ import print_function

import collections
import yaml

from keystoneclient.session import Session as KeystoneSession
from keystoneclient.auth.identity.v3 import Password as KeystonePassword
from keystoneclient.v3 import Client as KeystoneClient
from novaclient import client as novaclient
from glanceclient import client as glanceclient

def get_keystone_session(project):
    return KeystoneSession(auth=KeystonePassword(
        auth_url="http://cloudcontrol1004.wikimedia.org:5000/v3",
        username="novaobserver",
        password=open('novaobserver_password').read(),
        project_name=project,
        user_domain_name='default',
        project_domain_name='default'
    ))


keystone_client = KeystoneClient(
    session=get_keystone_session('bastion'),
    endpoint="http://cloudcontrol1004.wikimedia.org:5000/v3",
    interface='public'
)

flavours = {}
flavour_projects = collections.defaultdict(list)
observer_list = []
projects = keystone_client.projects.list()
for project in projects:
    if project.name != 'admin':
        session = get_keystone_session(project.name)
        nclient = novaclient.Client("2.0", session=session, region_name='eqiad1-r')
        for flavour in nclient.flavors.list():
            flavours[flavour.id] = flavour
            flavour_projects[flavour.id].append(project.name)
            

all_project_count = len(projects) - 1
for flavour in flavours.values():
    this_flavour_projects = flavour_projects[flavour.id]
    ram_gbs = float(flavour.ram) / 1024
    if ram_gbs % 1 == 0:
        ram_gbs = int(ram_gbs)
    print('Name {flavour.name}: {flavour.vcpus} VCPUs, {ram_gbs} GB RAM, {flavour.disk} GB disk space total. Available to '.format(flavour=flavour, ram_gbs=ram_gbs), end='')
    if len(this_flavour_projects) < all_project_count:
        print('projects: {projects}'.format(projects=this_flavour_projects))
    else:
        print('all')


