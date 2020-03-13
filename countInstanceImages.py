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

image_counts = collections.defaultdict(int)
for project in keystone_client.projects.list():
    if project.name != 'admin':
        session = get_keystone_session(project.name)
        for region in ['eqiad1-r']:
            nclient = novaclient.Client("2.0", session=session, region_name=region)
            instance_images = collections.defaultdict(list)
            for s in nclient.servers.list():
                instance_images[s.name] = s.image['id']
            gclient = glanceclient.Client(version=2, session=session, region_name=region)
            existing_images = {}
            for image in gclient.images.list():
                existing_images[image.id] = image.name
            for instance, image_id in instance_images.items():
                image_counts['all'] += 1
                image_name = existing_images.get(image_id)
                if image_name is None:
                    image_counts[None] += 1
                elif 'jessie' in image_name:
                    image_counts['jessie'] += 1
                elif 'stretch' in image_name:
                    image_counts['stretch'] += 1
                elif 'buster' in image_name:
                    image_counts['buster'] += 1
                elif 'trusty' in image_name:
                    image_counts['trusty'] += 1
                elif 'precise' in image_name:
                    image_counts['precise'] += 1
                    print('PRECISE', instance)
                else:
                    image_counts[image_name] += 1

print(dict(image_counts))
