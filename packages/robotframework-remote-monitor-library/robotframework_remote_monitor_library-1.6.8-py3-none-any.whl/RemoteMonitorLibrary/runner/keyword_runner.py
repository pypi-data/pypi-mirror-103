from typing import Any

from robot.libraries.BuiltIn import BuiltIn

from RemoteMonitorLibrary.model.runner_model import command_abstract


class KeywordRunner(command_abstract):

    def __init__(self, keyword, *args):
        self._keyword = keyword
        self._args = args

    @property
    def background(self):
        return False

    def __str__(self):
        return f"{self._keyword} {'  '.join(f'{a}' for a in self._args)}"

    def __call__(self, **kwargs) -> Any:
        BuiltIn().run_keyword(self._keyword, *list(list(self._args) + [f"{k}={v}" for k, v in kwargs.items()]))
