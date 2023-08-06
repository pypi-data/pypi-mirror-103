from setuptools import setup, find_packages

from example_package import __version__


def read_file(file_name):
    with open(file_name) as input_stream:
        return input_stream.read()


setup(
    name='flisol-example-package',
    version=__version__,
    description='FLISol Example Package',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    url='https://gitlab.com/ettoreleandrotognoli/pypi-flisol',
    author='Ettore Leandro Tognoli',
    author_email='ettoreleandrotognoli@gmail.com',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
    ],
    packages=find_packages(exclude=('tests',)),
)