"""Test infer_parser.py."""
# pylint: disable=unsubscriptable-object

from math import inf
from sys import version_info
import typing
from typing import Dict, List, Optional, Tuple, Union

import pytest

from infer_parser import (
    CantInfer,
    CantParse,
    infer,
    infer_length,
    parse_bool,
    parse_none,
)


def check_version(major: int, minor: int) -> bool:
    """Check python version."""
    return (version_info.major, version_info.minor) >= (major, minor)


def test_parse_none() -> None:
    """parse_none should parse '' and 'None' to None and nothing else."""
    assert parse_none("") is None
    assert parse_none("None") is None
    assert parse_none("none") is not None


def test_parse_bool() -> None:
    """parse_bool should parse only 'true', 'True', '1' to True."""
    truthy = ["true", "True", "1"]
    assert all(map(parse_bool, truthy))

    falsy = ["", "false", "False", "0"]
    assert not any(map(parse_bool, falsy))

    assert isinstance(parse_bool("TRue"), CantParse)
    assert isinstance(parse_bool("false "), CantParse)


def test_infer_none() -> None:
    """infer should return parse_none on None."""
    assert infer(None) is parse_none


def test_infer_bool() -> None:
    """infer should return parse_bool on bool."""
    assert infer(bool) is parse_bool


def test_infer_type() -> None:
    """infer should wrap basic and class types to return CantParse on error."""
    parse_float = infer(float)
    assert parse_float("1.5") == 1.5
    assert parse_float("9.0") == 9.0
    assert isinstance(parse_float("test"), CantParse)

    parse_int = infer(int)
    assert parse_int("-5") == -5
    assert parse_int("9002") == 9002
    assert isinstance(parse_int("0.0"), CantParse)


def test_infer_class_type() -> None:
    """infer should wrap custom types."""
    class Ok:  # pylint: disable=too-few-public-methods
        """Valid parser."""
        def __init__(self, arg: str):
            pass

    class Err:  # pylint: disable=too-few-public-methods
        """Invalid parser."""

    ok_ = infer(Ok)
    err = infer(Err)
    assert isinstance(ok_("test"), Ok)
    assert isinstance(err("test"), CantParse)


def test_infer_optional_type() -> None:
    """infer should work with optional types."""
    parse = infer(Optional[float])
    assert parse("1.5") == 1.5
    assert parse("") is None
    assert parse("None") is None
    assert parse("5") == 5.0


def test_infer_union_type() -> None:
    """infer should work with union types."""
    parse = infer(Union[float, bool])
    assert not parse("")
    assert not parse("false")
    assert not parse("False")
    assert parse("0") == 0.0
    assert parse("42") == 42.0
    assert isinstance(parse("e"), CantParse)

    zero = infer(Union[bool, float])("0")
    assert not zero
    assert isinstance(zero, bool)


@pytest.mark.skipif(not check_version(3, 8), reason="No typing.Final")
def test_infer_final_type() -> None:
    """infer should work with final types."""
    parse = infer(getattr(typing, "Final")[int])
    assert parse("17") == 17


@pytest.mark.skipif(not check_version(3, 9), reason="No typing.Annotated")
def test_infer_annotated_type() -> None:
    """infer should work with annotated types."""
    parse = infer(getattr(typing, "Annotated")[bool, None])
    assert parse("false") is False
    assert parse("True") is True


def test_infer_fixed_length_typing_tuple_type() -> None:
    """infer should work with fixed-length Tuple types."""
    parse = infer(Tuple[int, float])
    result = parse("5 5")
    assert isinstance(result, tuple)
    assert isinstance(result[0], int)
    assert isinstance(result[1], float)
    assert result == (5, 5.0)

    assert isinstance(parse("5"), CantParse)
    assert isinstance(parse("5.0 5"), CantParse)
    assert parse("  0  '1.5'   ") == (0, 1.5)

    assert infer(Tuple[bool, bool, bool])("True true 1") == \
        (True, True, True)


