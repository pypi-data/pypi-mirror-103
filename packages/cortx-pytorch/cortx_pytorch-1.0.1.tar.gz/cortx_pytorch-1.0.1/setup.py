from setuptools import setup

import os

current_directory = os.path.dirname(os.path.abspath(__file__))
try:
    with open(os.path.join(current_directory, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except Exception:
    long_description = ''

setup(name='cortx_pytorch',
      version='1.0.1',
      description='Fast interface between pytorch and Segate CORTX',
      author='Guillaume Leclerc',
      author_email='leclerc@mit.edu',
      url='https://github.com/GuillaumeLeclerc/cortx_pytorch',
      packages=['cortx_pytorch'],
      long_description=long_description,
      long_description_content_type='text/markdown',
      install_requires=[
          'torch',
          'tqdm',
          'boto3',
          'webdataset'
      ]
     )
