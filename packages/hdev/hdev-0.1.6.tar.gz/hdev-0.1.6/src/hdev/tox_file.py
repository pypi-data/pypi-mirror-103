"""Utilities for working with tox files."""

import warnings
from functools import lru_cache

_OLD_PIP_HINTS = (
    "tox-pip-extensions",
    "pip-tools<=5",
)


@lru_cache(1)
def requires_old_pip_tools(tox_file):
    """Get whether the provided tox file means we have to use old pip tools."""

    if not tox_file.exists():
        raise FileNotFoundError(tox_file)

    content = tox_file.read_text(encoding="utf-8")

    for hint in _OLD_PIP_HINTS:
        if hint in content:
            # This project uses tox-pip-extensions, so we must constrain
            # ourselves to a version of pip-tools < 5
            warnings.warn(
                "Support for 'tox-pip-extensions' will be dropped in future",
                DeprecationWarning,
            )
            return True

    # We can use any available version
    return False
