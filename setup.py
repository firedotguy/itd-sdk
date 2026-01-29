from setuptools import setup, find_packages

setup(
    name='itd-sdk',
    version='0.2.0',
    packages=find_packages(),
    install_requires=[
        'requests'
    ],
    python_requires=">=3.9"
)
