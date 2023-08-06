import setuptools
from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup_args = dict(
    name='RT-Congestion-Control',
    version='1.3',
    description='Implement exogenous peer to peer algorithm for Real time Congestion Control in distribution networks',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    license='MIT',
    packages=find_packages(),
    author='Guénolé CHEROT',
    author_email='guenole.cherot@ens-rennes.fr',
    keywords=['Distributed Optimisation', 'Peer-to-peer', 'Distribution System Operator',
     'Cost Allocation','Real-Time', 'Flexibility', 'Congestion Management'],
    url='https://gitlab.com/satie.sete/rt-congestion-control',
    download_url='https://gitlab.com/satie.sete/rt-congestion-control/-/archive/1.3/admm-1.3.tar.gz')


install_requires = [
    'pandapower',
    'flake8',
    'matplotlib',
    'osqp',
    'tqdm',
    'numpy',
    'scipy',
    'joblib',
    'numba',
    'plotly'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)