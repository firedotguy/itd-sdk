from setuptools import setup, find_packages

setup(
    name='itd-sdk',
    version='1.2.0',
    packages=find_packages(),
    install_requires=[
        'requests', 'pydantic', 'sseclient-py'
    ],
    python_requires=">=3.9"
)
