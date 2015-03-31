from setuptools import setup, find_packages

setup(
    name='fbfeeds',
    version='1.0',
    url='',
    license='BSD',
    description="A simple social post-feeds app (Facebook feed clone).",
    author='Aldwyn Cabarrubias',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=['setuptools'],
)
