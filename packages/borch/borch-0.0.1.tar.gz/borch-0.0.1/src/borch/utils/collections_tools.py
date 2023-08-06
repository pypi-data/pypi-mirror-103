"""
Tools for manipulating python collection objects.
"""
from collections import MutableMapping, OrderedDict
from typing import Any, Iterable, List, NamedTuple, Optional, Tuple

# def flatten(nested_dict: MutableMapping, parent_key: str = "", sep: str = "_") -> dict:
#     """Faltten a nested dictionary.
# 
#     Args:
#         nested_dict: a nested dictionary to flatten
#         parent_key: key to append to the name in the dict
#         sep: the seperator to use for the keys when flattening them
#     Returns:
#         a flat dictionary
#     """
#     items: List[Tuple[str, Any]] = []
#     for k, v in nested_dict.items():
#         new_key = parent_key + sep + k if parent_key else k
#         if isinstance(v, MutableMapping):
#             items.extend(flatten(v, new_key, sep=sep).items())
#         else:
#             items.append((new_key, v))
#     return dict(items)




# def invert_dictionary(dictionary: dict) -> dict:
#     """Reverses key-value pairs of a dictionary.
# 
#     Args:
#         dictionary: `dict` to reverse key-value pairs for.
# 
#     Returns:
#         A dictionary like ``dictionary`` but with key-value pairs reversed.
# 
#     Raises:
#         TypeError if any values were unhashable types.
#     """
#     return {v: k for k, v in dictionary.items()}


# def get_instance_indices(objects: Iterable, cls: type) -> tuple:
#     """Get the indices of objects that are instances of a particular class.
# 
#     Args:
#         objects: An iterable of objects.
#         cls: The class of interest to return indices of instances for.
# 
#     Returns:
#         A tuple of indices which correspond to elements in arg:`objects`
#         which are instances of arg:`cls`.
# 
#     Examples:
#         >>> my_list = [3, 4, 5.5, 6.6]
#         >>> get_instance_indices(my_list, int)
#         (0, 1)
#     """
#     return tuple(i for i, obj in enumerate(objects) if isinstance(obj, cls))
# 

# def dict_to_str(var):
#     """
#     Converts a dictionary to a nice string representation.
#     Args:
#         var (dict): dictionary to be converted to a string
# 
#     Returns:
#         a nicely formatted string with the contents of the var
#     """
#     return ", ".join("{!s} = {!r}".format(key, val) for key, val in var.items())


# def recursive_ordered_dict_to_dict(ordered_dict):
#     """
#     Converts nested OrderdDicts to dicts.
#     Args:
#         ordered_dict (OrderdDict): Nested orderd dicts
# 
#     Returns:
#         dict, all OrderdDicts converted to dicts
# 
#     Examples:
#         >>> ordered_dict = OrderedDict([('hej', OrderedDict([('test', 1)]))])
#         >>> recursive_ordered_dict_to_dict(ordered_dict)
#         {'hej': {'test': 1}}
#     """
#     simple_dict = {}
# 
#     for key, value in ordered_dict.items():
#         if isinstance(value, OrderedDict):
#             simple_dict[key] = recursive_ordered_dict_to_dict(value)
#         else:
#             simple_dict[key] = value
# 
#     return simple_dict
# 

# def namedtuple(
#     name: str,
#     fields: Iterable[Tuple[str, Any]],
#     *,
#     defaults: Optional[Tuple[Any]] = None,
# ) -> NamedTuple:
#     """A ``collections.namedtuple`` substitute which allows for: typing,
#     keyword-only arguments and getitem using field names.
# 
#     Args:
#         name: Name of the namedtuple class.
#         fields: Names and types for all fields.
#         defaults: Any defaults for fields, applied to the final fields.
# 
#     Examples:
#         >>> MyTuple = namedtuple("MyTuple", [("a", str), ("b", int)], defaults=(4,))
#         >>> MyTuple(a="hello")
#         MyTuple(a='hello', b=4)
#     """
#     nm_tpl = NamedTuple(name, fields)
#     if defaults is not None:
#         nm_tpl.__new__.__defaults__ = defaults
#     prev_geti = nm_tpl.__getitem__
# 
#     def _init(self, *args, **kwargs):  # pylint: disable=unused-argument
#         if args:
#             raise TypeError(f"{name} takes only keyword arguments")
# 
#     def _getitem(self, item):
#         if isinstance(item, str):
#             return prev_geti(self, self._fields.index(item))
#         return prev_geti(self, item)
# 
#     nm_tpl.__init__ = _init
#     nm_tpl.__getitem__ = _getitem
# 
#     return nm_tpl
