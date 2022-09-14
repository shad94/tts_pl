""" from https://github.com/keithito/tacotron """

import re
from typing import Dict

import inflect

_inflect = inflect.engine()
_comma_number_re = re.compile(r"([0-9][0-9\,]+[0-9])")
_decimal_number_re = re.compile(r"([0-9]+\.[0-9]+)")
_currency_re = re.compile(r"(£|\$|¥)([0-9\,\.]*[0-9]+)")
_ordinal_re = re.compile(r"[0-9]+(st|nd|rd|th)")
_number_re = re.compile(r"-?[0-9]+")


def _remove_commas(m):
    return m.group(1).replace(",", "")


def _expand_decimal_point(m):
    return m.group(1).replace(".", " point ")


def __expand_currency(value: str, inflection: Dict[float, str]) -> str:
    parts = value.replace(",", "").split(".")
    if len(parts) > 2:
        return f"{value} {inflection[2]}"  # Unexpected format
    text = []
    integer = int(parts[0]) if parts[0] else 0
    if integer > 0:
        integer_unit = inflection.get(integer, inflection[2])
        text.append(f"{integer} {integer_unit}")
    fraction = int(parts[1]) if len(parts) > 1 and parts[1] else 0
    if fraction > 0:
        fraction_unit = inflection.get(fraction / 100, inflection[0.02])
        text.append(f"{fraction} {fraction_unit}")
    if len(text) == 0:
        return f"zero {inflection[2]}"
    return " ".join(text)


def _expand_currency(m: "re.Match") -> str:
    currencies = {
        "$": {
            0.01: "cent",
            0.02: "centy",
            1: "dolar",
            2: "dolary",
        },
        "€": {
            0.01: "cent",
            0.02: "centy",
            1: "euro",
            2: "euro",
        },
        "£": {
            0.01: "grosik",
            0.02: "pens",
            1: "funt",
            2: "funty",
        },
       
    }
    unit = m.group(1)
    currency = currencies[unit]
    value = m.group(2)
    return __expand_currency(value, currency)


def _expand_ordinal(m):
    return _inflect.number_to_words(m.group(0))


def _expand_number(m):
    num = int(m.group(0))
    if -1 < num < 32:
        if num == 0:
            return "zero"
        if num == 1:
            return "jeden"
        if num == 2:
            return "dwa"
        if num == 3:
            return "trzy"
        if num == 4:
            return "cztery"
        if num == 5:
            return "pięć"
        if num == 6:
            return "sześć"
        if num == 7:
            return "siedem"
        if num == 8:
            return "osiem"
        if num == 9:
            return "dziewięć"
        if num == 10:
            return "dziesięć"
        if num == 11:
            return "jedenaście"
        if num == 12:
            return "dwanaście"
        if num == 13:
            return "trzynaście"
        if num == 14:
            return "czternaście"
        if num == 15:
            return "piętnaście"
        if num == 16:
            return "szesnaście"
        if num == 17:
            return "siedemnaście"
        if num == 18:
            return "osiemnaście"
        if num == 19:
            return "dziewiętnaście"
        if num == 20:
            return "dwadzieścia"
        if num == 21:
            return "dwadzieścia jeden"
        if num == 22:
            return "dwadzieścia dwa"
        if num == 23:
            return "dwadzieścia trzy"
        if num == 24:
            return "dwadzieścia cztery"
        if num == 25:
            return "dwadzieścia pięć"
        if num == 26:
            return "dwadzieścia sześć"
        if num == 27:
            return "dwadzieścia siedem"
        if num == 28:
            return "dwadzieścia osiem"
        if num == 29:
            return "dwadzieścia dziewięć"
        if num == 30:
            return "trzydzieści"
        if num == 31:
            return "trzydzieści jeden"
    if 1000 < num < 3000:
        if num== 2022:
            return "dwa tysiące dwadzieścia dwa"
        if num == 2000:
            return "dwa tysiące"
        if 2000 < num < 2070:
            return "dwa tysiące " + _inflect.number_to_words(num % 100)
        if num % 100 == 0:
            return _inflect.number_to_words(num // 100) + " sto"
        return _inflect.number_to_words(num, andword="", zero="oh", group=2).replace(", ", " ")
    return _inflect.number_to_words(num, andword="")


def normalize_numbers(text):
    text = re.sub(_comma_number_re, _remove_commas, text)
    text = re.sub(_currency_re, _expand_currency, text)
    text = re.sub(_decimal_number_re, _expand_decimal_point, text)
    text = re.sub(_ordinal_re, _expand_ordinal, text)
    text = re.sub(_number_re, _expand_number, text)
    return text
