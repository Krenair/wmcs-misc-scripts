# wmcs-misc-scripts
A collection of random scripts used for getting info from WMCS OpenStack

This is a bunch of things that talk to WMCS's OpenStack Keystone, Nova, Designate, Glance, etc. to generate info I found useful at one point or another when helping administer Wikimedia Cloud VPS. They are unlikely to work outside of the Wikimedia network.

Traditionally these lived at shinken-01.shinken.eqiad.wmflabs:~krenair for historical Wikimedia OpenStack client packaging reasons (most existing instances did not have the right versions of the packages).

They rely on the public novaobserver password (found as novaconfig.observer_password at https://github.com/wikimedia/labs-private/blob/master/hieradata/labs.yaml#L6), stored in a file named `novaobserver_password`.

These are not official enough for me to request a repo in Gerrit, or even really for me to put them in the Wikimedia org in GitHub. So this sits in my personal GitHub space.

Some no longer work (probably any with region `eqiad` instead of `eqiad1-r`).

Copyright 2016-2020 Alex Monk. Licensed Apache 2.0. Some files may have copyright jointly held with Wikimedia Foundation, Inc.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
