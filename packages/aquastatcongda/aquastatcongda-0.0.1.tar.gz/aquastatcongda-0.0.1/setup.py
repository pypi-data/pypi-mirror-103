import setuptools

setuptools.setup(
    name="aquastatcongda",
    version="0.0.1",
    author="Congda Xu",
    author_email="congdaxu2021@u.northwestern.edu",
    url="https://github.com/xcd1234/2021-msia423-Xu-Congda-assignment1",
    description="A Python package to deal with aquastat data",
    packages=setuptools.find_packages(where='src'),
    package_dir={'': 'src'},
    python_requires='>=3.6',
    install_requires=['pandas', 'numpy', 'matplotlib', 'seaborn', 'pytest'],
    data_files=[('my_data', ['data/aquastat.csv.gzip'])],
    license='MIT'
)