# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

VERSION = __import__('nomnom').get_version()
        
CLASSIFIERS = [
    'Development Status :: 2 - Pre-Alpha',
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Software Development',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
]

# get install_requires from requirements.txt
text = open('requirements.txt', 'r')
REQUIREMENTS = text.readlines()
i = 0
while i < len(REQUIREMENTS):
    REQUIREMENTS[i] = REQUIREMENTS[i].replace('\n', '')
    i += 1

setup(
    author="Kevin Harvey",
    author_email="kevin@storyandstructure.com",
    name='django-nomnom',
    version=VERSION,
    description='Generic importing tool for the Django admin site.',
    long_description='',
    license='MIT',
    keywords='django, import, admin',
    url='https://github.com/storyandstructure/django-nomnom/',
    platforms=['OS Independent'],
    classifiers=CLASSIFIERS,
    install_requires=REQUIREMENTS,
    packages=find_packages(),
    include_package_data=True,
    zip_safe = False
)
