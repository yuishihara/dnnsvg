from setuptools import find_packages
from setuptools import setup

install_requires = []
tests_require = []
setup_requires = []

setup(
    name='dnnsvg',
    version='0.0.1',
    description='NNSVG inspired network structure drawer for deep learning',
    author='Yu Ishihara',
    author_email='yuishihara1225@gmail.com',
    install_requires=install_requires,
    url='https://github.com/yuishihara/dnnsvg',
    license='MIT License',
    packages=find_packages(exclude=('tests')),
    setup_requires=setup_requires,
    test_suite='tests',
    tests_require=tests_require
)
