from setuptools import setup, find_packages

setup(name="gvg_mess_srv",
      version="0.0.1",
      description="gvg messanger server",
      author="Gulin Vitaliy",
      author_email="gvitaly@mail.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
