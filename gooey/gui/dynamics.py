from typing import Any, Mapping

from gui import seeder


def update_form(form, cmd, encoding):
    output: Mapping[str, Any] = seeder.communicate(cmd, encoding)
    for k,v in output.items():
        if bool(v) and bool(v.strip()):
            pass


def known_keys(form, ff):
    pass
