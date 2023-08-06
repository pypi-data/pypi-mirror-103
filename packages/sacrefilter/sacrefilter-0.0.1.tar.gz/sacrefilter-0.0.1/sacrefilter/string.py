
from __future__ import annotations
from typing import Iterator, List, Tuple

from functools import partial
from string import punctuation

import unicodedata
from unidecode import unidecode


def normalize_nfc(s):
    latin = re.compile('[a-zA-Z]+')
    normalized_chars = []
    for char in unicodedata.normalize('NFC', s):
        decoded = unidecode(char)  # Normalized character.
        normalized_chars.append(char if latin.match(decoded) else decoded)
    return "".join(normalized_chars)


def slugify(value, allow_unicode=False):
    """
    Slugify function from Django
    https://github.com/django/django/blob/main/django/utils/text.py
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')


class StringFilter:
    def __init__(self):
        pass

    def filter_corpus(self,
        self,
        source_corpus: Iterator[str],
        target_corpus: Iterator[str],
        remove_source_eq_target: bool=True,
        remove_single_char: bool=True,
        remove_startswith: Tuple[str]=None,
        remove_endswith: Tuple[str]=None,
        remove_contains: Tuple[str]=None,
        remove_non_roman: bool=False
        remove_regex_patterns: List[str]=None,
        ):
        for idx, (s, t) in tqdm(enumerate(zip(source_corpus, target_corpus))):
            # Check if source == target.
            if remove_source_eq_target and self.source_equals_target(s, t):
                continue
            # Check if source or target is single character.
            if remove_single_char and (self.single_character(s) or self.single_character(t)):
                continue
            # Check for startswith, endswith and contain operations.
            string_operations = {
                remove_startswith: partial(str.startswith, remove_startswith),
                remove_endswith: partial(str.endswith, remove_startswith),
                remove_contains: self.contains_filter
            }
            # Sets default to False.
            remove_string_operations = False
            # Checks through the operations.
            for substrings, str_func in string_operations.items():
                if substrings and str_func(s, substrings) and str_func(t, substrings):
                    remove_string_operations = True
                    break
            # Check for non-roman characters.
            if not self.is_roman(s) or not self.is_roman(t):
                continue
            # Yield the source and target that passed through the filters
            yield s, t

    @staticmethod
    def source_equals_target(s: str, t:str, normalize: bool=True) -> bool:
        # Checking the raw strings.
        raw_equals = s == t
        # Normalize whitespace.
        s_despace, t_despace = " ".join(s.split(), " ".join(t.split()
        normalize_equals = noramalize_nfc(s_despace) == noramalize_nfc(t_despace)

        if normalize:
            return raw_equals and normalize_equals
        else:
            return raw_equals

    @staticmethod
    def single_character(s: str) -> bool:
        return len(s) == 1

    @staticmethod
    def contains_filter(s: str, substrings: List[str]) -> bool:
        # See https://stackoverflow.com/q/3437059/610569
        return any(ch in s for ch in substrings)

    @staticmethod
    def string_reorders(s: str, t:str) -> bool:
        return set(s.lower().split()) == set(t.lower().split())

    @staticmethod
    def is_roman(s: str):
        s_no_punct = s.translate(str.maketrans('', '', punctuation))
        return len(slugify(s_no_punct)) == len(s_no_punct)
