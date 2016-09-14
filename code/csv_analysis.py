def shape_distance(a, b):
    '''
    Determines the 'distance' of the shape of two sequences of data. This
    measure checks if, from one element to the next, the two sequences 'behave
    similarly'.

    Formally, the measure is the sum of squared differences between the
    sequences of deltas between the elements of the two original sequences.
    Therefore, a measure of 0 means that the sequences have the same shape.
    '''

    # We'd like to keep track of the last element as well.
    # If we have the sequence [1.0], that should be treated differently
    # from [0.1]
    a.append(0)
    b.append(0)

    deltas_a = [a[i] - a[i-1] for i in range(1, len(a))]
    deltas_b = [b[i] - b[i-1] for i in range(1, len(b))]

    if len(deltas_a) < len(deltas_b):
        deltas_a.extend([0] * (len(deltas_b) - len(deltas_a)))
    else:
        deltas_b.extend([0] * (len(deltas_a) - len(deltas_b)))

    measure = 0.0
    for i in range(max(len(deltas_a), len(deltas_b))):
        x_a = deltas_a[i]
        x_b = deltas_b[i]

        measure += (x_a - x_b) * (x_a - x_b)

    return measure

def cluster(seqs, threshold):

    clusters = [] # clusters[i] is a two element tuple of sequences and sets
    for i, seq in enumerate(seqs):
        min_clu = -1
        min_dist = 1 #???

        for j, clu in enumerate(clusters):
            dist = shape_distance(seq, seqs[clu[0]])
            if dist < min_dist or min_clu == -1:
                min_clu = j
                min_dist = dist

        if min_clu != -1 and min_dist < threshold:
            clusters[min_clu][1].append(i)
        else:
            new_clu = (i, [i])
            clusters.append(new_clu)

    return clusters

def print_clus(seqs, clus):
    print('Clusters')
    print('\tNumber:', len(clus))
    for i, clu in enumerate(clus):
        print('\tClu', i, ':', len(clu[1]), 'elems, rep:', seqs[clu[0]])
        print('\t\tSample:', end=' ')
        for elem in clu[1][:8]:
            print(seqs[elem], end=',')
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

    print_clus(shapes, cluster(shapes, 0.08))
