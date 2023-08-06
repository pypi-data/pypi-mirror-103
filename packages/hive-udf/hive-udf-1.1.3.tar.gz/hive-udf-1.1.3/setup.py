import pathlib
from setuptools import setup, find_packages


HERE = pathlib.Path(__file__).parent
README = (HERE / 'README.md').read_text()

version = '1.1.3'

setup(
    name='hive-udf',
    version=version,
    description='Hive UDF (user defined functions)',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/zpz/hive-udf',
    license='MIT',
    python_requires='>=3.6',
    package_dir={'': 'src'},
    packages=['hive_udf'],
    include_package_data=True,
)
