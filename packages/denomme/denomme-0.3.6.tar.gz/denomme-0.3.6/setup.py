from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='denomme',
    version='0.3.6',    
    description="Name detection using spacy",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/meghanabhange/denomme.git",
    author='Meghana Bhange',
    author_email='meghanabhange@hey.com',
    license='MIT',
    packages=['denomme'],
    install_requires=['spacy==3.0.5',
                      'spacy-transformers==1.0.1',  
                      'sentencepiece==0.1.95',
                      ],
)
