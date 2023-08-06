from setuptools import setup

setup(
    name='moj_pak',
    version='0.0.1',
    packages=['moj_pak'],
    install_requires=[
        'requests',
        'importlib; python_version == "2.6"',
    ],
    include_package_data=True,
)
