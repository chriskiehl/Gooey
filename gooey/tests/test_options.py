import unittest

from gooey.gui.components.options import options

class TestPrefixFilter(unittest.TestCase):

    def test_doc_schenanigans(self):
        """Sanity check that my docstring wrappers all behave as expected"""
        @options._include_layout_docs
        def no_self_docstring():
            pass

        @options._include_layout_docs
        def yes_self_docstring():
            """sup"""
            pass

        # gets attached to functions even if they don't have a docstring
        self.assertIn(options.LayoutOptions.__doc__, no_self_docstring.__doc__)
        # gets attached to the *end* of existing doc strings
        self.assertTrue(yes_self_docstring.__doc__.startswith('sup'))
        self.assertIn(options.LayoutOptions.__doc__, yes_self_docstring.__doc__)


    def test_clean_method(self):
        """
        _clean should drop any keys with None values
        and flatten the layout_option kwargs to the root level
        """
        result = options._clean({'a': None, 'b': 123, 'c': 0})
        self.assertEqual(result, {'b': 123, 'c': 0})

        result = options._clean({'root_level': 123, 'layout_options': {
            'nested': 'hello',
            'another': 1234
        }})
        self.assertEqual(result, {'root_level': 123, 'nested': 'hello', 'another': 1234})

    def test_only_provided_arguments_included(self):
        """
        More sanity checking that the internal use of locals()
        does the Right Thing
        """
        option = options.LayoutOptions(label_color='#ffffff')
        self.assertIn('label_color', option)

        option = options.LayoutOptions()
        self.assertNotIn('label_color', option)

        option = options.TextField(label_color='#ffffff')
        self.assertIn('label_color', option)

        option = options.TextField()
        self.assertNotIn('label_color', option)