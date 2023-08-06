from distutils.core import setup
from setuptools import find_packages

with open("README.rst", "r") as f:
    long_description = f.read()

setup(name='kady-hello',  # 包名
      version='1.0.1',  # 版本号
      description='A small example package',
      long_description=long_description,
      author='kady',
      author_email='1057097750@qq.com',
      url='http://www.haiseer.com',
      install_requires=[],
      license='BSD License',
      packages=find_packages(),
      platforms=["all"],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python :: 3.8',
          'Topic :: Software Development :: Libraries'
        ],
      )
