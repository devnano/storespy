#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import setuptools


# Configure the required packages and scripts to install.
# Note that the Python Dataflow containers come with numpy already installed
# so this dependency will not trigger anything to be installed unless a version
# restriction is specified.
REQUIRED_PACKAGES = [
    'requests==2.18.4',
    'pytest==3.3.2',
    'demjson==2.2.4',
    'xmltodict==0.11.0',
    'python-dateutil==2.6.1'
    ]

#DEPENDENCY_LINKS = [
#    'git+https://github.com/winclap/play-scraper.git@v0.2.0'
#]

setuptools.setup(
    name='storespy',
    version='0.0.16',
    description='Get Google Play and App Store app info.',
    packages=['storespy', 'play_scraper'],
    install_requires=REQUIRED_PACKAGES,
#    dependency_links=DEPENDENCY_LINKS,
    )
