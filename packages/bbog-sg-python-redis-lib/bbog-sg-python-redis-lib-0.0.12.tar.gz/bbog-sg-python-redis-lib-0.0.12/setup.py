from pip._internal.network.session import PipSession
from setuptools import find_packages, setup
from pip._internal.req import parse_requirements
import os

requirements = parse_requirements(os.path.join(os.path.dirname(__file__), 'prodrequirements.txt'), session=PipSession())
requirements_as_array = [str(requirement.requirement) for requirement in requirements]

setup(
    name='bbog-sg-python-redis-lib',
    packages=find_packages(exclude=['test.*', 'test']),
    version='0.0.12',
    description='Python library to handle redis api',
    author='otacha@bancodebogota.com.co',
    license='MIT',
    install_requires=requirements_as_array,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='test',
)
