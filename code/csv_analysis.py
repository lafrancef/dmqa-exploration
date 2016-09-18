import sys
import time

def shape_distance(a, b):
    '''
    Determines the 'distance' of the shape of two sequences of data. This
    measure checks if, from one element to the next, the two sequences 'behave
    similarly'.

    Formally, the measure is the sum of squared differences between the
    sequences of deltas between the elements of the two original sequences.
    Therefore, a measure of 0 means that the sequences have the same shape.
    '''

    measure = 0.0
    for i in range(len(a)):
        x_a = a[i]
        x_b = b[i]

        measure += (a[i] - b[i]) * (a[i] - b[i])

    return measure

def make_deltas(seqs):
    withZeros = [x + [0] for x in seqs]
    deltas = [[x[i] - x[i-1] for i in range(1, len(x))] for x in withZeros]
    maxLen = max([len(x) for x in deltas])
    for i, seq in enumerate(deltas):
        deltas[i] = seq + ([0] * (maxLen - len(seq)))

    return deltas


def cluster(seqs, threshold):

    last = 0
    clusters = [] # clusters[i] is a two element tuple of sequences and sets
    deltas = make_deltas(seqs)
    print('Clustering', len(seqs), 'sequences', file=sys.stderr)

    for i, seq in enumerate(deltas):
        min_clu = -1
        min_dist = 1 #???

        for j, clu in enumerate(clusters):
            dist = shape_distance(seq, deltas[clu[0]])
            if dist < min_dist or min_clu == -1:
                min_clu = j
                min_dist = dist

        if min_clu != -1 and min_dist < threshold:
            clusters[min_clu][1].add(i)
        else:
            new_clu = (i, set([i]))
            clusters.append(new_clu)

        if i % 1000 == 0:
            print(i, 'clus:', len(clusters), 'time:',
                    time.perf_counter() - last, file=sys.stderr)
            last = time.perf_counter()


    return clusters

def print_clus(seqs, clus):
    print('Clusters')
    print('\tNumber:', len(clus))
    for i, clu in enumerate(clus):
        print('\tClu', i, ':', len(clu[1]), 'elems, rep:', seqs[clu[0]])
        print('\t\tSample:', end=' ')

        for _ in range(8):
            if len(clu[1]) > 0:
                print(seqs[clu[1].pop()], end=',')
            else:
                break

        print()

def print_clu(seqs, clu):
    print('REP: ', seqs[clu[0]])
    for elem in clu[1]:
        print('\t', seqs[elem])

if __name__ == '__main__':
    hdl = open('csv_indices_all.csv')
    shapes = []
    ln = hdl.readline()
    while ln != '':
        sims = ln.split(',')[4::2] # Take every other point starting at index 4
        shapes.append([float(x) for x in sims])
        ln = hdl.readline()

    clus = cluster(shapes, 0.09)
    print_clus(shapes, clus)
