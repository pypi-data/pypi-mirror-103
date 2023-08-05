
dénommé : Multilingual Name Detection using spaCy v3
[image: https://img.shields.io/github/v/release/meghanabhange/denomme] [image: https://img.shields.io/pypi/v/denomme] [image: https://img.shields.io/pypi/l/denomme] 
Supported Languages [image: https://img.shields.io/badge/Lang-English-yellow] [image: https://img.shields.io/badge/Lang-Arabic-yellow]
Installation
pip install https://denomme.s3.us-east-2.amazonaws.com/xx_denomme-0.3.1/dist/xx_denomme-0.3.1.tar.gz
pip install denomme
Using the denomme-pipe
from spacy.lang.xx import MultiLanguage
from denomme.name import person_name_component

nlp = MultiLanguage()
nlp.add_pipe("denomme")
doc = nlp("Hi my name is Meghana S.R Bhange and I want to talk Asha")
print(doc._.person_name)
