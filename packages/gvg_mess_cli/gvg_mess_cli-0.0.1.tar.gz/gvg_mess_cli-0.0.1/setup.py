from setuptools import setup, find_packages

setup(name="gvg_mess_cli",
      version="0.0.1",
      description="gvg messanger client",
      author="Gulin Vitaliy",
      author_email="gvitaly@mail.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
