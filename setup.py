from pathlib import Path
from typing import Union

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


def read_requirements(path: Union[str, Path]):
    with open(path, "r") as file:
        return file.read().splitlines()


requirements = read_requirements("requirements.txt")
requirements_dev = read_requirements("requirements_dev.txt")


setuptools.setup(
    name="lollms_server_proxy",
    version="0.0.1",
    author="Saifeddine ALOUI (ParisNeo)",
    author_email="aloui.saifeddine@gmail.com",
    description="A fastapi server for petals decentralized text generation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ParisNeo/lollms_server_proxy",
    packages=setuptools.find_packages(),  
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'lollms_server_proxy = lollms_server_proxy.main:main',
            'lollms_server_add_user = lollms_server_proxy.add_user:main',
        ],
    },
    extras_require={"dev": requirements_dev},
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
