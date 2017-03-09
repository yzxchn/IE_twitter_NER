#!/usr/bin/env python

# Generate a dataset in the crfsuite compatible format.

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
            

def get_word_label_at(t, word_list, offset):
    """
    Get the word-label tuple at position word_i+offset
    """
    i = t + offset
    if i >= 0 and i < len(word_list):
        return word_list[i]
    else:
        return None

def get_word_at(t, word_list, offset):
    result = get_word_label_at(t, word_list, offset)
    if result:
        w, labels = result
        return "w[{}]={}".format(offset, w)
    else:
        return None

def get_label_at(t, word_list, offset):
    result = get_word_label_at(t, word_list, offset)
    if result:
        w, labels = result
        return "l[{}]={}".format(offset, labels[0])
    else:
        return None

def gen_feature_func(func, offset):
    """
    Generate a lambda function as a feature function

    func: a function requiring t, word_list and offset as its arguments
    offset: an integer

    This function supplies the offset to func as its argument, 
    and returns a lambda function requiring the other two arguments.
    """
    return lambda t, word_list: func(t, word_list, offset)

def extract_features(word_label_list, feature_funcs):
    word_features = []
    for i in range(len(word_label_list)):
        word_features.append([])
        for f in feature_funcs:
            word_features[-1].append(f(i, word_label_list))
    return word_features

if __name__ == "__main__":
    import sys, os
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

    sents = load_words(input_path)
    feature_funcs = [gen_feature_func(get_word_at, 0), gen_feature_func(get_word_at, -1), 
                gen_feature_func(get_word_at, -2), gen_feature_func(get_word_at, 1)]
    for s in sents:
        features = extract_features(s, feature_funcs)
        for i in range(len(s)):
            label = get_label_at(i, s, 0)
            line = label
            for f in features[i]:
                if not f is None:
                    line += '\t'+f
            output_file.write(line+'\n')

    input_file.close()
    output_file.close()

