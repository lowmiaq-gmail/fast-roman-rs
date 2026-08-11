import argparse
import importlib.util
from importlib import metadata
import inspect
import os
from pathlib import Path
import re
import subprocess
import sys
import sysconfig

import pytest

import roman as candidate


def load_oracle():
    path = Path(__file__).parents[1] / "upstream" / "oracle" / "roman" / "__init__.py"
    spec = importlib.util.spec_from_file_location("frozen_roman_oracle", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def public_names(module):
    return {name for name in vars(module) if not name.startswith("_")}


def test_public_surface_matches_oracle():
    oracle = load_oracle()
    assert public_names(candidate) == public_names(oracle)
    assert candidate.__doc__ == oracle.__doc__
    assert candidate.__author__ == oracle.__author__
    assert candidate.__copyright__ == oracle.__copyright__
    assert candidate.romanNumeralMap == oracle.romanNumeralMap
    assert type(candidate.romanNumeralMap) is tuple
    assert isinstance(candidate.romanNumeralPattern, re.Pattern)
    assert candidate.romanNumeralPattern.pattern == oracle.romanNumeralPattern.pattern
    assert candidate.romanNumeralPattern.flags == oracle.romanNumeralPattern.flags == 96
    assert candidate.romanNumeralPattern.groups == oracle.romanNumeralPattern.groups == 3
    assert candidate.romanNumeralPattern.groupindex == oracle.romanNumeralPattern.groupindex == {}
    assert candidate.argparse is argparse
    assert candidate.re is re
    assert candidate.sys is sys


@pytest.mark.parametrize("name", ["toRoman", "fromRoman", "parse_args", "main"])
def test_function_introspection_matches_oracle(name):
    oracle = load_oracle()
    actual = getattr(candidate, name)
    expected = getattr(oracle, name)
    assert inspect.signature(actual) == inspect.signature(expected)
    assert actual.__name__ == expected.__name__
    assert actual.__qualname__ == expected.__qualname__
    assert actual.__module__ == "roman"
    assert actual.__doc__ == expected.__doc__
    assert actual.__annotations__ == expected.__annotations__
    assert actual.__defaults__ == expected.__defaults__
    assert actual.__kwdefaults__ == expected.__kwdefaults__


def test_exception_hierarchy_and_modules():
    assert candidate.RomanError.__bases__ == (Exception,)
    for name in ("OutOfRangeError", "NotIntegerError", "InvalidRomanNumeralError"):
        cls = getattr(candidate, name)
        assert cls.__bases__ == (candidate.RomanError,)
        assert cls.__module__ == "roman"


def test_complete_integer_domain_round_trip():
    assert candidate.toRoman(False) == "N"
    assert candidate.toRoman(True) == "I"
    for value in range(5000):
        numeral = candidate.toRoman(value)
        assert isinstance(numeral, str)
        assert candidate.fromRoman(numeral) == value


@pytest.mark.parametrize(
    ("value", "error", "message"),
    [
        (-1, "OutOfRangeError", "number out of range (must be 0..4999)"),
        (5000, "OutOfRangeError", "number out of range (must be 0..4999)"),
        (1.0, "NotIntegerError", "decimals cannot be converted"),
        ("1", "NotIntegerError", "decimals cannot be converted"),
        (None, "NotIntegerError", "decimals cannot be converted"),
    ],
)
def test_to_roman_error_contract(value, error, message):
    with pytest.raises(getattr(candidate, error), match=re.escape(message)) as captured:
        candidate.toRoman(value)
    assert str(captured.value) == message


@pytest.mark.parametrize(
    ("value", "special", "expected"),
    [
        ("n", True, 0),
        ("N", "yes", 0),
        ("i", False, 1),
        ("MMMMCMXCIX", True, 4999),
        ("I\n", True, 1),
        ("\n", True, 0),
    ],
)
def test_from_roman_boundaries(value, special, expected):
    assert candidate.fromRoman(value, special) == expected


@pytest.mark.parametrize("value", ["", None, False, 0, []])
def test_falsy_input_uses_blank_error(value):
    with pytest.raises(candidate.InvalidRomanNumeralError) as captured:
        candidate.fromRoman(value)
    assert str(captured.value) == "Input cannot be blank"


@pytest.mark.parametrize("value", ["N", "IIII", "MMMMM", "I\r\n", " N "])
def test_invalid_roman_message_uses_uppercased_input(value):
    with pytest.raises(candidate.InvalidRomanNumeralError) as captured:
        candidate.fromRoman(value, False)
    assert str(captured.value) == "Invalid Roman numeral: %s" % value.upper()


def test_dynamic_upper_protocol_matches_upstream():
    class UpperReturns:
        def __bool__(self):
            return True

        def upper(self):
            return "X"

    assert candidate.fromRoman(UpperReturns()) == 10
    with pytest.raises(TypeError, match="string pattern"):
        candidate.fromRoman(b"I")


def test_distribution_typing_and_console_script():
    distribution = metadata.distribution("fast-roman-rs")
    entries = [entry for entry in distribution.entry_points if entry.group == "console_scripts"]
    assert [(entry.name, entry.value) for entry in entries] == [("roman", "roman:main")]
    assert any(str(path) == "roman/py.typed" for path in distribution.files or [])
    executable = Path(sysconfig.get_path("scripts")) / (
        "roman.exe" if os.name == "nt" else "roman"
    )
    assert executable.is_file()
    assert subprocess.run([executable, "972"], text=True, capture_output=True).stdout == "CMLXXII\n"
    reverse = subprocess.run([executable, "-r", "cMlxxii"], text=True, capture_output=True)
    assert reverse.returncode == 0
    assert reverse.stdout == "972\n"
    assert reverse.stderr == ""


def test_python_module_entry_remains_absent():
    completed = subprocess.run(
        [sys.executable, "-m", "roman"], text=True, capture_output=True, check=False
    )
    assert completed.returncode != 0
    assert completed.stdout == ""
    assert "No module named roman.__main__" in completed.stderr
