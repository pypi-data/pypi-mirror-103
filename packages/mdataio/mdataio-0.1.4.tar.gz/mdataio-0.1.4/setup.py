import setuptools
try: # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError: # for pip <= 9.0.3
    from pip.req import parse_requirements

# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements("requirements.txt", session=False)
# reqs is a list of requirement
reqs = [str(ir.req) for ir in install_reqs]

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name='mdataio',
    version='0.1.4',
    author="Xin Yi",
    description="scripts used for meidcal data manipulation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    url = 'https://xinario.github.io',   
    download_url = 'https://github.com/xinario/mdataio/archive/refs/tags/0.1.4.tar.gz',   
    packages=['mdataio'],
    install_requires=reqs,
    classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    ],
 )



