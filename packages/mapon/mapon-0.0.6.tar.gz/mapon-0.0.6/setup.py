import setuptools

setuptools.setup(
    name='mapon',
    version='0.0.6',
    description='A data wrangling tool',
    long_description=open('README.md').read(),
    author='nalssee',
    author_email='jinisrolling@gmail.com',
    url='https://github.com/nalssee/mapon.git',
    license='MIT',
    packages=setuptools.find_packages(),
    # Install statsmodels manually using conda install
    # TODO: Not easy to install numpy and stuff without conda
    install_requires=[
        'openpyxl>=2.5.12',
        'sas7bdat>=2.0.7',
        'psutil>=5.4.3',
        'graphviz>=0.8.2',
        'pathos>=0.2.2.1',
        'xlrd>=0.9.0',
        'more-itertools>=5.0.0',
        'coloredlogs>=10.0',
        'tqdm>=4.29.1',
         # 'statsmodels==0.10.1',
        'statsmodels',
        'pandas',
    ],
    include_package_data=True,
    package_data={'': ['*.txt']},
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
    ],
    zip_safe=False
)
