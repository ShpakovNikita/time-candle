from setuptools import setup, find_packages

setup(
    name='time_candle',
    version="0.2",
    license='MIT',
    description='little and unuseful time tracker',
    author='Paul Fon Boudervill',
    author_email='shpakovnikita1998@gmail.com',
    packages=find_packages(),
    include_package_data=False,
    install_requires=["peewee", "logging"],
    package_data={
        "time_candle": [
            "logging.conf",
            "config.ini",
        ]},
)
