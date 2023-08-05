from setuptools import setup

setup(
    name='denomme',
    version='0.3.2',    
    description="Name detection using spacy",
    url="https://github.com/meghanabhange/denomme.git",
    author='Meghana Bhange',
    author_email='meghanabhange@hey.com',
    license='MIT',
    packages=['denomme'],
    install_requires=['spacy==3.0.5',
                      'spacy-transformers==1.0.1',  
                      'sentencepiece==0.1.95'
                      ],
     dependency_links=  [
                        'https://denomme.s3.us-east-2.amazonaws.com/xx_denomme-0.3.1/dist/xx_denomme-0.3.1.tar.gz'
                        ]
)
