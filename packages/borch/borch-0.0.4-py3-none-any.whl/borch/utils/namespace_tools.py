"""
Tools for programatically manipulating / adding to the namespace.
"""

import inspect
import sys


def get_subclass_members(module, parent):
    """Get the members of a module which are subclasses of `parent`, excluding
    `parent` itself.

    Args:
        module: The module to find classes within.
        parent: The parent class to search for subclasses of. NB `parent`
          itself will also be filtered out.

    Returns:
        A list of subclasses of `parent` exported from module `module`.
    """

    def _predicate(obj):
        try:
            return (
                issubclass(obj, parent)
                and obj is not parent
                and not obj.__name__.startswith("_")
            )
        except TypeError:
            return False

    return inspect.getmembers(module, _predicate)


def get_instances(module, instance):
    """Get the members of a module which are instances of `instance`.

    Args:
        module: The module to find instances within.
       instance: The parent class to search for subclasses of. NB `parent`
          itself will also be filtered out.

    Returns:
        A list of instances of `instance` exported from module `module`.
    """

    def _predicate(obj):
        return isinstance(obj, instance)

    return inspect.getmembers(module, _predicate)


def create_augmented_classes(
    caller: str, module: object, parent: type, class_factory: callable
) -> None:
    """Using `class_factory`, create modified classes of any subclasses of
    `parent` found in `module` and set them in the namespace of `caller`.

    Args:
        caller: The name of the caller module (available as `__name__`).
        module: The module to search for subclasses of `parent`.
        parent: The parent class for discovering classes to augment.
        class_factory: A callable which receives a class, performs operations
          with that class, then returns a new class.

    Notes:
        Type of `module` should be `module`, but this is not available through
        the builtins or `typing` library...
    """
    for _, cls in get_subclass_members(module, parent):
        setattr(sys.modules[caller], cls.__name__, class_factory(cls))
