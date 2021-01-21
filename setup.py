import os
import setuptools


setuptools.setup(
    setup_requires=['pbr>=1.8'],
    pbr=True
)


def mk_log_dir():
    log_dir = "/var/log/tianti"
    if os.path.exists(log_dir) is False:
        os.makedirs(log_dir)


mk_log_dir()