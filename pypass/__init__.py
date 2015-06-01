import os
import sys

_THISDIR = os.path.abspath(os.path.dirname(__file__))

DICTIONARY = os.path.join(_THISDIR, 'dictionary.txt')
MAX_WORD_LENGTH = 6
HEX_KEY_LENGTH = 64
NUM_WORDS = 4
LEFT_HAND = set('abcdefgqrstwxz')
RIGHT_HAND = set('hijklmnopuy')

#TODO: 1337-ify the passwd generated to increase robustess
#TODO: Add max pass length param
def newpass(wordlist, num_words=NUM_WORDS, max_word_length=MAX_WORD_LENGTH):
    """Pick a random wordlist-based password satisfying the given constraints
       with as secure a random number source as possible."""

    _filter = _make_word_filter(max_word_length)
    _wordlist = list(filter(_filter, wordlist))

    while num_words > 0:
        _listlength = len(_wordlist)
        assert _listlength > 0
        word = _wordlist.pop(_getrandom(_listlength))
        if _filter(word): yield word
        num_words -= 1

def newkey(length=HEX_KEY_LENGTH):
    """Hex keys of arbitrary length."""
    return ''.join([_hexify(_getrandom(16)) for i in xrange(HEX_KEY_LENGTH)])

####################################################################################################
#                                              UTILS                                               #
####################################################################################################

def _load_dict(filename):
    with open(filename) as f:
        for line in f.readlines():
            yield line.strip()

def _hexify(num):
    assert 0 <= num and num <= 16
    if num < 10: return chr(num + ord('0'))
    return chr(num - 10 + ord('A'))

def _getrandom(_max):
    # Goal: We need a random value evenly distributed over [0, _max - 1]
    #
    # Assumption:
    #   ord(os.urandom(1)) is evenly distributed over [0, k - 1]
    #   where k = 256, for log_2(k) possibilities.
    #
    #   Therefore, ord(os.urandom(n)) is evenly distributed over [0, 255^n]
    return _max * ord(os.urandom(1)) // 256

def _make_word_filter(max_word_length):
    """Returns an appropriate filter for typable passwords."""

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

    def _wordfilter(word):
        """Filter words"""
        if len(word) > max_word_length: return False
        if _repeats_letters(word): return False
        if not _alternates(word, LEFT_HAND, RIGHT_HAND): return False
        return True

    return _wordfilter

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    allwords = _load_dict(DICTIONARY)
    print ' '.join(newpass(allwords, NUM_WORDS, MAX_WORD_LENGTH))
    print ''.join(newkey(HEX_KEY_LENGTH))

    ##DEBUGGING WORDS
    #word = _rand_word(allwords, MAX_LENGTH)
    #print word, len(word), MAX_LENGTH

    ##DEBUGGING KEYS
    #key = newkey(HEX_KEY_LENGTH)
    #print key, len(key)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
