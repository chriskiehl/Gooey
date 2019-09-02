import sys
import unittest
from argparse import ArgumentParser

from gooey import GooeyParser
from gooey.python_bindings import argparse_to_json
from gooey.util.functional import getin


class TestArgparse(unittest.TestCase):

    def test_mutex_groups_conversion(self):
        """
        Ensure multiple mutex groups are processed correctly.
        """
        parser = ArgumentParser()
        g1 = parser.add_mutually_exclusive_group(required=True)
        g1.add_argument('--choose1')
        g1.add_argument('--choose2')

        g2 = parser.add_mutually_exclusive_group(required=True)
        g2.add_argument('--choose3')
        g2.add_argument('--choose4')

        output = argparse_to_json.process(parser, {}, {}, {})

        # assert that we get two groups of two choices back
        items = output[0]['items']
        self.assertTrue(len(items) == 2)
        group1 = items[0]
        group2 = items[1]
        self.assertTrue(['--choose1'] in group1['data']['commands'])
        self.assertTrue(['--choose2'] in group1['data']['commands'])
        self.assertTrue(['--choose3'] in group2['data']['commands'])
        self.assertTrue(['--choose4'] in group2['data']['commands'])
        self.assertTrue(group1['type'] == 'RadioGroup')
        self.assertTrue(group2['type'] == 'RadioGroup')

    def test_json_iterable_conversion(self):
        """
        Issue #312 - tuples weren't being coerced to list during argparse
        conversion causing downstream issues when concatenating
        """
        # our original functionality accepted only lists as the choices arg
        parser = ArgumentParser()
        parser.add_argument("-foo", choices=['foo','bar', 'baz'])
        result = argparse_to_json.action_to_json(parser._actions[-1], "Dropdown", {})

        choices = result['data']['choices']
        self.assertTrue(isinstance(choices, list))
        self.assertEqual(choices, ['foo','bar', 'baz'])

        # Now we allow tuples as well.
        parser = ArgumentParser()
        parser.add_argument("-foo", choices=('foo','bar', 'baz'))
        result = argparse_to_json.action_to_json(parser._actions[-1], "Dropdown", {})

        choices = result['data']['choices']
        self.assertTrue(isinstance(choices, list))
        self.assertEqual(choices, ['foo','bar', 'baz'])


    def test_choice_string_cooersion(self):
        """
        Issue 321 - must coerce choice types to string to support wx.ComboBox
        """
        parser = ArgumentParser()
        parser.add_argument('--foo', default=1, choices=[1, 2, 3])
        choice_action = parser._actions[-1]
        result = argparse_to_json.action_to_json(choice_action, 'Dropdown', {})
        self.assertEqual(getin(result, ['data', 'choices']), ['1', '2', '3'])
        # default value is also converted to a string type
        self.assertEqual(getin(result, ['data', 'default']), '1')

    def test_choice_string_cooersion_no_default(self):
        """
        Make sure that choice types without a default don't create
        the literal string "None" but stick with the value None
        """
        parser = ArgumentParser()
        parser.add_argument('--foo', choices=[1, 2, 3])

        choice_action = parser._actions[-1]
        result = argparse_to_json.action_to_json(choice_action, 'Dropdown', {})
        self.assertEqual(getin(result, ['data', 'default']), None)
        

    def test_listbox_defaults_cast_correctly(self):
        """
        Issue XXX - defaults supplied in a list were turned into a string
        wholesale (list and all). The defaults should be stored as a list
        proper with only the _internal_ values coerced to strings.
        """
        parser = GooeyParser()
        parser.add_argument('--foo', widget="Listbox", nargs="*", choices=[1, 2, 3], default=[1, 2])

        choice_action = parser._actions[-1]
        result = argparse_to_json.action_to_json(choice_action, 'Listbox', {})
        self.assertEqual(getin(result, ['data', 'default']), ['1', '2'])


    def test_listbox_single_default_cast_correctly(self):
        """
        Single arg defaults to listbox should be wrapped in a list and
        their contents coerced as usual.
        """
        parser = GooeyParser()
        parser.add_argument('--foo', widget="Listbox",
                            nargs="*", choices=[1, 2, 3], default="sup")

        choice_action = parser._actions[-1]
        result = argparse_to_json.action_to_json(choice_action, 'Listbox', {})
        self.assertEqual(getin(result, ['data', 'default']), ['sup'])

    def test_non_data_defaults_are_dropped_entirely(self):
        """
        This is a refinement in understanding of Issue #147

        Caused by Issue 377 - passing arbitrary objects as defaults
        causes failures.
        """
        # passing plain data to cleaning function results in plain data
        # being returned
        data = ['abc',
                123,
                ['a', 'b'],
                [1, 2, 3]]

        for datum in data:
            result = argparse_to_json.clean_default(datum)
            self.assertEqual(result, datum)

        # passing in complex objects results in None
        objects = [sys.stdout, sys.stdin, object(), max, min]

        for obj in objects:
            result = argparse_to_json.clean_default(obj)
            self.assertEqual(result, None)


