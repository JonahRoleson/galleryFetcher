#!/usr/bin/env python
import os
import sys
# compatibility shim for packages that expect collections.Hashable etc.
import collections
import collections.abc as _abc

# Only set if missing so we don't override modern behavior
if not hasattr(collections, "Hashable"):
    collections.Hashable = _abc.Hashable
if not hasattr(collections, "Iterable"):
    collections.Iterable = _abc.Iterable
if not hasattr(collections, "Mapping"):
    collections.Mapping = _abc.Mapping

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Make sure it's installed and available on your PYTHONPATH."
        ) from exc
    execute_from_command_line(sys.argv)

