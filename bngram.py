import random, sys

# (Aux) Pad sentences.
# (1) Store n-gram tokens.
# (2) Randomly generate a sentence.

def pad_line(n, line):
    # pad line with n dummy words first, 1 dummy word last
    out = '<s> ' * (n - 1) + line.strip() + ' </s>'
    return out

def update_ngram_dictionary(n, line, d):
    # incorporate n-grams from line into d

    # pad the line
    line = pad_line(n, line)

    # extract and store n-grams.
    words = line.split()
    for i in range(0, len(words) - (n - 1)): # length of len, stop at n-1 index
        ngram = tuple(words[i : i+n]) # ngram as tuple, from current position + n-1 words

        prefix = ngram[:-1] #all but last word in ngram
        suffix = ngram[-1] # last word in ngram

        if not prefix in d: # add prefix to dictionary if new
            d[prefix] = []
        d[prefix].append(suffix) # add suffix to list at d[prefix]

    return d

def gen_sentence(n, d):
    # generate random sentence
    sentence = []

    prefix = tuple(['<s>'] * (n-1)) # First prefix will be series of n dummy words
    last_word = '' # check for last dummy word in while loop

    while last_word != '</s>': # '</s>' is end of sentence tag
        last_word = random.choice(d[prefix]) # randomly chooses next word
        sentence.append(last_word) # adds word to sentence

        prefix = prefix[1:] + (last_word, ) #next prefix: (n-1)gram+word

    sentence = ' '.join(sentence[:-1]) # combines without last dummy word

    return sentence

############

if __name__ == '__main__':
    what_gram = int(sys.argv[1])
    ngram_d = {}

    f = open('bullshit.txt', 'r')
    for line in f:
        d = update_ngram_dictionary(what_gram, line, ngram_d)
    f.close()

    print gen_sentence(what_gram, ngram_d)
