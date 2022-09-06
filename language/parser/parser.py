import nltk
from nltk.tokenize import word_tokenize
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | NP VP Conj NP VP | NP VP Conj VP NP

AP -> Adj Adj Adj | Adj Adj | Adj
NP -> Det N | N | PP NP | AP N | Det NP
PP -> P NP | P Det | P Det NP | P Det NP PP
VP -> V | V NP | V NP PP | V PP | Adv VP | V PP Adv | V Adv
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    words = word_tokenize(sentence)
    final = []
    for i in words:
        for j in i:
            if j.isalpha():
                final.append(i.lower())
                break
    print(final)
    return final


def np_chunk(tree):
    list = []
    for s in tree:
        if s.label() == "NP":
            add = True
            for h in s.subtrees(lambda t: t):
                if h.height() < s.height():
                    if h.label() == "NP":
                        add = False
            if add ==True:
                list.append(s)
    return list


if __name__ == "__main__":
    main()
