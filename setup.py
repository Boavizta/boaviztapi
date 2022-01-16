import sys

from setuptools import setup, find_packages

py_version = sys.version_info[:2]
if py_version < (3, 7):
    raise Exception("api requires Python >= 3.7.")

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='boaviztapi',
      version='0.0.1',
      packages=find_packages(),
      include_package_data=True,
      description="Giving access to BOAVIZTA referenced datas and methodologies trought a RESTful api ",
      use_pipfile=True,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/Boavizta/Tools-API",
      test_suite='tests',
      setup_requires=['setuptools-pipfile'],
      keywords=['boavizta', 'api'],
      classifiers=[
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.7",
          "Programming Language :: Python :: 3.8",
          "Programming Language :: Python :: 3.9",
          "Intended Audience :: Developers",
          "Operating System :: OS Independent",
      ],
      python_requires='>=3.7',
      entry_points=''' ''')
