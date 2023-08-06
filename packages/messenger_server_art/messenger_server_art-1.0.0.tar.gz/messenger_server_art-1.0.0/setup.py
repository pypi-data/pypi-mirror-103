from setuptools import setup, find_packages

setup(name="messenger_server_art",
      version="1.0.0",
      description="messenger_server_art",
      author="Artem",
      author_email="artmikh@yandex.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
