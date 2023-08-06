
from setuptools import setup, find_packages

VERSION = '0.1.2'

setup(name='anndb_api',
    version=VERSION,
    description='AnnDB API Client',
    author='Marek Galovic',
    author_email='contact@anndb.com',
    license='Apache-2.0',
    url='https://github.com/anndb-com/anndb-api-client-python',
    download_url='https://github.com/anndb-com/anndb-api-client-python/archive/%s.tar.gz' % VERSION,
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        'google',
        'protobuf',
        'grpcio'
    ],
)