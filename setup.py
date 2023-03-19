from setuptools import setup, find_packages
import requests
NAME = 'zettasql'
LONG_DESC = ''
try:
    LONG_DESC = requests.get(
        "https://raw.githubusercontent.com/SoumadeepChoudhury/zettasql/main/README.md").text
except:
    LONG_DESC = ''
VERSION = ''
with open("./zclient/info.log", "r") as infoFile:
    lines = infoFile.readlines()
    for line in lines:
        if line.startswith("version :"):
            VERSION = line.split(":")[1].strip()

setup(
    name=NAME,
    version=VERSION,
    description="Secure and powerful database server.",
    long_description=LONG_DESC,
    long_description_content_type='text/markdown',
    author="Ahens | An Initiative to Initial",
    author_email="ahensinitiative@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    packages=find_packages(),
    include_package_data=True,
    package_data={'zclient': ['*.log']},
    entry_points={
        'console_scripts': ['zettasql-start=zserver.start:start', 'zettasql-stop=zserver.stop:stop', 'zettasql=zclient.main:main', 'zettasql-help=zserver.help:help'
                            ],
    },
)
