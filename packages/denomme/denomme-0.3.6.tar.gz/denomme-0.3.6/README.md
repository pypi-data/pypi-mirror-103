<a href="https://github.com/meghanabhange/denomme"><img src="https://i.ibb.co/jwGVWPZ/rainbow-bohemian-logo-removebg-preview.png" width="125" height="125" align="right" /></a>

# dénommé : Multilingual Name Detection using spaCy v3
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/meghanabhange/denomme)](https://github.com/meghanabhange/denomme/releases)
[![PyPI](https://img.shields.io/pypi/v/denomme)](https://pypi.org/project/denomme/)
[![PyPI - License](https://img.shields.io/pypi/l/denomme)](https://pypi.org/project/denomme/)
[![Python application](https://github.com/meghanabhange/denomme/actions/workflows/python-app.yml/badge.svg)](https://github.com/meghanabhange/denomme/actions/workflows/python-app.yml)

### Supported Languages 
![](https://img.shields.io/badge/Lang-English-yellow) 
![](https://img.shields.io/badge/Lang-English(withIndianNames)-yellow) 
![](https://img.shields.io/badge/Lang-English(withArabicNames)-yellow) 
![](https://img.shields.io/badge/Lang-Arabic-yellow)

### Installation 

```
pip install denomme https://denomme.s3.us-east-2.amazonaws.com/xx_denomme-0.3.1/dist/xx_denomme-0.3.1.tar.gz
```


#### Using the denomme-pipe

```
from spacy.lang.xx import MultiLanguage
from denomme.name import person_name_component

nlp = MultiLanguage()
nlp.add_pipe("denomme")
doc = nlp("Hi my name is Meghana S.R Bhange and I want to talk Asha")
print(doc._.person_name)
```
