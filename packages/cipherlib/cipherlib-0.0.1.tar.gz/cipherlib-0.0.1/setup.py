from setuptools import setup, find_packages

setup(
    name='cipherlib',
    version="0.0.1",
    description='Block Ciphers',
    python_requires='>=3.6',
    author='MIEM',
    author_email='n.yurasov@yahoo.com',
    license='MIT',
    package_data={
        'cipherlib': ['configs/logging_config.json'],
    },
    packages=find_packages(include=[
        'cipherlib', 'cipherlib.*'
    ]),
    url='https://github.com/NikitaYurasov/cipherlib',
    download_url='https://github.com/NikitaYurasov/cipherlib/archive/refs/tags/v0.0.1.tar.gz',
    include_package_data=True,
    zip_safe=False
)
