"""Infer parser from type hints."""

from functools import wraps
from math import inf
import shlex
import types
import typing
from typing import Any, Callable, Dict, Iterable, List, Tuple, Union


class CantParse(Exception):
    """Returned by wrapped parsers."""


class CantInfer(Exception):
    """Returned by infer."""
    def __call__(self, _: str) -> CantParse:
        """Callable so that infer result is always callable."""
        return CantParse(0)


Parser = Callable[[str], Union[Any, CantParse]]


def wrap(parser: Parser) -> Parser:
    """Wrap parser to return CantParse on error."""
    @wraps(parser)
    def wrapper(string: str) -> Union[Any, CantParse]:
        try:
            return parser(string)
        except Exception:  # pylint: disable=broad-except
            return CantParse()
    return wrapper


def make_union_parser(*args: Parser) -> Parser:
    """Create parser that tries each parser in args one by one."""
    def union_parser(string: str) -> Union[Any, CantParse]:
        for parse in args:
            result = parse(string)
            if not isinstance(result, CantParse):
                return result
        return CantParse()
    return union_parser


ParseEllipsis = wrap(str)  # Used to identify ... from infer result


def make_variable_length_tuple_parser(parse: Parser) -> Parser:
    """Create shell string to variable-length tuple parser."""
    def variable_length_tuple_parser(string: str
                                     ) -> Union[Tuple[Any, ...], CantParse]:
        result = tuple(map(parse, shlex.split(string)))
        if any(isinstance(r, CantParse) for r in result):
            return CantParse()
        return result
    return variable_length_tuple_parser


def make_fixed_length_tuple_parser(*args: Parser) -> Parser:
    """Create shell string to fixed-length tuple parser."""
    def tuple_parser(string: str) -> Union[Tuple[Any, ...], CantParse]:
        strings = shlex.split(string)
        if len(strings) != len(args):
            return CantParse()
        result = tuple(parse(s) for parse, s in zip(args, strings))
        if any(isinstance(r, CantParse) for r in result):
            return CantParse()
        return result
    return tuple_parser


def make_tuple_parser(*args: Parser) -> Union[Parser, CantInfer]:
    """Create shell string to tuple parser."""
    if ParseEllipsis in args:
        if len(args) != 2:
            return CantInfer()
        if args[0] is ParseEllipsis:
            return CantInfer()
        return make_variable_length_tuple_parser(args[0])
    return make_fixed_length_tuple_parser(*args)


def make_list_parser(*args: Parser) -> Union[Parser, CantInfer]:
    """Create shell string to list parser."""
    if len(args) != 1:
        return CantInfer()
    parse = args[0]

    def list_parser(string: str) -> Union[List[Any], CantParse]:
        result = [parse(s) for s in shlex.split(string)]
        if any(isinstance(r, CantParse) for r in result):
            return CantParse()
        return result
    return list_parser


def make_dict_parser(*args: Parser) -> Union[Parser, CantInfer]:
    """Create shell string to dict parser."""
    if len(args) != 2:
        return CantInfer()
    parse_key, parse_val = args

    def dict_parser(string: str) -> Union[Dict[Any, Any], CantParse]:
        keys: List[Any] = []
        vals: List[Any] = []
        for i, token in enumerate(shlex.split(string)):
            item = (parse_key, parse_val)[i % 2](token)
            (keys, vals)[i % 2].append(item)
            if isinstance(item, CantParse):
                return item
        if len(keys) != len(vals):
            return CantParse()
        return dict(zip(keys, vals))
    return dict_parser


def parse_none(string: str) -> Union[None, CantParse]:
    """Parse '' or 'None' to None."""
    if string in ("", "None"):
        return None
    return CantParse()


def parse_bool(string: str) -> Union[bool, CantParse]:
    """Parse '', 'true', 'false', 'True', 'False', '0' and '1'."""
    if string in ("true", "True", "1"):
        return True
    if string in ("false", "False", "", "0"):
        return False
    return CantParse()


