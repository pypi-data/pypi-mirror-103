import setuptools

setuptools.setup(
    name='mapon',
    version='0.0.9',
    description='A data wrangling tool',
    long_description=open('README.md').read(),
    author='nalssee',
    author_email='jinisrolling@gmail.com',
    url='https://github.com/nalssee/mapon.git',
    license='MIT',
    packages=setuptools.find_packages(),
    install_requires=[],
    include_package_data=True,
    package_data={'': ['*.txt']},
    zip_safe=False
)
