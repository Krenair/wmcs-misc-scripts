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

#keystone_client = KeystoneClient(
#    session=get_keystone_session('bastion'),
#    endpoint="http://cloudcontrol1004.wikimedia.org:5000/v3",
#    interface='public'
#)

#image_counts = collections.Counter()
#for project in keystone_client.projects.list():
#    if project.name != 'admin':
#        session = get_keystone_session(project.name)
#        for region in ['eqiad1-r']:
#            nclient = novaclient.Client("2.0", session=session, region_name=region)
#            instance_images = collections.defaultdict(list)
#            for s in nclient.servers.list():
#                instance_images[s.name] = s.image['id']
#            gclient = glanceclient.Client(version=2, session=session, region_name=region)
#            existing_images = {}
#            for image in gclient.images.list():
#                existing_images[image.id] = image.name
#            for instance, image_id in instance_images.items():
#                image_name = existing_images.get(image_id)
#                image_counts[image_name] += 1

#for i in image_counts.most_common():
#    print("{} - {}".format(*i))

session = get_keystone_session('observer')
gclient = glanceclient.Client(version=2, session=session, region_name='eqiad1-r')
for image in gclient.images.list():
#    print(image, dir(image))
    print(image.status, image.id, image.name)
