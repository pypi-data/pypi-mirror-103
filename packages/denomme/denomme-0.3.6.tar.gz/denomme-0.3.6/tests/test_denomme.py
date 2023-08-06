import unittest
from pathlib import Path
from denomme.name import person_name_component
from spacy.lang.xx import MultiLanguage

class TestPersonName(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.nlp = MultiLanguage()
        self.nlp.add_pipe("denomme")

    def test_single_name(self):
        doc = self.nlp("Hi my name is Meghana S.R Bhange")
        self.assertListEqual([name.text for name in doc._.person_name], ["Meghana S.R Bhange"])
    
    def test_single_word_names(self):
        doc = self.nlp("Meghana")
        self.assertListEqual([name.text for name in doc._.person_name], ["Meghana"])


    def test_two_names(self):
        doc = self.nlp("Hi my name is Meghana S.R Bhange and I want to talk to Ketaki Ambadkar")
        self.assertListEqual([name.text for name in doc._.person_name], ["Meghana S.R Bhange", "Ketaki Ambadkar"])
    
    def test_no_names(self):
        doc = self.nlp("Hi, I want to talk to someone?")
        self.assertListEqual([name.text for name in doc._.person_name], [])

    def test_city_names(self):
        doc = self.nlp("Hi, I want to book a flight to London")
        self.assertListEqual([name.text for name in doc._.person_name], [])
        
    @classmethod
    def tearDownClass(self):
        pass