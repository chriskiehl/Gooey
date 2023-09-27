import argparse
import sys
import unittest
from argparse import ArgumentParser, FileType

from gooey import GooeyParser
from gooey.python_bindings import argparse_to_json
from gooey.util.functional import getin
from gooey.tests import *
from gooey.gui.components.options.options import FileChooser
from gooey.gui.components.widgets import FileSaver


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


    def test_suppress_is_removed_as_default_value(self):
        """
        Issue #469
        Argparse uses the literal string ==SUPPRESS== as an internal flag.
        When encountered in Gooey, these should be dropped and mapped to `None`.
        """
        parser = ArgumentParser(prog='test_program')
        parser.add_argument("--foo", default=argparse.SUPPRESS)
        parser.add_argument('--version', action='version', version='1.0')

        result = argparse_to_json.convert(parser, required_cols=2, optional_cols=2)
        groups = getin(result, ['widgets', 'test_program', 'contents'])
        for item in groups[0]['items']:
            self.assertEqual(getin(item, ['data', 'default']), None)


    def test_version_maps_to_checkbox(self):
        testcases = [
            [['--version'], {}, 'TextField'],
            # we only remap if the action is version
            # i.e. we don't care about the argument name itself
            [['--version'], {'action': 'store'}, 'TextField'],
            # should get mapped to CheckBox because of the action
            [['--version'], {'action': 'version'}, 'CheckBox'],
            # ditto, even through the 'name' isn't 'version'
            [['--foobar'], {'action': 'version'}, 'CheckBox'],
        ]
        for args, kwargs, expectedType in testcases:
            with self.subTest([args, kwargs]):
                parser = argparse.ArgumentParser(prog='test')
                parser.add_argument(*args, **kwargs)
                result = argparse_to_json.convert(parser, required_cols=2, optional_cols=2)
                contents = getin(result, ['widgets', 'test', 'contents'])[0]
                self.assertEqual(contents['items'][0]['type'], expectedType)


    def test_textinput_with_list_default_mapped_to_cli_friendly_value(self):
        """
        Issue: #500

        Using nargs and a `default` value with a list causes the literal list string
        to be put into the UI.
        """
        testcases = [
            {'nargs': '+', 'default': ['a b', 'c'], 'gooey_default': '"a b" "c"', 'w': 'TextField'},
            {'nargs': '*', 'default': ['a b', 'c'], 'gooey_default': '"a b" "c"', 'w': 'TextField'},
            {'nargs': '...', 'default': ['a b', 'c'], 'gooey_default': '"a b" "c"', 'w': 'TextField'},
            {'nargs': 2, 'default': ['a b', 'c'], 'gooey_default': '"a b" "c"', 'w': 'TextField'},
            # TODO: this demos the current nargs behavior for string defaults, but
            # TODO: it is wrong! These should be wrapped in quotes so spaces aren't
            # TODO: interpreted as unique arguments.
            {'nargs': '+', 'default': 'a b', 'gooey_default': 'a b', 'w': 'TextField'},
            {'nargs': '*', 'default': 'a b', 'gooey_default': 'a b', 'w': 'TextField'},
            {'nargs': '...', 'default': 'a b', 'gooey_default': 'a b', 'w': 'TextField'},
            {'nargs': 1, 'default': 'a b', 'gooey_default': 'a b', 'w': 'TextField'},

            # Listbox has special nargs handling which keeps the list in tact.
            {'nargs': '+', 'default': ['a b', 'c'], 'gooey_default': ['a b', 'c'], 'w': 'Listbox'},
            {'nargs': '*', 'default': ['a b', 'c'], 'gooey_default': ['a b', 'c'], 'w': 'Listbox'},
            {'nargs': '...', 'default': ['a b', 'c'], 'gooey_default': ['a b', 'c'],'w': 'Listbox'},
            {'nargs': 2, 'default': ['a b', 'c'], 'gooey_default': ['a b', 'c'], 'w': 'Listbox'},
            {'nargs': '+', 'default': 'a b', 'gooey_default': ['a b'], 'w': 'Listbox'},
            {'nargs': '*', 'default': 'a b', 'gooey_default': ['a b'], 'w': 'Listbox'},
            {'nargs': '...', 'default': 'a b', 'gooey_default': ['a b'], 'w': 'Listbox'},
            {'nargs': 1, 'default': 'a b', 'gooey_default': ['a b'], 'w': 'Listbox'},
        ]
        for case in testcases:
            with self.subTest(case):
                parser = ArgumentParser(prog='test_program')
                parser.add_argument('--foo', nargs=case['nargs'], default=case['default'])
                action = parser._actions[-1]
                result = argparse_to_json.handle_initial_values(action, case['w'], action.default)
                self.assertEqual(result, case['gooey_default'])

    def test_nargs(self):
        """
        so there are just a few simple rules here:
        if nargs in [*, N, +, remainder]:
            default MUST be a list OR we must map it to one

        action:_StoreAction
            - nargs '?'
                - default:validate list is invalid
                - default:coerce stringify
            - nargs #{*, N, +, REMAINDER}
                - default:validate None
                - default:coerce
                    if string: stringify
                    if list: convert from list to cli style input string
        action:_StoreConstAction
            - nargs: invalid
            - defaults:stringify

        action:{_StoreFalseAction, _StoreTrueAction}
            - nargs: invalid
            - defaults:validate: require bool
            - defaults:coerce: no stringify; leave bool

        action:_CountAction
            - nargs: invalid
            - default:validate: must be numeric index within range OR None
            - default:coerce: integer or None

        action:_AppendAction
            TODO: NOT CURRENTLY SUPPORTED BY GOOEY
            nargs behavior is weird and needs to be understood.
            - nargs

        action:CustomUserAction:
            - nargs: no way to know expected behavior. Ignore
            - default: jsonify type if possible.
        """

        parser = ArgumentParser()
        parser.add_argument(
            '--bar',
            nargs='+',
            choices=["one", "two"],
            default="one",
        )


    def test_filetype_chooses_good_widget(self):
        """
        #743 chose the picker type based on the FileType mode
        when available.
        """
        cases = [
            (FileType(), 'FileChooser'),
            (FileType('r'), 'FileChooser'),
            (FileType('rb'), 'FileChooser'),
            (FileType('rt'), 'FileChooser'),
            (FileType('w'), 'FileSaver'),
            (FileType('wt'), 'FileSaver'),
            (FileType('wb'), 'FileSaver'),
            (FileType('a'), 'FileSaver'),
            (FileType('x'), 'FileSaver'),
            (FileType('+'), 'FileSaver'),
        ]

        for filetype, expected_widget in cases:
            with self.subTest(f'expect {filetype} to produce {expected_widget})'):
                parser = ArgumentParser()
                parser.add_argument('foo', type=filetype)
                action = [parser._actions[-1]]
                result = next(argparse_to_json.categorize(action, {}, {}))
                self.assertEqual(result['type'], expected_widget)


    def test_nargs_with_choices_chooses_good_widget(self):
        """
        #763 argument with nargs in {+, *} and a list of choices should use
        a Listbox widget
        """
        cases = ['*', '+']

        for nargs in cases:
            with self.subTest(f'expect {nargs} to produce a Listbox'):
                parser = ArgumentParser()
                parser.add_argument('foo', nargs=nargs, choices=['choice', 'choice1'])
                action = [parser._actions[-1]]
                result = next(argparse_to_json.categorize(action, {}, {}))
                self.assertEqual(result['type'], 'Listbox')

