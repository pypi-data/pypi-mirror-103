from setuptools import setup
from ectyper import __version__

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ectyper',
    version=__version__,
    description='Escherichia coli fast serotyping using both raw reads and assemblies with automatic species identification',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/phac-nml/ecoli_serotyping',
    author='Chad Laing, Kyrylo Bessonov, Sam Sung, Camille La Rose, ',
    author_email='chad.laing@canada.ca, kyrylo.bessonov@canada.ca, sam.sung@canada.ca, claro100@uottawa.ca',
    license='Apache 2',
    scripts=['bin/ectyper'],
    packages=['ectyper'],
    install_requires=['requests','biopython','pandas'],
    package_data={'ectyper': ['Data/*.json', 'Data/*.py']},
    zip_safe=False,
    test_suite='py.test'
)

