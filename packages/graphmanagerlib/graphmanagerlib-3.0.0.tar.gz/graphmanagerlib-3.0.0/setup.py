from setuptools import find_packages, setup


setup(
    name='graphmanagerlib',
    packages=find_packages(),
    version='3.0.0',
    description='My first Python library',
    author='Cambier Damien',
    license='MIT',
    install_requires=['tensorflow==2.4.1',
                      'pandas==1.1.5',
                      'networkx==2.5.1',
                      'torch==1.8.0',
                      'torch-geometric==1.7.0',
                      'bpemb==0.3.3',
                      'sklearn==0.0',
                      'matplotlib==3.4.1',
                      'python-Levenshtein==0.12.2',
                      'opencv-python==4.5.1.48',
                      'sentence-transformers==1.0.4'],
)