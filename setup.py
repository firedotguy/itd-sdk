from setuptools import setup, find_packages

version = '1.0.0'

setup(
    name='itd-iter-api',
    version=version,
    packages=find_packages(),
    install_requires=[
        'requests', 'DrissionPage', 'verboselogs'
    ],
    python_requires=">=3.9"
)
