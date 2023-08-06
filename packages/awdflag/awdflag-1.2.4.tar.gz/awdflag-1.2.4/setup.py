from setuptools import find_packages, setup

setup(
    name='awdflag',
    version='1.2.4',
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
        'pyasn1',
        'pycryptodomex',
        'pyOpenSSL',
        'six',
        'ldap3',
        'ldapdomaindump',
        'flask',
        'cx_Oracle',
        'pandas',
        'pymssql'
    ],
    packages=find_packages(),
    python_requires='>=3.6',
)
