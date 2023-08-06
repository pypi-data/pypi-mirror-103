from setuptools import setup, find_packages

setup(name="my_message_client",
      version="1.0.0",
      description="mess_client",
      author="Anton Kuznetsov",
      author_email="fireflysmk@google.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )


