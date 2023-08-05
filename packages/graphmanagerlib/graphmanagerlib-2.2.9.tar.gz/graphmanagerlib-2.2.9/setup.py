from setuptools import find_packages, setup


setup(
    name='graphmanagerlib',
    packages=find_packages(),
    version='2.2.9',
    description='My first Python library',
    author='Cambier Damien',
    license='MIT',
    install_requires=['tensorflow',
                      'pandas',
                      'networkx',
                      'torch==1.8.0',
                      'torch-geometric',
                      'bpemb',
                      'sklearn',
                      'matplotlib',
                      'opencv-python',
                      'sentence_transformers',
                      'stellargraph'],
)