import unittest

from gooey import GooeyParser
from gooey.tests import *
from tests.harness import instrumentGooey


class TestRadioGroupBehavior(unittest.TestCase):


    def mutext_group(self, options):
        """
        Basic radio group consisting of two options.
        """
        parser = GooeyParser()
        group = parser.add_mutually_exclusive_group(**options)
        group.add_argument("-b", type=str)
        group.add_argument("-d", type=str, widget="DateChooser")
        return parser


    def test_initial_selection_options(self):
        """
        Ensure that the initial_selection GooeyOption behaves as expected.
        """
        # each pair in the below datastructure represents input/output
        # First position: kwargs which will be supplied to the parser
        # Second position: expected indices which buttons/widgets should be enabled/disabled
        testCases = [
            [{'required': True, 'gooey_options': {}},
             {'selected': None, 'enabled': [], 'disabled': [0, 1]}],

            # Issue #517 - initial section with required=True was not enabling
            # the inner widget
            [{'required': True, 'gooey_options': {"initial_selection": 0}},
             {'selected': 0, 'enabled': [0], 'disabled': [1]}],

            [{'required': True, 'gooey_options': {"initial_selection": 1}},
             {'selected': 1, 'enabled': [1], 'disabled': [0]}],

            [{'required': False, 'gooey_options': {}},
             {'selected': None, 'enabled': [], 'disabled': [0, 1]}],

            [{'required': False, 'gooey_options': {"initial_selection": 0}},
             {'selected': 0, 'enabled': [0], 'disabled': [1]}],

            [{'required': False, 'gooey_options': {"initial_selection": 1}},
             {'selected': 1, 'enabled': [1], 'disabled': [0]}],
        ]
        for options, expected in testCases:
            parser = self.mutext_group(options)
            with self.subTest(options):
                with instrumentGooey(parser) as (app, gooeyApp):
                    radioGroup = gooeyApp.configs[0].reifiedWidgets[0]

                    # verify that the checkboxes themselves are correct
                    if expected['selected'] is not None:
                        self.assertEqual(
                            radioGroup.selected,
                            radioGroup.radioButtons[expected['selected']])
                    else:
                        self.assertEqual(radioGroup.selected, None)

                    # verify the widgets contained in the radio group
                    # are in the correct state
                    for enabled in expected['enabled']:
                        # The widget contained within the group should be enabled
                        self.assertTrue(radioGroup.widgets[enabled].IsEnabled())

                    # make sure all widgets other than the selected
                    # are disabled
                    for enabled in expected['disabled']:
                        self.assertFalse(radioGroup.widgets[enabled].IsEnabled())


    def test_optional_radiogroup_click_behavior(self):
        """
        Testing that select/deselect behaves as expected
        """
        testcases = [
            self.click_scenarios_optional_widget(),
            self.click_scenarios_required_widget(),
            self.click_scenarios_initial_selection()
        ]

        for testcase in testcases:
            with self.subTest(testcase['name']):
                # wire up the parse with our test case options
                parser = self.mutext_group(testcase['input'])

                with instrumentGooey(parser) as (app, gooeyApp):
                    radioGroup = gooeyApp.configs[0].reifiedWidgets[0]

                    for scenario in testcase['scenario']:
                        targetButton = scenario['clickButton']

                        event = wx.CommandEvent(wx.wxEVT_LEFT_DOWN, wx.Window.NewControlId())
                        event.SetEventObject(radioGroup.radioButtons[targetButton])

                        radioGroup.radioButtons[targetButton].ProcessEvent(event)

                        expectedEnabled, expectedDisabled = scenario['postState']

                        for index in expectedEnabled:
                            self.assertEqual(radioGroup.selected, radioGroup.radioButtons[index])
                            self.assertTrue(radioGroup.widgets[index].IsEnabled())

                        for index in expectedDisabled:
                            self.assertNotEqual(radioGroup.selected, radioGroup.radioButtons[index])
                            self.assertFalse(radioGroup.widgets[index].IsEnabled())


    def click_scenarios_optional_widget(self):
        return {
            'name': 'click_scenarios_optional_widget',
            'input': {'required': False},
            'scenario': [
                # clicking enabled the button
                {'clickButton': 0,
                 'postState': [[0], [1]]},

                # clicking again disables the button (*when not required*)
                {'clickButton': 0,
                 'postState': [[], [0, 1]]},

                # clicking group 2 enabled it
                {'clickButton': 1,
                 'postState': [[1], [0]]},

                # and similarly clicking group 2 again disables it
                {'clickButton': 1,
                 'postState': [[], [0, 1]]},

                # enable second group
                {'clickButton': 1,
                 'postState': [[1], [0]]},

                # can switch to group one
                {'clickButton': 0,
                 'postState': [[0], [1]]},
            ]
        }

    def click_scenarios_required_widget(self):
        return {
            'name': 'click_scenarios_required_widget',
            'input': {'required': True},
            'scenario': [
                # clicking enables the button
                {'clickButton': 0,
                 'postState': [[0], [1]]},

                # unlike the the optional case, this
                # has no effect. You cannot _not_ select something
                # when it is required.
                {'clickButton': 0,
                 'postState': [[0], [1]]},

                # we can select a different button
                {'clickButton': 1,
                 'postState': [[1], [0]]},

                # again, if we click it again, we cannot deselect it
                {'clickButton': 1,
                 'postState': [[1], [0]]},

                # we can click back to the other group
                {'clickButton': 0,
                 'postState': [[0], [1]]},
            ]}

    def click_scenarios_initial_selection(self):
        return {
            'name': 'click_scenarios_initial_selection',
            'input': {'required': False, 'gooey_options': {'initial_selection': 0}},
            'scenario': [
                # we start already selected via GooeyOptions. As such,
                # clicking on the radiobutton should deselect it
                {'clickButton': 0,
                 'postState': [[], [0, 1]]},
                # clicking again reselected it
                {'clickButton': 0,
                 'postState': [[0], [1]]},
            ]}



if __name__ == '__main__':
    unittest.main()