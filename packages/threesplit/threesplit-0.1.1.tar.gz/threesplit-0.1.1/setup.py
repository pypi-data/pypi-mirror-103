from setuptools import setup
import os


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as fp:
        s = fp.read()
    return s


setup(name='threesplit',
      version='0.1.1',
      description=(
          "Three-way data split into training set, "
          "validation set, and test set."),
      long_description=read('README.rst'),
      long_description_content_type='text/markdown',
      url='http://github.com/kmedian/threesplit',
      author='Ulf Hamster',
      author_email='554c46@gmail.com',
      license='Apache License 2.0',
      packages=['threesplit'],
      install_requires=[
          'numpy>=1.14.5'],
      python_requires='>=3.6',
      zip_safe=True)
