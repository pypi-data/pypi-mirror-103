from setuptools import setup, find_packages

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name="tagscounteralexdoka",
    packages=["tagscounteralexdoka"],
    # find_packages(),
    version="0.1.0",
    author="Aliaksandr Dakutovich",
    author_email="alex.doka@gmail.com",
    description="app counting tags on web page",
    long_description=readme(),
    license="MIT",
    include_package_data=True,
    entry_points={'console_scripts': ['tagcounter = tagscounteralexdoka.tagcounter:main']},
    install_requires=[
         'argparse',
         'datetime',
         'certifi==2020.12.5',
         'chardet', 
         'future==0.18.2',
         'PyYAML==5.4.1',
         'idna==2.10',
         'tk',
         'requests==2.25.1',
         'urllib3'
      ]
)

