import unittest
from argparse import ArgumentParser
from unittest.mock import patch

from tests.harness import instrumentGooey


class TestGooeyDropdown(unittest.TestCase):

    def make_parser(self, **kwargs):
        parser = ArgumentParser(description='description')
        parser.add_argument('--dropdown', **kwargs)
        return parser


    @patch("gui.containers.application.seeder.fetchDynamicProperties")
    def test_dropdown_behavior(self, mock):
        """
        Testing that:
            - default values are used as the initial selection (when present)
            - Initial selection defaults to placeholder when no defaults supplied
            - selection is preserved (when possible) across dynamic updates
        """
        testcases = [
            # tuples of [choices, default, initalSelection, dynamicUpdate, expectedFinalSelection]
            [['1', '2'], None, 'Select Option', ['1', '2','3'], 'Select Option'],
            [['1', '2'], '2', '2', ['1', '2','3'],  '2'],
            [['1', '2'], '1', '1', ['1', '2','3'], '1'],
            # dynamic updates removed our selected value; defaults back to placeholder
            [['1', '2'], '2', '2', ['1', '3'], 'Select Option'],
        ]

        for choices, default, initalSelection, dynamicUpdate, expectedFinalSelection in testcases:
            parser = self.make_parser(choices=choices, default=default)
            with instrumentGooey(parser) as (app, gooeyApp):
                dropdown = gooeyApp.configs[0].reifiedWidgets[0]
                # ensure that default values (when supplied) are selected in the UI
                self.assertEqual(dropdown.widget.GetValue(), initalSelection)
                # fire a dynamic update with the mock values
                mock.return_value = {'--dropdown': dynamicUpdate}
                gooeyApp.fetchExternalUpdates()
                # the values in the UI now reflect those returned from the update
                # note: we're appending the ['select option'] bit here as it gets automatically added
                # in the UI.
                expectedValues = ['Select Option'] + dynamicUpdate
                self.assertEqual(dropdown.widget.GetItems(), expectedValues)
                # and our selection is what we expect
                self.assertEqual(dropdown.widget.GetValue(), expectedFinalSelection)


if __name__ == '__main__':
    unittest.main()