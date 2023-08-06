from setuptools import setup
import os


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as fp:
        s = fp.read()
    return s


setup(name='randdate',
      version='0.1.1',
      description='Generate a list of random dates or resp. datetime objects',
      long_description=read('README.rst'),
      long_description_content_type='text/markdown',
      url='http://github.com/kmedian/randdate',
      author='Ulf Hamster',
      author_email='554c46@gmail.com',
      license='Apache License 2.0',
      packages=['randdate'],
      # install_requires=[],
      python_requires='>=3.6',
      zip_safe=True)
