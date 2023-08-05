from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='data-tap',
    install_requires=required,
    description="A python wrapper that connects to multiple 3rd party resources for AWS.",
    version='0.0.5',
    url='https://github.com/DirksCGM/data-tap',
    author='DirkSCGM',
    author_email='dirkscgm@gmail.com',
    keywords=[
        'aws',
        'datapipeline',
        'google',
        'analytics'
    ]
)
