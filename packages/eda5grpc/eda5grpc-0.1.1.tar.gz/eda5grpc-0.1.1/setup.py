from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="eda5grpc",
    version='0.1.1',
    description='Interface for gRPC communication',
    py_modules=[
        'client',
        'server',
        'game_state',
        'utils',
        'eda_games_pb2',
        'eda_games_pb2_grpc',
    ],
    package_dir={'': 'eda5grpc'},
    url='https://github.com/evbeda/edagames-grpc',
    author='Platform Team - EDA 5',
    author_email='ecrespillo@eventbrite.com',
    packages=[],
    python_requires='>=3.6',

    # requirements
    install_requires=[
        "grpcio==1.37.0",
        "protobuf==3.15.8",
    ],

    # LICENSE
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent"
    ],

    # README.md
    long_description=long_description,
    long_description_content_type="text/markdown",
)
