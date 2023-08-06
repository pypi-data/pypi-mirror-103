from setuptools import setup

__version__ = "0.3.0"
setup(name='test-cicd-pipeline',
      version=__version__,
      description='Package to setup and test basic CICD pipeline',
      author_email='maarten.s1991@gmail.com',
      packages=['src', 'testing'],
      url='https://github.com/Maarten-s1991/testcicd',
      zip_safe=False
      )
