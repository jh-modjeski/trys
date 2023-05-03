from setuptools import setup, find_packages

setup(
    name="Trys",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'docopt',
        'halo',
        'pydub',
        'tqdm',
        'whisper'
    ],
    entry_points={
        'console_scripts': [
            'my-command=my_package.main:main',
        ],
    },
)