@pytest.mark.skipif(not check_version(3, 9), reason="No generic aliases")
def test_infer_fixed_length_tuple_type() -> None:
    """infer should work with fixed-length tuple types."""
    parse = infer(tuple[int, float])  # type: ignore
    result = parse("5 5")
    assert isinstance(result, tuple)
    assert isinstance(result[0], int)
    assert isinstance(result[1], float)
    assert result == (5, 5.0)

    assert isinstance(parse("5"), CantParse)
    assert isinstance(parse("5.0 5"), CantParse)
    assert parse("  0  '1.5'   ") == (0, 1.5)

    assert (True, True, True) == \
        infer(tuple[bool, bool, bool])("True true 1")  # type: ignore


def test_infer_variable_length_typing_tuple_type() -> None:
    """infer should work with variable-length Tuple types."""
    parse = infer(Tuple[float, ...])
    result = parse("0.0 1.1 2.2 '3.3'")

    assert isinstance(result, tuple)
    assert all(isinstance(r, float) for r in result)
    assert result == (0.0, 1.1, 2.2, 3.3)

    assert infer(Tuple[bool, ...])("true True 1") == (True, True, True)
    assert isinstance(infer(Tuple[int, ...])("1 2 3 four"), CantParse)


@pytest.mark.skipif(not check_version(3, 9), reason="No generic aliases")
def test_infer_variable_length_tuple_type() -> None:
    """infer should work with variable-length tuple types."""
    parse = infer(tuple[float, ...])  # type: ignore
    result = parse("0.0 1.1 2.2 '3.3'")

    assert isinstance(result, tuple)
    assert all(isinstance(r, float) for r in result)
    assert result == (0.0, 1.1, 2.2, 3.3)

    assert (True, True, True) == \
        infer(tuple[bool, ...])("true True 1")  # type: ignore
    parse = infer(tuple[int, ...])  # type: ignore
    assert isinstance(parse("1 2 3 four"), CantParse)

    assert isinstance(infer(tuple[...]), CantInfer)  # type: ignore
    assert isinstance(infer(tuple[..., int]), CantInfer)  # type: ignore
    assert isinstance(infer(tuple[int, float, ...]), CantInfer)  # type: ignore


def test_infer_typing_list_type() -> None:
    """infer should work with List types."""
    parse = infer(List[float])
    result = parse("0.0 1.1 2.2 '3.3'")

    assert isinstance(result, list)
    assert all(isinstance(r, float) for r in result)
    assert result == [0.0, 1.1, 2.2, 3.3]

    assert infer(List[bool])("true True 1") == [True, True, True]
    assert isinstance(infer(List[int])("1 2 3 four"), CantParse)


@pytest.mark.skipif(not check_version(3, 9), reason="No generic aliases")
def test_infer_list_type() -> None:
    """infer should work with list types."""
    parse = infer(list[float])  # type: ignore
    result = parse("0.0 1.1 2.2 '3.3'")

    assert isinstance(result, list)
    assert all(isinstance(r, float) for r in result)
    assert result == [0.0, 1.1, 2.2, 3.3]

    assert [True, True, True] == \
        infer(list[bool])("true True 1")  # type: ignore
    hint = list[int]  # type: ignore
    assert isinstance(infer(hint)("1 2 3 four"), CantParse)

    assert isinstance(infer(list[...]), CantInfer)  # type: ignore
    assert isinstance(infer(list[int, float]), CantInfer)  # type: ignore


def test_infer_typing_dict_type() -> None:
    """infer should work with Dict types."""
    parse = infer(Dict[str, float])
    result = parse("foo 1.0 bar 2.0")
    assert result == {"foo": 1.0, "bar": 2.0}

    assert infer(Dict[int, int])(" 1  2 '3' 4") == {1: 2, 3: 4}
    assert isinstance(infer(Dict[int, int])("1 2 3"), CantParse)
    assert isinstance(infer(Dict[str, float])("1 2 foo bar"), CantParse)


