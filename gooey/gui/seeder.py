"""
Util for talking to the client program in order to retrieve
dynamic defaults for the UI
"""
import json
import subprocess


def fetchDynamicProperties(target, encoding):
    """
    Sends a gooey-seed-ui request to the client program it retrieve
    dynamically generated defaults with which to seed the UI
    """
    # TODO: this needs to apply the same argpase_to_json data cleaning rules
    cmd = '{} {}'.format(target, 'gooey-seed-ui --ignore-gooey')
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    if proc.returncode != 0:
        out, _ = proc.communicate()
        return json.loads(out.decode(encoding))
    else:
        # TODO: useful feedback
        return {}

