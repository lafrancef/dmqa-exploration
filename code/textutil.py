'''
Useful functions to keep around.
@author: lafrancef
'''

from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

from string import digits as DIGITS
LEMMATIZER = WordNetLemmatizer()
STOPS = set(stopwords.words('english'))

def build_doc_sentences(doc_contents):
    '''
    Returns a list of tuples. For each tuple, the first element is the input
    sentence and the second element is its corresponding reduced sentence.

    If a sentence is reduced to nothing, its corresponding tuple is omitted.
    '''
    sentences = sent_tokenize(doc_contents)
    reduced = [reduce_sentence(sent) for sent in sentences]

    not_empty_f = lambda x: len(x) > 0

    sentences = [s for i, s in enumerate(sentences) if not_empty_f(reduced[i])]
    reduced = [s for s in reduced if not_empty_f(s)]

    return zip(sentences, reduced)

def reduce_sentence(sent):
    '''
    Reduces all the words in a sentence.
    '''
    return [r for r in [reduce_word(w) for w in word_tokenize(sent)] if r is not None]

def reduce_word(word):
    '''
    Reduces a word by case-folding and lemmatizing it. Returns the reduced form.
    If the word is not alphanumeric, or is a stop word, None is returned.
    '''
    # We want to keep numbers - seems like they could be important (financial
    # news for example).
    if is_number(word):
        return word

    if not is_word(word):
        return None

    reduced = LEMMATIZER.lemmatize(word.lower())
    if reduced in STOPS:
        return None
    return reduced

def is_word(s):
    '''
    Checks whether a string a word. Unlike isalnum(), this will allow
    hyphenated words.
    '''

    if s is None or len(s) == 0:
        return False

    has_alnum = False
    for c in s:
        is_alnum = c.isalnum()
        if c != '-' and not is_alnum:
            return False
        if is_alnum:
            has_alnum = True

    return has_alnum

def is_number(s):
    '''
    Checks whether a string is a number. Unlike isdigit(), this allows
    things like "10.2" or "100,000". NLTK's tokenizer won't split those
    (but will split "$10.50" into "$" and "10.50", so we're good for that)
    '''
    if s is None or len(s) == 0:
        return False

    has_number = False
    for c in s:
        isDigit = c in DIGITS
        if c != '.' and c != ',' and not isDigit:
            return False
        if isDigit:
            has_number = True

    return has_number

def n_grams(words, n):
    '''
    Returns a list of n-grams from a list of words.
    '''
    if n <= 1:
        return words

    parts = [words[i:] for i in range(n)]

    return zip(*parts)


def pretty(s, length=50):
    '''
    Pretty-prints a string using an ascii encoding.

    @param length: specifies the maximum length of the string that will be
    printed before adding an ellipsis. If negative, the entire string is always
    printed.

    '''
    if length >= 0 and len(s) > length:
        s = s[:length] + '...'

    return str(s.encode('ascii', 'replace'))

def counter_to_csv(counter, label_keys='', label_values=''):
    return assocs_to_csv(list(counter.items()))

def assocs_to_csv(assoc_list, label_keys='', label_values=''):
    csv = []
    if label_keys or label_values:
        csv.append(label_keys + ',' + label_values)

    for (k, v) in assoc_list:
        csv.append(k + ',' + v)

    return '\n'.join(csv)
