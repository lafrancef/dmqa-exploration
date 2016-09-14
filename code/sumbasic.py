'''
@author: lafrancef

The summarization scheme implemented in this file is described in
Nenkova & Vanderwende 2005.
'''

def sumbasic(doc, sz, update_redundancy=True):
    '''
    Performs a basic extractive summarization scheme. Each word is assigned a
    score proportional to its frequency. Sentences with the highest total score
    are extracted until the size requirement is met. Optionally and by default,
    the scores of chosen words are discounted to prevent redundant sentences
    from being extracted.

    Returns a list of indices to the sentences of the document that were chosen,
    in the order they were chosen.
    '''

    N = sum([len(rsent) for rsent in doc.reduced_sents])
    scores = {word: amount / N for word, amount in
                doc.reduced_sents_counts.iteritems()}

    chosen = []
    available = doc.reduced_sents[:] # Copy of the reduced sentences
    while sz > 0:
        i = select_sentence(available, scores)

        if update_redundancy:
            # Only update once per type
            for w in set(doc.reduced_sents[i]):
                scores[w] *= scores[w]

        sz -= len(doc.sents[i])
        chosen.append[i]

        del available[i] # Never pick a sentence twice
        if len(available) == 0:
            break

    return chosen

def select_sentence(sents, scores):
    best_score = 0
    best_sent_i = -1
    for i, rsent in enumerate(doc.reduced_sents):

        if len(rsent) == 0:
            continue

        score = sum([scores[w] for w in red]) / float(len(red))
        if score > best_score:
            best_score = score
            best_isent = isent

    if best_sent_i == -1:
        raise Exception('No best sentence to summarize', doc.name)

    return best_sent_i
