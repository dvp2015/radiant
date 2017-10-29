import os
import re

from setuptools import setup, find_packages


with open(os.path.join("radiant", "__init__.py"), mode="r") as fh:
    version = re.match("__version__\s*=\s*['\"](.*?)['\"]", fh.read()).group(1)
packages = find_packages()
with open("requirements.txt", mode="r") as fh:
    install_requires = fh.readlines()


setup(
    name='radiant',
    version=version,
    packages=packages,
    install_requires=install_requires,
    extras_require={
        'PyQt5': ["PyQt5"],
        'moderngl': ["moderngl"],
    },
    description="",
    long_description="",
    author="Korijn van Golen",
    author_email="korijn@gmail.com",
    url="https://github.com/Korijn/radiant",
    license="MIT",
    platforms='any',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Topic :: Multimedia :: Graphics :: 3D Rendering',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
    ],
)
