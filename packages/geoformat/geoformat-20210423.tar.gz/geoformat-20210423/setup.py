from setuptools import setup, find_packages

from geoformat import version

markdown_path = 'README.md'

with open(markdown_path) as read_me_file:
    read_me_file_txt = read_me_file.read()

setup(
    name='geoformat',
    version=str(version(verbose=False)),
    url='https://framagit.org/Guilhain/Geoformat',
    license='MIT',
    author='Guilhain Averlant',
    author_email='g.averlant@mailfence.com',
    description='Geoformat is a GDAL/OGR library overlayer',
    long_description=read_me_file_txt,
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=["data"]),
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Topic :: Scientific/Engineering :: GIS",
    ]
)
