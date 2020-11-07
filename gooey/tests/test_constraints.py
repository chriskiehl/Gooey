import unittest

from gooey import GooeyParser
from gooey.tests import *

class TestConstraints(unittest.TestCase):

    def test_listbox_constraints(self):
        """
        Listbox widgets must be provided a nargs option
        """

        # Trying to create a listbox widget without specifying nargs
        # throws an error
        with self.assertRaises(ValueError):
            parser = GooeyParser()
            parser.add_argument('one', choices=['one', 'two'], widget='Listbox')

        # Listbox with an invalid nargs value throws an error
        with self.assertRaises(ValueError):
            parser = GooeyParser()
            parser.add_argument(
                'one', choices=['one', 'two'], widget='Listbox', nargs='?')

        # Listbox with an invalid nargs value throws an error
        with self.assertRaises(ValueError):
            parser = GooeyParser()
            parser.add_argument(
                'one', choices=['one', 'two'], widget='Listbox', nargs=3)

        # valid nargs throw no errors
        for narg in ['*', '+']:
            parser = GooeyParser()
            parser.add_argument(
                'one', choices=['one', 'two'], widget='Listbox', nargs=narg)



    def test_visibility_constraint(self):
        """
        When visible=False in Gooey config, the user MUST supply either
        a custom validator or a default value.
        """
        # added without issue
        parser = GooeyParser()
        parser.add_argument('one')

        # still fine
        parser = GooeyParser()
        parser.add_argument('one', gooey_options={'visible': True})

        # trying to hide an input without a default or custom validator
        # results in an error
        with self.assertRaises(ValueError):
            parser = GooeyParser()
            parser.add_argument('one', gooey_options={'visible': False})

        # explicit default=None; still error
        with self.assertRaises(ValueError):
            parser = GooeyParser()
            parser.add_argument(
                'one',
                default=None,
                gooey_options={'visible': False})

        # default = empty string. Still error
        with self.assertRaises(ValueError):
            parser = GooeyParser()
            parser.add_argument(
                'one',
                default='',
                gooey_options={'visible': False})

        # default = valid string. No Error
        parser = GooeyParser()
        parser.add_argument(
            'one',
            default='Hello',
            gooey_options={'visible': False})

        # No default, but custom validator: Success
        parser = GooeyParser()
        parser.add_argument(
            'one',
            gooey_options={
                'visible': False,
                'validator': {'test': 'true'}
            })

        # default AND validator, still fine
        parser = GooeyParser()
        parser.add_argument(
            'one',
            default='Hai',
            gooey_options={
                'visible': False,
                'validator': {'test': 'true'}
            })