from setuptools import setup, find_packages

setup(name="mes_server_proj",
      version="1.0.0",
      description="mes_server_proj",
      author="Anton Kuznetsov",
      author_email="fireflysmk@google.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )