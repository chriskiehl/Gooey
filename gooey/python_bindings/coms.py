"""
Because Gooey communicates with the host program
over stdin/out, we have to be able to differentiate what's
coming from gooey and structured, versus what is arbitrary
junk coming from the host's own logging.

To do this, we just prefix all written by gooey with the
literal string 'gooey::'. This lets us dig through all the
noisy stdout to find just the structured Gooey data we're
after.
"""

import json

prefix = 'gooey::'


def serialize_outbound(msg: str):
    """
    Attaches a prefix to whatever is about to be written
    to stdout so that we can differentiate it in the
    sea of other stdout writes
    """
    return prefix + msg


def deserialize_inbound(stdout: bytes, encoding):
    """
    Deserializes the incoming stdout payload after
    finding the relevant sections give the gooey prefix.
    e.g.
    std='foo\nbar\nstarting run\ngooey::{active_form: [...]}\n'
    => {active_form: [...]}
    """
    return json.loads(stdout.decode(encoding).split(prefix)[-1])
