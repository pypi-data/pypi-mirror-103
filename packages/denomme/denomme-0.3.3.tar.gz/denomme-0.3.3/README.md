<a href="https://explosion.ai"><img src="https://i.ibb.co/jwGVWPZ/rainbow-bohemian-logo-removebg-preview.png" width="125" height="125" align="right" /></a>

# dénommé : Multilingual Name Detection using spaCy v3
![GitHub release (latest by date)](https://img.shields.io/github/v/release/meghanabhange/denomme) 
![PyPI](https://img.shields.io/pypi/v/denomme)

### Supported Languages ![](https://img.shields.io/badge/Lang-English-yellow)  ![](https://img.shields.io/badge/Lang-Arabic-yellow)

### Installation 

```
pip install https://denomme.s3.us-east-2.amazonaws.com/xx_denomme-0.3.1/dist/xx_denomme-0.3.1.tar.gz
pip install denomme
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
