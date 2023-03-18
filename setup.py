from setuptools import setup,find_packages
import requests
NAME='zettasql'
try:
    LONG_DESC=requests.get("https://raw.githubusercontent.com/SoumadeepChoudhury/zettasql/main/README.md").text
except:
    LONG_DESC=''
VERSION=''
with open("./client/info.log","r") as infoFile:
    lines=infoFile.readlines()
    for line in lines:
        if line.startswith("version :"):
            VERSION=line.split(":")[1].strip()

setup(
    name=NAME,
    version=VERSION,
    description="Secure and powerful database server.",
    long_description=LONG_DESC,
    long_description_content_type='text/markdown',
    author="Ahens | An Initiative to Initial",
    packages=find_packages(exclude=['.*']),
    entry_points={
        'console_scripts':['zettasql-start=server.start:start','zettasql-stop=server.stop:stop','zettasql=client.main:main'
                               ],
        },
)