def is_none(hint: Any) -> bool:
    """Check if hint is None."""
    if hint is None:
        return True
    try:
        return isinstance(None, hint)
    except TypeError:
        return False


def map_infer_length(hints: Iterable[Any],
                     allow_ellipsis: bool = False
                     ) -> Union[List[Union[int, float]], CantInfer]:
    """Map infer_length on hints."""
    lengths = []
    for hint in hints:
        length = infer_length(hint)
        if isinstance(length, CantInfer):
            return length
        if not allow_ellipsis and hint is ...:
            return CantInfer()
        lengths.append(length)
    return lengths


def is_generic_alias(hint: Any) -> bool:
    """Check if type hint is a generic alias (e.g. tuple[int], etc.).

    This function is used to support python 3.8.
    """
    if not hasattr(types, "GenericAlias"):
        return False
    return isinstance(hint, getattr(types, "GenericAlias"))


def get_annotated_origin() -> Any:
    """Return typing.Annotated if available or object."""
    if hasattr(typing, "Annotated"):
        return getattr(typing, "Annotated")
    return object()


def get_final_origin() -> Any:
    """Return typing.Final if available or object.

    This function is needed to support python 3.7.
    """
    if hasattr(typing, "Final"):
        return getattr(typing, "Final")
    return object()


def get_literal_origin() -> Any:
    """Return typing.Literal if available or object.

    This function is needed to support python 3.7.
    """
    if hasattr(typing, "Literal"):
        return getattr(typing, "Literal")
    return object()


def get_origin(hint: Any) -> Any:
    """typing.get_origin wrapper to support python 3.7."""
    if hasattr(typing, "get_origin"):
        return getattr(typing, "get_origin")(hint)
    try:
        return hint.__origin__
    except AttributeError:
        return None


def get_args(hint: Any) -> Any:
    """typing.get_args wrapper to support python 3.7."""
    if hasattr(typing, "get_args"):
        return getattr(typing, "get_args")(hint)
    try:
        return hint.__args__
    except AttributeError:
        return ()


def infer(hint: Any) -> Union[Parser, CantInfer]:
    """Infer parser from type hint.

    Returns CantInfer on failure.
    """
    # pylint: disable=too-many-return-statements
    if isinstance(infer_length(hint), CantInfer):
        return CantInfer()

    if hint == ...:
        return ParseEllipsis
    if is_none(hint):
        return parse_none
    if hint == bool:
        return parse_bool
    if type(hint) == type and not is_generic_alias(hint):  # pylint: disable=unidiomatic-typecheck; # noqa: E501
        return wrap(hint)

    origin = get_origin(hint)  # See help(get_args) for supported types.
    args = get_args(hint)
    parsers = [infer(parser) for parser in args]

    return (
        make_tuple_parser(*parsers) if origin in (tuple, typing.Tuple) else
        make_list_parser(*parsers) if origin in (list, typing.List) else
        make_dict_parser(*parsers) if origin in (dict, typing.Dict) else
        CantInfer(hint) if origin is get_literal_origin() else
        parsers[0] if origin in (
            get_final_origin(),
            get_annotated_origin()) else
        make_union_parser(*parsers) if origin is typing.Union else
        CantInfer(hint)
    )


def infer_length(hint: Any) -> Union[int, float, CantInfer]:
    """Return max number of items in a 'flattened' list."""
    origin = get_origin(hint)
    args = get_args(hint)
    if origin is None:
        return 1

    assert len(args) > 0
    allow_ellipsis = origin in (tuple, typing.Tuple)
    lengths = map_infer_length(args, allow_ellipsis=allow_ellipsis)
    if isinstance(lengths, CantInfer):
        return lengths

    return (
        lengths[0] if origin in (get_annotated_origin(), get_final_origin())
        else
        max(lengths) if origin is Union else
        sum(lengths) if origin in (tuple, Tuple) and ... not in args else
        (CantInfer() if inf in lengths else inf) if origin in
        (dict, typing.Dict, list, typing.List, tuple, typing.Tuple) else
        CantInfer()
    )
