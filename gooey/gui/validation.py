from typing import Mapping

from gooey import Events
from gooey.python_bindings.types import Try
from gooey.util.functional import merge


def validateForm(self) -> Try[Mapping[str, str]]:  # or Exception
    config = self.navbar.getActiveConfig()
    localErrors: Mapping[str, str] = config.getErrors()
    dynamicResult: Try[Mapping[str, str]] = self.fetchDynamicValidations()

    combineErrors = lambda m: merge(localErrors, m)
    return dynamicResult.map(combineErrors)


def fetchDynamicValidations(self) -> Try[Mapping[str, str]]:
    # only run the dynamic validation if the user has
    # specifically subscribed to that event
    if Events.VALIDATE_FORM in self.buildSpec.get('use_events', []):
        cmd = self.getCommandDetails()
        return seeder.communicate2(cli.formValidationCmd(
            cmd.target,
            cmd.subcommand + 'baba',
            cmd.positionals,
            cmd.optionals
        ), self.buildSpec['encoding'])
    else:
        # shim response if nothing to do.
        return Success({})