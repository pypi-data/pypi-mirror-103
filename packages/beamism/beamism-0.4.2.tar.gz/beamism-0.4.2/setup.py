# -*- coding: utf-8 -*-
#!/usr/bin/env python

from setuptools import setup, find_packages


REQUIRED_PACKAGES = [
    'apache-beam==2.28.0',
    'jsonschema>=3.2.0',
    'dill==0.3.1.1',
    'protobuf==3.12.2',
    'httplib2==0.17.3',
    'dill==0.3.1.1',
    'dnspython>=1.15.0',
    'gitpython>=3.0.5',
    'google-api-core==1.26.0',
    'google-apitools<0.5.32,>=0.5.31',
    'google-auth==1.25.0',
    'google-auth-httplib2==0.0.4',
    'google-cloud-core==1.1.0',
    'google-cloud-pubsub==1.0.2',
    'googleapis-common-protos==1.52.0',
    'oauth2client==3.0.0',
    'python-dateutil==2.8.1',
    'pymongo==3.10.1',
    'slackclient>=2.3.1'
]


with open('version.cache', 'r') as f:
    version = f.read()


setup(
    name="beamism",
    version=version,
    packages=find_packages(),
    description='welcome to beamism',
    platforms='Linux, Darwin',
    zip_safe=False,
    include_package_data=True,
    install_requires=REQUIRED_PACKAGES,
    license="MIT",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ]
)
