import os
from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
]

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='PC-Info',
    version='1.0.2',
    description='PC-Info is a library used for getting all kinds of information about the computer you are using this module on.',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/stop-bark/PC-Info',
    author='imagine#0403',
    author_email='imagine@stop-bark.club',
    license='MIT',
    classifiers=classifiers,
    keywords=['pc-info', 'info', 'pc', 'pcinfo'],
    packages=find_packages(),
    install_requires=['']
)
