import os
import sys

_THISDIR = os.path.abspath(os.path.dirname(__file__))

DICTIONARY = os.path.join(_THISDIR, 'dictionary.txt')
MAX_LENGTH = 6
WORD_NUM = 4
LEFT_HAND = set('abcdefgqrstwxz')
RIGHT_HAND = set('hijklmnopuy')

def newpass(wordlist, num_words, max_length):
    """Pick a random word from wordlist satisfying the given constraints
       with as secure a random number source as possible."""

    def _getrandom(_max):
        # Goal: We need a random value evenly distributed over [0, l - 1]
        #
        # Assumption:
        #   ord(os.urandom(1)) is evenly distributed over [0, k - 1]
        #   where k = 256, for log_2(k) possibilities.
        #
        #   Therefore, ord(os.urandom(n)) is evenly distributed over [0, 255^n]
        return _max * ord(os.urandom(1)) // 256

    def _is_ok(word):
        """Filter words"""
        if len(word) > max_length: return False
        if _repeats_letters(word): return False
        if not _alternates(word, LEFT_HAND, RIGHT_HAND): return False
        return True

    _wordlist = list(filter(_is_ok, wordlist))

    while num_words > 0:
        _listlength = len(_wordlist)
        assert _listlength > 0
        word = _wordlist.pop(_getrandom(_listlength))
        if _is_ok(word): yield word
        num_words -= 1

####################################################################################################
#                                              UTILS                                               #
####################################################################################################

def _load_dict(filename):
    with open(filename) as f:
        for line in f.readlines():
            yield line.strip()

def _repeats_letters(word):
    def nodups(a,b):
        if a == b: raise RuntimeError()
        return b
    try:
        reduced = reduce(nodups, word)
    except:
        return True
    return False

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

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    allwords = _load_dict(DICTIONARY)
    print ' '.join(newpass(allwords, WORD_NUM, MAX_LENGTH))
    #word = _rand_word(allwords, MAX_LENGTH)
    #print word, len(word), MAX_LENGTH

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
