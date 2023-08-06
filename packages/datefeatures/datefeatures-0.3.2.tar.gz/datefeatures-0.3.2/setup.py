from setuptools import setup
import os


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as fp:
        s = fp.read()
    return s


def get_version(path):
    with open(path, "r") as fp:
        lines = fp.read()
    for line in lines.split("\n"):
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")


setup(name='datefeatures',
      version=get_version("datefeatures/__init__.py"),
      description='Feature engineering sklearn transformer for dates',
      long_description=read('README.rst'),
      url='http://github.com/kmedian/datefeatures',
      author='Ulf Hamster',
      author_email='554c46@gmail.com',
      license='Apache License 2.0',
      packages=['datefeatures'],
      install_requires=[
          'numpy>=1.14.5',
          'scikit-learn>=0.20.0',
          'pandas>=0.23.4',
          'holidays>=0.9.9'],
      python_requires='>=3.6',
      zip_safe=True)
