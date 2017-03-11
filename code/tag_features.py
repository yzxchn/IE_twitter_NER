#!/usr/bin/env python

# Preprocess the dataset and add feature tags to the tokens

from word_cluster import WordCluster
import os
from collections import defaultdict

def load_words(path):
    """
    Given a path, open the file, and load the words and label(s) into a list. 
    Each word and its labels should be separated by a newline character.
    """
    f = open(path)
    tweets = []
    tweet = []
    for l in f:
        toks = l.split()
        if len(toks) >= 2:
            w, labels = toks[0], toks[1:]
            tweet.append((w, labels))
        else:
            tweets.append(tweet[:])
            tweet = []
    return tweets

def tag_pos(word_list, tagger):
    """
    Given a list of (word, labels) pairs, 
    returns a list of POS tags corresponding to each word.
    """
    pos_tags = []
    sent = list(map(lambda x: x[0], word_list))
    tagged = tagger.tag(sent)
    for w, pos in tagged:
        pos_tags.append(pos)
    assert len(pos_tags) == len(word_list)
    return pos_tags

def tag_cluster_path(word_list, cluster_obj):
    """
    Given a list of (word, labels) pairs, 
    returns a list os word_cluster path values corresponding to each word.
    """
    cluster_paths = []
    for w, labels in word_list:
        cpath = cluster_obj.get_cluster_path(w.lower())
        if cpath:
            cluster_paths.append(cpath)
        else:
            cluster_paths.append("")
    return cluster_paths

def tag_capitalized(word_list):
    """
    Given a list of (word, labels) pairs, 
    returns a list of flags indicating whether the corresponding word is 
    capitalized or not.
    """
    flags = []
    for w, labels in word_list:
        if w.isupper() or w.istitle():
            flags.append("is_cap")
        else:
            flags.append("no_cap")
    return flags

def tag_word(word_list):
    words = []
    for w, labels in word_list:
        words.append(w)
    return words

def get_tags(word_list, tag_funcs):
    sent_tags = [[] for w in word_list]
    for f in tag_funcs:
        tags = f(word_list)
        for i in range(len(word_list)):
            sent_tags[i].append(tags[i])
    return sent_tags

if __name__ == "__main__":
    import sys
    from os.path import join, dirname, realpath
    from word_cluster import WordCluster
    from nltk.tag import StanfordPOSTagger as SPT

    try: 
        input_path, output_path = sys.argv[1], sys.argv[2]
    except IndexError:
        print("Error: Please supply the input and output file paths")
        print("e.g. python feature_extraction.py <input_path> <output_path>")
        exit(1)
    try:
        input_file = open(input_path)
        output_file = open(output_path, 'w')
    except IOError as e:
        print(str(e))
        exit(1)

    wcpath = join(dirname(dirname(realpath(__file__))), "data/cluster.dump")
    wc = WordCluster(fpath=wcpath)
    
    tagger = SPT("models/gate-EN-twitter.model", 
                 "stanford-postagger-2016-10-31/stanford-postagger.jar")

    sents = load_words(input_path)
    #list of functions to be applied to the data
    tag_funcs = [tag_word, lambda wl:tag_pos(wl, tagger), 
                 lambda wl:tag_cluster_path(wl, wc), tag_capitalized]

    total = len(sents)
    counter = 1

    for s in sents:
        print("Tagging {}/{}".format(counter, total))
        tags = get_tags(s, tag_funcs)
        labels = list(map(lambda x:x[1][0], s))
        assert len(tags)==len(labels)
        for i in range(len(labels)):
            tags[i].insert(0, labels[i])
            line = '\t'.join(tags[i])
            output_file.write(line+'\n')
        output_file.write('\n')
        counter += 1

    input_file.close()
    output_file.close()
