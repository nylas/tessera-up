#!/usr/bin/env python

from setuptools import setup


setup(
    name='tessera-up',
    version='0.0.1',
    include_package_data = True,
    packages = ['tessera_up'],
    author = "Rob McQueen",
    author_email = "rob@nylas.com",
    maintainer = "Nylas Team",
    maintainer_email = "support@nylas.com",
    description = "Uploads dashboards to Tessera based on config directory",
    scripts=['bin/tessera-up'],
    install_requires=['tessera-client', 'PyYAML'],
    zip_safe=False
)
