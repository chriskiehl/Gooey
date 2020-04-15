from argparse import ArgumentParser, _SubParsersAction
from argparse import _MutuallyExclusiveGroup, _ArgumentGroup
from textwrap import dedent


class GooeySubParser(_SubParsersAction):
    def __init__(self, *args, **kwargs):
        super(GooeySubParser, self).__init__(*args, **kwargs)


# TODO: figure out how to correctly dispatch all of these
#       so that the individual wrappers aren't needed
class GooeyArgumentGroup(_ArgumentGroup):
    def __init__(self, parser, widgets, options, *args, **kwargs):
        self.parser = parser
        self.widgets = widgets
        self.options = options
        super(GooeyArgumentGroup, self).__init__(self.parser, *args, **kwargs)

    def add_argument(self, *args, **kwargs):
        widget = kwargs.pop('widget', None)
        metavar = kwargs.pop('metavar', None)
        options = kwargs.pop('gooey_options', None)
        action = super(GooeyArgumentGroup, self).add_argument(*args, **kwargs)
        self.parser._actions[-1].metavar = metavar
        self.widgets[self.parser._actions[-1].dest] = widget
        self.options[self.parser._actions[-1].dest] = options
        return action

    def add_argument_group(self, *args, **kwargs):
        options = kwargs.pop('gooey_options', {})
        group = GooeyArgumentGroup(self.parser, self.widgets, self.options, *args, **kwargs)
        group.gooey_options = options
        self._action_groups.append(group)
        return group

    def add_mutually_exclusive_group(self, *args, **kwargs):
        options = kwargs.pop('gooey_options', {})
        container = self
        group = GooeyMutuallyExclusiveGroup(container, self.parser, self.widgets, self.options, *args, **kwargs)
        group.gooey_options = options
        self.parser._mutually_exclusive_groups.append(group)
        return group


class GooeyMutuallyExclusiveGroup(_MutuallyExclusiveGroup):
    def __init__(self, container, parser, widgets, options, *args, **kwargs):
        self.parser = parser
        self.widgets = widgets
        self.options = options
        super(GooeyMutuallyExclusiveGroup, self).__init__(container, *args, **kwargs)

    def add_argument(self, *args, **kwargs):
        widget = kwargs.pop('widget', None)
        metavar = kwargs.pop('metavar', None)
        options = kwargs.pop('gooey_options', None)
        super(GooeyMutuallyExclusiveGroup, self).add_argument(*args, **kwargs)
        self.parser._actions[-1].metavar = metavar
        self.widgets[self.parser._actions[-1].dest] = widget
        self.options[self.parser._actions[-1].dest] = options



class GooeyParser(object):
    def __init__(self, **kwargs):
        self.__dict__['parser'] = ArgumentParser(**kwargs)
        self.widgets = {}
        self.options = {}
        if 'parents' in kwargs:
            for parent in kwargs['parents']:
                if isinstance(parent, self.__class__):
                    self.widgets.update(parent.widgets)
                    self.options.update(parent.options)

    @property
    def _mutually_exclusive_groups(self):
        return self.parser._mutually_exclusive_groups

    @property
    def _actions(self):
        return self.parser._actions

    @property
    def description(self):
        return self.parser.description

    def add_argument(self, *args, **kwargs):
        widget = kwargs.pop('widget', None)
        metavar = kwargs.pop('metavar', None)
        options = kwargs.pop('gooey_options', None)

        action = self.parser.add_argument(*args, **kwargs)
        self.parser._actions[-1].metavar = metavar

        action_dest = self.parser._actions[-1].dest
        if action_dest not in self.widgets or self.widgets[action_dest] is None:
            self.widgets[action_dest] = widget

        if action_dest not in self.options or self.options[action_dest] is None:
            self.options[self.parser._actions[-1].dest] = options

        self._validate_constraints(
            self.parser._actions[-1],
            widget,
            options or {},
            **kwargs
        )
        return action

    def add_mutually_exclusive_group(self, *args, **kwargs):
        options = kwargs.pop('gooey_options', {})
        group = GooeyMutuallyExclusiveGroup(self, self.parser, self.widgets, self.options, *args, **kwargs)
        group.gooey_options = options
        self.parser._mutually_exclusive_groups.append(group)
        return group

    def add_argument_group(self, *args, **kwargs):
        options = kwargs.pop('gooey_options', {})
        group = GooeyArgumentGroup(self.parser, self.widgets, self.options, *args, **kwargs)
        group.gooey_options = options
        self.parser._action_groups.append(group)
        return group

    def parse_args(self, args=None, namespace=None):
        return self.parser.parse_args(args, namespace)

    def add_subparsers(self, **kwargs):
        if self._subparsers is not None:
            self.error(_('cannot have multiple subparser arguments'))

        # add the parser class to the arguments if it's not present
        kwargs.setdefault('parser_class', type(self))

        if 'title' in kwargs or 'description' in kwargs:
            title = kwargs.pop('title', 'subcommands')
            description = kwargs.pop('description', None)
            self._subparsers = self.add_argument_group(title, description)
        else:
            self._subparsers = self._positionals

        # prog defaults to the usage message of this parser, skipping
        # optional arguments and with no "usage:" prefix
        if kwargs.get('prog') is None:
            formatter = self._get_formatter()
            positionals = self._get_positional_actions()
            groups = self._mutually_exclusive_groups
            formatter.add_usage(self.usage, positionals, groups, '')
            kwargs['prog'] = formatter.format_help().strip()

        # create the parsers action and add it to the positionals list
        parsers_class = self._pop_action_class(kwargs, 'parsers')
        action = parsers_class(option_strings=[], **kwargs)
        self._subparsers._add_action(action)

        # return the created parsers action
        return action

    def _validate_constraints(self, parser_action, widget, options, **kwargs):
        from gooey.python_bindings import constraints
        constraints.assert_listbox_constraints(widget, **kwargs)
        constraints.assert_visibility_requirements(parser_action, options)



    def __getattr__(self, item):
        return getattr(self.parser, item)

    def __setattr__(self, key, value):
        return setattr(self.parser, key, value)
