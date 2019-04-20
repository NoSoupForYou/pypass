from functools import reduce
import os
import sys


_DEBUG = False
"""Debug mode"""

_THISDIR = os.path.abspath(os.path.dirname(__file__))
DICTIONARY = os.path.join(_THISDIR, 'dictionary.txt')
"""Dictionary file"""


MIN_WORD_LENGTH = 6
MAX_WORD_LENGTH = 10
HEX_KEY_LENGTH = 64
NUM_WORDS = 4
"""Desired lengths"""


LEFT_HAND = set('abcdefgqrstwxz')
RIGHT_HAND = set('hijklmnopuy')
"""Character sets"""


# TODO: 1337-ify the passwd generated to increase robustess
# TODO: Add max pass length param
def newpass(
        wordlist, num_words=NUM_WORDS, min_word_length=MIN_WORD_LENGTH,
        max_word_length=MAX_WORD_LENGTH):
    """
    Pick a random wordlist-based password satisfying the given constraints
    with as secure a random number source as possible
    """

    _filter = _make_word_filter(min_word_length, max_word_length)
    _wordlist = list(filter(_filter, wordlist))

    while num_words > 0:
        _listlength = len(_wordlist)
        assert _listlength > 0
        word = _wordlist.pop(_getrandom(_listlength))
        if _filter(word):
            yield word
        num_words -= 1


def newkey(length):
    """Hex keys of arbitrary length."""
    return ''.join([_hexify(_getrandom(16)) for i in range(HEX_KEY_LENGTH)])


###############################################################################
#                                   UTILS                                     #
###############################################################################


def _load_dict(filename):
    with open(filename) as f:
        for line in f.readlines():
            yield line.strip()


def _hexify(num):
    assert 0 <= num and num <= 16
    if num < 10:
        return chr(num + ord('0'))
    return chr(num - 10 + ord('A'))


def _getrandom(_max):
    """
    Goal: We need a random value evenly distributed over [0, _max - 1]

    Assumption:
        ord(os.urandom(1)) is evenly distributed over [0, k - 1]
        where k = 256, for log_2(k) possibilities.

        Therefore, ord(os.urandom(n)) is evenly distributed over [0, 255^n]
    """
    return _max * ord(os.urandom(1)) // 256


def _make_word_filter(min_length, max_length):
    """Returns an appropriate filter for typable passwords."""

    def _repeats_letters(word):
        """Returns whether word repeats letters"""

        def nodups(a, b):
            if a == b:
                raise RuntimeError()
            return b

        try:
            list(reduce(nodups, word))
            return False
        except RuntimeError:
            return True

    def _alternates(word, *sets):
        """Make sure characters in word alternate word sets"""

        assert len(sets) > 1
        last_set = None
        for char in word:
            for _set in sets:
                if char in _set:
                    if last_set == _set:
                        return False
                    else:
                        last_set = _set

        return True

    def _wordfilter(word):
        """Filter words"""
        return all((
            min_length <= len(word) <= max_length,
            not _repeats_letters(word),
            not _alternates(word, LEFT_HAND, RIGHT_HAND)
        ))

    return _wordfilter


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    allwords = _load_dict(DICTIONARY)
    print(' '.join(newpass(
        allwords, NUM_WORDS, MIN_WORD_LENGTH, MAX_WORD_LENGTH)))
    print(''.join(newkey(HEX_KEY_LENGTH)))


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
