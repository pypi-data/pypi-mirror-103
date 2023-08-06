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


setup(name='numpy-fracadf',
      version=get_version("numpy_fracadf/__init__.py"),
      description='Determine fractal order by the ADF test',
      long_description=read('README.rst'),
      url='http://github.com/ulf1/fracadf',
      author='Ulf Hamster',
      author_email='554c46@gmail.com',
      license='Apache License 2.0',
      packages=['numpy_fracadf'],
      install_requires=[
          'numpy>=1.18.*,<2',
          'scipy>=1.4.*,<2',
          'statsmodels>=0.11.*',
          'numpy-fracdiff>=0.3.1'
      ],
      python_requires='>=3.6',
      zip_safe=True)
