from setuptools import setup, find_packages

setup(
    name='package',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'requests',
        'numpy',
        'matplotlib',
        're',
        'os',
        'time',
        'shutil',
        'geopy',
        'datetime',
        'typing'
    ],
)