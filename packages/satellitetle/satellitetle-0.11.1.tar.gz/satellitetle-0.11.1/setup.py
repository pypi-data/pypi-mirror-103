from setuptools import setup

setup(name='satellitetle',
      version='0.11.1',
      description='Fetch satellite TLEs from various online sources',
      url='https://gitlab.com/librespacefoundation/python-satellitetle',
      author='Fabian P. Schmidt',
      author_email='kerel-fs@gmx.de',
      license='MIT',
      long_description=open('README.rst').read(),
      packages=['satellite_tle'],
      install_requires=[
          'requests~=2.25.0',
          'sgp4~=2.18',
          'spacetrack~=0.16.0',
      ],
      extras_require={'dev': [
          'flake8~=3.9.0',
          'tox~=3.23.0',
      ]},
      package_data={'satellite_tle': ['sources.csv']},
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
      ],
      )
