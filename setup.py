from setuptools import setup, find_packages

setup(
    name='cloud-management-tool',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'Django==3.2',
        'djangorestframework==3.12',
        'boto3==1.17',
        'azure-mgmt-resource==16.1.0',
        'PyQt5==5.15',
        'psycopg2-binary'
    ],
    entry_points={
        'console_scripts': [
            'manage=backend.manage:main',
        ],
    },
)
