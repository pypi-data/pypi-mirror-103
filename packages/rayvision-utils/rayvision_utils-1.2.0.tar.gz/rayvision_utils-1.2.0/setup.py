"""Describe our module distribution to Distutils."""

# Import third-party modules
from setuptools import find_packages
from setuptools import setup

def parse_requirements(filename):
    with open(filename, "r") as f:
        for line in f:
            yield line.strip()

setup(
    name='rayvision_utils',
    author='Shenzhen Rayvision Technology Co., Ltd',
    author_email='developer@rayvision.com',
    url='https://github.com/renderbus/rayvision_utils',
    package_dir={'': '.'},
    packages=find_packages('.'),
    description='A Python API for Using Renderbus cloud rendering.',
    entry_points={},
    install_requires=list(parse_requirements('requirements.txt')),
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    use_scm_version=True,
    setup_requires=['setuptools_scm', 'pytest-runner'],
    tests_require=['pytest==4.6', 'pytest-mock==1.10']
)