@pytest.mark.skipif(not check_version(3, 9), reason="No generic aliases")
def test_infer_dict_type() -> None:
    """infer should work with dict types."""
    parse = infer(dict[str, float])  # type: ignore
    result = parse("foo 1.0 bar 2.0")
    assert result == {"foo": 1.0, "bar": 2.0}

    assert infer(dict[int, int])(" 1  2 '3' 4") == {1: 2, 3: 4}  # type: ignore
    hint = dict[int, int]  # type: ignore
    assert isinstance(infer(hint)("1 2 3"), CantParse)
    hint = dict[str, float]  # type: ignore
    assert isinstance(infer(hint)("1 2 foo bar"), CantParse)

    assert isinstance(infer(dict[bool]), CantInfer)  # type: ignore
    assert isinstance(infer(dict[int, ...]), CantInfer)  # type: ignore
    assert isinstance(infer(dict[str, str, str]), CantInfer)  # type: ignore


@pytest.mark.skipif(not check_version(3, 8), reason="No typing.Final")
def test_infer_nested_type() -> None:
    """infer should work with nested types."""
    parse = infer(getattr(typing, "Final")[Union[Union[int, bool],
                                                 Optional[float]]])
    assert parse("19.5") == 19.5
    assert parse("false") is False
    assert parse("None") is None


def test_infer_fail() -> None:
    """infer should return CantInfer on failure."""
    assert isinstance(infer(typing.Any), CantInfer)
    assert isinstance(infer(typing.Callable[..., None]), CantInfer)


@pytest.mark.skipif(not check_version(3, 8), reason="No typing.Literal")
def test_infer_fail_literal() -> None:
    """infer does not support typing.Literal."""
    literal = getattr(typing, "Literal")
    assert isinstance(infer(Optional[literal[0, 1, 2]]), CantInfer)


def test_infer_fail_non_flattenable_types() -> None:
    """Type hints with ambiguous nargs should fail infer."""
    assert not isinstance(infer(List[int]), CantInfer)
    assert isinstance(infer(List[List[int]]), CantInfer)
    assert not isinstance(infer(Dict[Tuple[str], Tuple[int]]), CantInfer)

    hint = Dict[Tuple[str, ...], Tuple[int]]
    assert isinstance(infer(hint), CantInfer)
    assert isinstance(infer(Tuple[Dict[str, Dict[str, int]]]), CantInfer)

    hint = Tuple[Tuple[int, ...], ...]  # type: ignore
    assert isinstance(infer(hint), CantInfer)
    assert not isinstance(infer(Tuple[int, ...]), CantInfer)
    assert not isinstance(infer(Tuple[Tuple[str, int]]), CantInfer)


def test_infer_fail_call() -> None:
    """CantInfer objects CantParse."""
    parse = infer(typing.Any)
    assert isinstance(parse, CantInfer)
    assert isinstance(parse(""), CantParse)


def test_infer_length() -> None:
    """infer_length should return # of items in a shell string for the type."""
    assert infer_length(bool) == 1
    assert infer_length(int) == 1
    assert infer_length(Tuple[int, str, float]) == 3
    assert infer_length(Tuple[int, Tuple[int, Tuple[int, int]]]) == 4
    assert infer_length(Tuple[int, ...]) == inf
    assert infer_length(Dict[Tuple[int, str], str]) == inf
    assert infer_length(List[str]) == inf
    assert isinstance(infer_length(List[List[str]]), CantInfer)
    assert isinstance(infer_length(Dict[Tuple[int, ...], Dict[str, int]]),
                      CantInfer)
    assert infer_length(Optional[Tuple[int, float]]) == 2
    assert isinstance(infer_length(typing.Callable[..., int]), CantInfer)


@pytest.mark.skipif(not check_version(3, 9), reason="No typing.Annotated")
def test_infer_length_annotated_type() -> None:
    """infer_length should work with annotated types."""
    annotated = getattr(typing, "Annotated")
    assert infer_length(annotated[Tuple[str, str, str], None]) == 3


@pytest.mark.skipif(not check_version(3, 8), reason="No typing.Final")
def test_infer_length_final_type() -> None:
    """infer_length should work with final types."""
    final = getattr(typing, "Final")
    assert infer_length(final[List[int]]) == inf
