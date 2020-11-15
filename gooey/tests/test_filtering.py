import unittest

from gooey import PrefixTokenizers
from gui.components.filtering.prefix_filter import SearchOptions, PrefixSearch
from collections import namedtuple

TestData = namedtuple('TestData', [
    'options',
    'input_string',
    'expected_results',
])

Places = namedtuple('Places', [
    'kabul',
    'tirana',
    'kyoto',
    'tokyo'
])

class TestPrefixFilter(unittest.TestCase):


    def setUp(self):
        self.testdata = Places(
            'Afghanistan Kabul',
            'Albania Tirana',
            'Japan Kyoto',
            'Japan Tokyo'
        )

    def test_prefix_searching(self):
        p = self.testdata
        cases = [
            TestData({'ignore_case': True}, 'a', [p.kabul, p.tirana]),
            TestData({'ignore_case': True}, 'A', [p.kabul, p.tirana]),
            TestData({'ignore_case': False}, 'a', []),
            TestData({'ignore_case': False}, 'A', [p.kabul, p.tirana]),

            # when using the phrase tokenizer, the search input must
            # match starting from the beginning. So we find Afghanistan
            TestData({'choice_tokenizer': PrefixTokenizers.ENTIRE_PHRASE}, 'Afghan', [p.kabul]),
            # but we cannot look up Kyoto because the phrase begins with "Japan"
            TestData({'choice_tokenizer': PrefixTokenizers.ENTIRE_PHRASE}, 'Kyoto', []),
            # So if we start with "Japan K" it'll be returned
            TestData({'choice_tokenizer': PrefixTokenizers.ENTIRE_PHRASE}, 'Japan K', [p.kyoto]),



            # word tokenizer will split on all whitespace and index
            # each choice one for each UNIQUE word
            # so passing in 'a' will match "Af" and "Al" as usual
            TestData({'choice_tokenizer': PrefixTokenizers.WORDS}, 'a', [p.kabul, p.tirana]),
            # but now we can also find Kyoto without prefixing "japan" as we'd
            # need to do with the phrase tokenizer
            TestData({'choice_tokenizer': PrefixTokenizers.WORDS}, 'kyo', [p.kyoto]),

            # if we tokenize the input, we're perform two searches against the index
            # The default operator is AND, which means all the words in your search
            # input must match the choice for it to count as as a hit.
            # In this example, we index the choices under PHRASE, but set the input
            # tokenizer to WORDS. Our input 'Japan K' gets tokenized to ['Japan', 'K']
            # There is no phrase which starts with Both "Japan" and "K" so we get no
            # matches returned
            TestData({'choice_tokenizer': PrefixTokenizers.ENTIRE_PHRASE,
                      'input_tokenizer': PrefixTokenizers.WORDS}, 'Japan K', []),
            # Tokenize the choices by WORDS means we can now filter on both words
            TestData({'choice_tokenizer': PrefixTokenizers.WORDS,
                      'input_tokenizer': PrefixTokenizers.WORDS}, 'Jap K', [p.kyoto]),
            # the default AND behavior can be swapped to OR to facilitate matching across
            # different records in the index.
            TestData({'choice_tokenizer': PrefixTokenizers.WORDS,
                      'input_tokenizer': PrefixTokenizers.WORDS,
                      'operator': 'OR'}, 'Kyo Tok', [p.kyoto, p.tokyo]),

            # Turning on Suffix indexing allow matching anywhere within a word.
            # Now 'kyo' will match both the beginning 'Kyoto' and substring 'ToKYO'
            TestData({'choice_tokenizer': PrefixTokenizers.WORDS,
                      'input_tokenizer': PrefixTokenizers.WORDS,
                      'index_suffix': True}, 'kyo ', [p.kyoto, p.tokyo]),

            TestData({'choice_tokenizer': PrefixTokenizers.WORDS,
                      'input_tokenizer': PrefixTokenizers.WORDS,
                      'index_suffix': True}, 'j kyo ', [p.kyoto, p.tokyo]),
        ]

        for case in cases:
            with self.subTest(case):
                searcher = PrefixSearch(self.testdata, case.options)
                result = searcher.findMatches(case.input_string)
                self.assertEqual(result, case.expected_results)


