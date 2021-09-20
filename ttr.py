import pandas as pd
import numpy as np

def compute_ttr_diffs(s, n_diffs, N):
    """
    Parameters
    ----------
    s: string
        A sentence of words separated by spaces
    n_diffs: int
        Number of differences to compute
    N: int
        Number of words to take in each difference
    
    Returns
    -------
    Average of ttr differences, or None if the passage was too short
    """
    words = s.lower().split()
    if len(words) < N:
        return
    avg = 0
    for round in range(n_diffs):
        # Do two rounds of random permutations
        lens = []
        for k in range(2):
            setk = set([words[i] for i in np.random.permutation(len(words))[0:N]])
            lens.append(len(setk))
        avg += np.abs(lens[0]-lens[1])
    return avg/(N*n_diffs)

def process_ttr_spreadsheet(path, sentence_col, n_diffs, N, verbose=True):
    """
    Compute the average TTR diffs on every element in a spreadsheet, and save
    a spreadsheet with an additional column with the average TTR differences

    Parameters
    ----------
    path: string
        Path to spreadsheet
    sentence_field: string
        The name of the column that holds the sentences
    n_diffs: int
        Number of differences to compute
    N: int
        Number of words to take in each difference
    verbose: boolean
        Whether to print progress
    """
    sentences = pd.read_csv(path)[sentence_col]
    fin = open(path)
    lines = [l.rstrip() for l in fin.readlines()]
    fin.close()
    fout = open(path[0:-4]+"_ttrdiff.csv", "w")
    fout.write(lines[0]+",\"TTR_DIFF\"\n")
    for i, (l, s) in enumerate(zip(lines[1::], sentences)):
        if verbose and i%10 == 9:
            print("{} of {}".format(i, len(sentences)))
        res = compute_ttr_diffs(s, n_diffs, N)
        fout.write(l + ",{}\n".format(res))
    fout.close()


if __name__ == '__main__':
    n_diffs = 100000
    N = 50
    for typ in ["pre", "post"]:
        path = "{}clean_allwords.csv".format(typ)
        sentence_col = "allspeech_{}".format(typ)
        print("Doing", path, "....")
        process_ttr_spreadsheet(path, sentence_col, n_diffs, N)