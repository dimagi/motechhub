from setuptools import setup


setup(
    name='authproxy-client',
    version='1.0',
    description='Client library for authproxy',
    packages=[
        'authproxy_client',
    ],
    install_requires=[
        'jsonobject',
        'requests',
    ],
    tests_require=['unittest2'],
    test_suite='test',
)
