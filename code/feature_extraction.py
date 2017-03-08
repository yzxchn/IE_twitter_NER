#!/usr/bin/env python

# Generate a dataset in the crfsuite compatible format.

def load_words(path):
    """
    Given a path, open the file, and load the words and tag(s) into a list. 
    Each word and its tags should be separated by a newline character.
    """
    f = open(path)
    tweets = []
    tweet = []
    for l in f:
        toks = l.split()
        if len(toks) >= 2:
            w, tags = toks[0], toks[1:]
            tweet.append((w, tags))
        else:
            tweets.append(tweet[:])
            tweet = []
    return tweets
            

def get_word_tag_at(t, word_list, offset):
    """
    Get the word-tag tuple at position word_i+offset
    """
    i = t + offset
    if i >= 0 and i < len(word_list):
        return word_list[i]
    else:
        return None

def get_word_at(t, word_list, offset):
    w, tags = get_word_tag_at(t, word_list, offset)
    return w

def get_tag_at(t, word_lsit, offset):
    w, tags = get_word_tag_at(t, word_list, offset)
    return tags[0]

def get_

def extract_features(file_path, output_path, feature_funcs):



if __name__ == "__main__":
    dev_path = "../data/dev.gold"
    tweets = load_words(dev_path)
    func = get_word_tag_at
    print(func(3, tweets[0], -1))

