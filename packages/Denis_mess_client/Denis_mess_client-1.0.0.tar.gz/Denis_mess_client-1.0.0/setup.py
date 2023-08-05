from setuptools import setup, find_packages

setup(name="Denis_mess_client",
      version="1.0.0",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
