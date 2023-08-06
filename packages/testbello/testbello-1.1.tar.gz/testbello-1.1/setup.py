from setuptools import setup, find_packages
from requests import get

setup(
      name='testbello',
      version="01.01", # Lastest release
      description="z",
      url="https://github.com/repos/CastellaniDavide/testbello",
      author="DavideC03",
      author_email="help@castellanidavide.it",
      license='GNU',
      packages=find_packages(),
      python_requires=">=3.6",
      platforms="linux_distibution",
      install_requires=["tabular-log", "requests", "programGUI"],
      zip_safe=True
      )