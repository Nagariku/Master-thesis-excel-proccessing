from setuptools import setup, find_packages

setup(
    name='Master thesis excel proccessing',
    version='0.1.0',
    description='Project to allow for automated processing of files via config file and some slight user input',
    author='Grigorii Osipov',
    author_email='osipovgrisha.ru2@gmail.com',
    url='hhttps://github.com/grigsos/Master-thesis-excel-proccessing',
    packages=find_packages(),
    install_requires=[
        # list any dependencies your project requires here
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Engineers',
        'License :: GNU General Public License v3.0',
        'Programming Language :: Python :: 3.11.1',
    ],
)