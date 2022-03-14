from setuptools import setup, find_packages
#import gwmqtt.default_config as defCfg
#import json

version = {}
with open("gw_watchdog/version.py") as fp:
    exec(fp.read(), version)

setup(
    name='gw_watchdog',
    version=version['__version__'],
    url='https://github.com/iotmaxx/gw-watchdog',
    author='Ralf Glaser',
    author_email='glaser@iotmaxx.de',
    description='gateway watchdog',
    packages=find_packages(),    
    install_requires=[],
)
