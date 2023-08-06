from setuptools import find_packages, setup

setup(
    name='awdflag',
    version='1.2.3',
    description='Test setup',
    author='Evi1oX',
    author_email='dropboy@qq.com',
    url='https://evi1ox.github.io',

    install_requires=[
        'Cython',
        'paramiko',
        'pysmb',
        'pywinrm',
        'pypsrp',
        'impacket',
        'pyasn1>=0.2.3',
        'pycryptodomex',
        'pyOpenSSL>=0.13.1',
        'six',
        'ldap3>=2.5,!=2.5.2,!=2.5.0,!=2.6',
        'ldapdomaindump>=0.9.0',
        'flask>=1.0',
        'cx_Oracle',
        'pandas',
        'pymssql'
    ],
    packages=find_packages(),
    python_requires='>=3.6',
)
