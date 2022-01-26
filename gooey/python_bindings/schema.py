from typing import Dict, Any

from gooey.python_bindings.types import PublicGooeyState
from gooey.python_bindings import types as t


def validate_public_state(state: Dict[str, Any]) -> PublicGooeyState:
    """
    Very, very minimal validation the shape of the incoming state
    is inline with the PublicGooeyState type.

    TODO: turn this into something useful.
    """
    top_level_keys = PublicGooeyState.__annotations__.keys()
    assert set(top_level_keys) == set(state.keys())
    for item in state['active_form']:
        assert 'type' in item
        expected_keys = getattr(t, item['type']).__annotations__.keys()
        a = set(expected_keys)
        b = set(item.keys())
        assert set(expected_keys) == set(item.keys())
    return state
