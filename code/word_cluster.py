#!/usr/bin/env python
import pickle

class WordCluster:
    def __init__(self, fpath=None):
        if fpath:
            self.load_dumped(fpath)
        else:
            self.cluster_table = {}
    
    def load_dumped(self, path):
        with open(path, "rb") as input_file:
            self.cluster_table = pickle.load(input_file)

    def generate_table(self, cluster_file):
        f = open(cluster_file)
        for l in f:
            items = l.split()
            if len(items)==3:
                path, tok, _ = l.split()
                self.cluster_table[tok] = path

    def get_cluster_path(self, token):
        """
        Given a token, return its cluster path
        """
        return self.cluster_table.get(token)

    def dump_table(self, output_path):
        with open(output_path, "wb") as out:
            pickle.dump(self.cluster_table, out)

if __name__ == "__main__":
    import sys
    cluster_file = "../data/50mpaths2.txt"

    cluster = WordCluster()
    cluster.generate_table(cluster_file)
    cluster.dump_table("../data/cluster.dump")

