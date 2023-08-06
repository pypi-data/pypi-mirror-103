import re

from typing import List, Tuple


class Validator:
    html_pattern = re.compile("<.*?>")
    non_letter_pattern = re.compile("[^a-zA-Z'\-\s]")

    def __init__(self, ignore_html=True, ignore_token_fraction=0.5):
        self.ignore_html = ignore_html
        self.acceptable_fraction_of_ignorable_tokens = ignore_token_fraction

    def _has_html(self, segment: str) -> bool:
        return self.html_pattern.match(segment) != None

    def _has_non_letter(self, segment: str):
        return self.non_letter_pattern.match(segment) != None

    def _is_empty(self, segment: str):
        return len(segment.strip()) == 0

    def _is_unacceptable(self, segment: str):
        if self._is_empty(segment):
            print("segment is empty")
            return True
        if self.ignore_html and self._has_html(segment):
            print("segment has HTML")
            return True
        return False

    def _is_ignored_tokens(self, token: str) -> bool:
        return self._has_non_letter(token)

    def _has_too_many_ignore_tokens(self, segment: str) -> bool:
        tokens = segment.strip().split(" ")
        token_length = len(tokens)
        ignored_tokens = [t for t in tokens if self._is_ignored_tokens(t)]
        ignored_length = len(ignored_tokens)
        if token_length == 0:
            return False
        else:
            return (
                ignored_length / token_length
                > self.acceptable_fraction_of_ignorable_tokens
            )

    def __call__(self, segment: str):
        if self._is_unacceptable(segment):
            return False
        if self._has_too_many_ignore_tokens(segment):
            print(f"too many non-letter tokens in {segment}")
            return False
        return True
