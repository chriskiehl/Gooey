from collections import OrderedDict


def positional(actions):
    groups = OrderedDict([('Positional Arguments', []), ('Optional Arguments', [])])
    for action in actions:
        if action['group_name'] == 'Positional Arguments':
            groups['Positional Arguments'].append(action)
        else:
            groups['Optional Arguments'].append(action)
    return groups


def requiredAndOptional(actions):
    groups = OrderedDict([('Required', []), ('Optional', [])])
    for action in actions:
        if action['required']:
            groups['Required'].append(action)
        else:
            groups['Optional'].append(action)
    return groups


def argparseGroups(actions):
    groups = OrderedDict()
    for action in actions:
        if action['group_name'] not in groups:
            groups[action['group_name']] = []
        groups[action['group_name']].append(action)
    return groups
