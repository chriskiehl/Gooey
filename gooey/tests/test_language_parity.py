import os
import unittest
import json
from collections import OrderedDict
from gooey import languages

from gooey.gui.processor import ProcessController


class TestLanguageParity(unittest.TestCase):
    """
    Checks that all language files have the same set of keys so that non-english
    languages don't silently break as features are added to Gooey.
    """

    def test_languageParity(self):
        langDir = os.path.dirname(languages.__file__)
        englishFile = os.path.join(langDir, 'english.json')

        english = self.readFile(englishFile)
        jsonFiles = [(path, self.readFile(os.path.join(langDir, path)))
                      for path in os.listdir(langDir)
                      if path.endswith('json') and 'poooo' not in path and '2' not in path]

        allKeys = set(english.keys())
        for name, contents in jsonFiles:
            missing = allKeys.difference(set(contents.keys()))
            self.assertEqual(
                set(),
                missing,
                "{} language file is missing keys: [{}]".format(name, missing)
            )


    def readFile(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.loads(f.read())


if __name__ == '__main__':
    unittest.main()
