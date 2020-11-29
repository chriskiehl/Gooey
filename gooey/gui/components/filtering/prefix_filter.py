import re

import pygtrie as trie
from functools import reduce

__ALL__ = ('PrefixTokenizers', 'PrefixSearch')



class PrefixTokenizers:
    # This string here is just an arbitrary long string so that
    # re.split finds no matches and returns the entire phrase
    ENTIRE_PHRASE = '::gooey/tokenization/entire-phrase'
    # \s == any whitespace character
    WORDS = r'\s'

    @classmethod
    def REGEX(cls, expression):
        return expression

class OperatorType:
    AND = 'AND'
    OR = 'OR'

class SearchOptions:
    def __init__(self,
                 choice_tokenizer=PrefixTokenizers.ENTIRE_PHRASE,
                 input_tokenizer=PrefixTokenizers.ENTIRE_PHRASE,
                 ignore_case=True,
                 operator='AND',
                 index_suffix= False,
                 **kwargs):
        self.choice_tokenizer = choice_tokenizer
        self.input_tokenizer = input_tokenizer
        self.ignore_case = ignore_case
        self.operator = operator
        self.index_suffix = index_suffix



class PrefixSearch(object):
    """
    A trie backed index for quickly finding substrings
    in a list of options.
    """

    def __init__(self, choices, options={}, *args, **kwargs):
        self.choices = sorted(filter(None, choices))
        self.options: SearchOptions = SearchOptions(**options)
        self.searchtree = self.buildSearchTrie(choices)

    def updateChoices(self, choices):
        self.choices = sorted(filter(None, choices))
        self.searchtree = trie.Trie()

    def findMatches(self, token):
        if not token:
            return sorted(self.choices)
        tokens = self.tokenizeInput(token)
        matches = [set(flatten(self._vals(self.searchtree, prefix=t))) for t in tokens]
        op = intersection if self.options.operator == 'AND' else union
        return sorted(reduce(op, matches))

    def tokenizeInput(self, token):
        """
        Cleans and tokenizes the user's input.

        empty characters and spaces are trimmed to prevent
        matching all paths in the index.
        """
        return list(filter(None, re.split(self.options.input_tokenizer, self.clean(token))))

    def tokenizeChoice(self, choice):
        """
        Splits the `choice` into a series of tokens based on
        the user's criteria.

        If suffix indexing is enabled, the individual tokens
        are further broken down and indexed by their suffix offsets. e.g.

            'Banana', 'anana', 'nana', 'ana'
        """
        choice_ = self.clean(choice)
        tokens = re.split(self.options.choice_tokenizer, choice_)
        if self.options.index_suffix:
            return [token[i:]
                    for token in tokens
                    for i in range(len(token) - 2)]
        else:
            return tokens

    def clean(self, text):
        return text.lower() if self.options.ignore_case else text

    def buildSearchTrie(self, choices):
        searchtrie = trie.Trie()
        for choice in choices:
            for token in self.tokenizeChoice(choice):
                if not searchtrie.has_key(token):
                    searchtrie[token] = []
                searchtrie[token].append(choice)
        return searchtrie

    def _vals(self, searchtrie, **kwargs):
        try:
            return searchtrie.values(**kwargs)
        except KeyError:
            return []


def intersection(a, b):
    return a.intersection(b)


def union(a, b):
    return a.union(b)


def flatten(xs):
    return [item for x in xs for item in x]
