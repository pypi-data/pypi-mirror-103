import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

requires = [
    'pandas',
    'PyYAML==5.4.1',
    'httplib2~=0.19.1',
    'oauth2client~=4.1.3',
    'google-api-python-client~=2.2.0',
    'pyOpenSSL==20.0.1',
    'pytest',
    'boto3'
]

setuptools.setup(
    name='data_tap',
    version='0.0.7',
    description='A python wrapper that connects to multiple 3rd party resources for AWS.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='DirkSCGM',
    author_email='dirkscgm@gmail.com',
    url='https://github.com/DirksCGM/data-tap',
    classifiers=['Programming Language :: Python :: 3 :: Only'],
    packages=setuptools.find_packages(),
    install_requires=requires,
    python_requires='>=3',
    keywords=['aws', 's3', 'google', 'google analytics', 'google search console', 'data', 'pipeline']
)
