#!/usr/bin/env python
from setuptools import setup, find_packages
from sys import version_info
from cron_sentry.version import VERSION

requirements = ['raven']
if version_info < (2, 7, 0):
    requirements.append('argparse')

setup(
    name='cron-sentry',
    version=VERSION,
    author='Yipit Coders',
    author_email='coders@yipit.com',
    description='Cron-Sentry is a command-line wrapper that reports unsuccessful runs to Sentry (https://www.getsentry.com)',
    long_description=open('README.md').read(),
    license='MIT',
    classifiers=[
        'Topic :: Utilities',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    url='http://github.com/yipit/cron-sentry',
    packages=find_packages(),
    install_requires=requirements,
    data_files=[],
    entry_points={
        'console_scripts': [
            # `raven-cron` entry point is for backwards compatibility purposes.
            # it should get removed in future releases
            'raven-cron = cron_sentry.runner:run',
            'cron-sentry = cron_sentry.runner:run',
        ]
    }
)
