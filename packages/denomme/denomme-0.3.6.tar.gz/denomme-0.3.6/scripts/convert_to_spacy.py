import json
import logging
import random
import re
import string
from collections import defaultdict
from pathlib import Path
from random import sample
from spacy.lang.xx import MultiLanguage
import fire
import pandas
import spacy
from spacy.tokens import DocBin, Span
from src import LOGGER
from tqdm import tqdm

LOGGER.info("Generate Sythetic Names")

nlp = MultiLanguage()


def convert(out_dir: Path, files: list):
    for f in files:
        output_filename = out_dir / f"{f.name[:-4]}.json"
        LOGGER.info(f"Saving in {output_filename}")
        all_sentences = f.open("r").read().split("\n\n")
        entity_tags = ("B-PER", "S-PER", "I-PER", "E-PER")
        spacy_sentence_data = []
        for sentence in tqdm(all_sentences):
            try:
                subwords = str(sentence).split("\n")
                entity_tag_relation = []
                sent = []
                for phrase in subwords:
                    texts = phrase.split(" ")
                    word = texts[0]
                    entity = texts[1]
                    sent.append(word)
                    if entity in entity_tags:
                        entity_tag_relation.append({word: entity})
                output_sentence = " ".join(sent)
                output_dict = {"entities": entity_tag_relation}
                spacy_sentence = [output_sentence, output_dict]
                spacy_sentence_data.append(spacy_sentence)
            except:
                pass
        json.dump(spacy_sentence_data, output_filename.open("w"), indent=2)


def convert_to_spacy_format(
    modified_ner_dir: str = "modified_wiki_ner",
    out_dir: str = "spacy_ner_data",
    data_path: str = "./assets",
):
    LOGGER.info(f"==========RECIEVED INPUT============")
    LOGGER.info(f"modified_ner_dir\t\t{modified_ner_dir}")
    LOGGER.info(f"out_dir Path\t\t{out_dir}")
    LOGGER.info(f"data_path\t\t{data_path}")
    LOGGER.info(f"====================================")
    data_path = Path(data_path)
    out_dir = data_path / out_dir
    modified_ner_dir_path = data_path / modified_ner_dir
    p = modified_ner_dir_path.glob("**/*.txt")
    files = [x for x in p if x.is_file()]
    LOGGER.info("======Found following files=====")
    for file in files:
        LOGGER.info(file)
    LOGGER.info("===============================")
    LOGGER.info("Converting to SpaCy Format...")
    convert(out_dir=out_dir, files=files)
    LOGGER.info("Done.")


if __name__ == "__main__":
    fire.Fire(convert_to_spacy_format)
