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

for project in keystone_client.projects.list():
#for project in ['deployment-prep']:
    if project.name != 'admin':
        session = get_keystone_session(project.name)
#    if project != 'admin':
#        session = get_keystone_session(project)
        for region in ['eqiad', 'eqiad1-r']:
            nclient = novaclient.Client("2.0", session=session, region_name=region)
            image_instances = collections.defaultdict(list)
            for s in nclient.servers.list():
                image_instances[s.image['id']].append(s.name)
            gclient = glanceclient.Client(version=2, session=session, region_name=region)
            existing_images = {}
            for image in gclient.images.list():
                existing_images[image.id] = image.name
            for missing_image in set(image_instances.keys()) - set(existing_images.keys()):
                print(project.name, region, missing_image, image_instances[missing_image])
