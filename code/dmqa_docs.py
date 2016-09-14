'''
@author: lafrancef
'''

import textutil
import glob
import itertools

from collections import Counter

DATA_ROOT = '../data/'
SUBFOLDERS = ['cnn/', 'dailymail/']
STORIES = 'stories/*.story'

GRAM_LEN = 2

class DmqaDoc:
    '''
    A document from the DMQA corpus. Divides text between article content and
    highlights.
    '''

    def __init__(self, name, text):
        '''
        Create a document from raw text.
        '''
        self.name = name
        self._raw = text

        parts = text.split('@highlight')

        self._raw_contents = parts[0].strip()

        # Split the text on paragraph breaks (the default NLTK sentence tokenizer
        # seems to have some trouble with those), then build sentences on each
        # split segment.
        segs = map(textutil.build_doc_sentences, self._raw_contents.split('\n\n'))

        # Flatten segments into one list
        contentSents = []
        for seg in segs:
            contentSents.extend(seg)

        self.sents = [s for s, r in contentSents]
        self.reduced_sents = [r for s, r in contentSents]

        # Every highlight is one sentence
        self.highlights = [s.strip() for s in parts[1:]]
        self.reduced_highlights = [textutil.reduce_sentence(s) for s
                                   in self.highlights]

        self.similarities = self._compute_similarities()

    def _compute_similarities(self):
        '''
        Returns a list of lists of tuples. The sublist at index i is associated
        to highlight i. The tuple at index j of sublist i has two elements: an
        index to a sentence with a nonzero similarity score with the highlight,
        and the similarity score in question.
        '''
        sim_per_highlight = []

        for highlight in self.reduced_highlights:
            sim = []
            for i, sent in enumerate(self.reduced_sents):
                score = ngram_overlap(highlight, sent, GRAM_LEN)
                if (score > 0):
                    sim.append((i, score))

            sim.sort(key=lambda x: x[1], reverse=True)
            sim_per_highlight.append(sim)

        return sim_per_highlight

    def __str__(self):
        return textutil.pretty(self._raw)

    def __repr__(self):
        return str(self)

    def reduced_sents_counts(self):
        count = Counter()
        for rsent in self.reduced_sents:
            for w in rsent:
                count[w] += 1

        return count.items()


def ngram_overlap(reference, candidate, n):
    '''
    n-gram overlap (i.e. ROUGE-n) between a candidate and a reference.
    Corresponds to #(cooccurring n-grams) / #(n-grams in reference).
    '''

    ngrams_ref = set(textutil.n_grams(reference, n))

    # Could happen if we want e.g. a 4-gram on a len-3 sentence
    if len(ngrams_ref) == 0:
        return 0

    count = 0
    for gram in set(textutil.n_grams(candidate, n)):
        if gram in ngrams_ref:
            count += 1

    return count / (len(reference) - n + 1)

def generate_docs(limit=None):
    '''
    Generate a number of documents, with an optional limit.
    '''
    for folder in SUBFOLDERS:
        files = glob.glob(DATA_ROOT + folder + STORIES)[:limit]
        for fname in files:
            with open(fname, encoding='utf-8') as hdl:
                yield DmqaDoc(fname, hdl.read())

def pretty_all(doc):
    '''
    Pretty-prints all matches for every highlight in the given document.
    '''
    for i, sim_hi in enumerate(doc.similarities):
        print(doc.name, end='/    ')
        print(textutil.pretty(doc.highlights[i]), ':', end=' ')
        for sent, sim in sim_hi:
            print(textutil.pretty(doc.sents[sent]), '(', sim, ')', end=', ')

        print()

def pretty_best(doc):
    '''
    Pretty-prints the top match for every highlight in the given document.
    '''
    for i, sim_hi in enumerate(doc.similarities):
        print(doc.name, end='/    ')
        print(textutil.pretty(doc.highlights[i], -1), end=': ')
        if sim_hi:
            sent, sim = sim_hi[0]
            print(textutil.pretty(doc.sents[sent], -1), '(', sim, ')')
        else:
            print('none')

def pretty_none(doc):
    '''
    Pretty-prints the highlights that have no matches in the given document.
    '''
    for i, sim_hi in enumerate(doc.similarities):
        if not sim_hi:
            print(doc.name, end='/    ')
            print(textutil.pretty(doc.highlights[i]))

def csv_indices(doc):
    '''
    Prints every highlight and its similarity values in the following format:

    filename,num_sents - 1,highlight,sent1,similarity1,sent2,similarity2, ...
    '''
    for i, sim_hi in enumerate(doc.similarities):
        print(doc.name, end=',')
        print(len(doc.sents) - 1, end=',') # Last index of a sentence.
        print(i, end=',')
        for sent, sim in sim_hi:
            print(sent, end=',')
            print(sim, end=',')

        print()

def print_hi_lengths(doc):
    for hi in doc.highlights:
        print(doc.name, ': ', len(hi))

def print_num_words_all_his(doc):
    '''
    Prints the number of words in all highlights of the document.
    '''
    # Good enough for an approximation. Ignoring consecutive spaces, etc.
    print(sum([hi.count(' ') + 1 for hi in doc.highlights]))


def bucket_counts(sims):
    buckets = Counter()

    for sims_doc in sims:
        buckets.update([len(sim_hi) for sim_hi in sims_doc])

    return buckets

def bucket_position_matches(docs, only_best=False):

    buckets = Counter()
    for i, doc in enumerate(docs):
        sims_doc = doc.similarities
        len_doc = len(docs[i].sents)
        if only_best:
            raw = [sim_hi[0][0] / len_doc for sim_hi in sims_doc if sim_hi]
        else:
            sims_doc_flat = itertools.chain.from_iterable(sims_doc)
            raw = [sent_i / len_doc for (sent_i, _) in sims_doc_flat]

        buckets.update([round(x, 2) for x in raw])

    return buckets

if __name__ == '__main__':

    for doc in generate_docs():
        csv_indices(doc)
