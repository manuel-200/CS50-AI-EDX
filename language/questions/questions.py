import nltk
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    dicti = dict()
    for txt in os.listdir(directory):
        f = open(os.path.join(directory, txt), 'r')
        dicti[txt] = f.read()
    return dicti


def tokenize(document):
    words = nltk.word_tokenize(document)
    punct = []
    wordy = []
    for i in string.punctuation:
        punct.append(i)
    for i in words:
        if not i.lower() in nltk.corpus.stopwords.words("english"):
            append = False
            for j in i:
                if not j in punct:
                    append = True
            if append == True:
                wordy.append(i.lower())
    return wordy


def compute_idfs(documents):
    unique = dict()
    docs = len(documents)
    for i in documents:
        for j in documents[i]:
            if j not in unique:
                count = 0
                for h in documents:
                    if j in documents[h]:
                        count = count+1
                unique[j] = math.log(docs/count)
    return unique


def top_files(query, files, idfs, n):
    filerank = []
    for i in files:
        total = 0
        for j in query:
            if j in files[i]:
                count = 0
                for h in files[i]:
                    if h == j:
                        count = count+1
                total = total+count*idfs[j]
        filerank.append((i, total))
    filenames = sorted(filerank, key=lambda variable: variable[1], reverse=True)
    filenamesN = []
    for i in filenames:
        filenamesN.append(i[0])
    return filenamesN[:n]


def top_sentences(query, sentences, idfs, n):
    sentencerank = []
    for i in sentences:
        total = 0
        count = 0
        for j in query:
            if j in sentences[i]:
                count = count+1
                total = total+idfs[j]
        sentencerank.append((i, total, count/len(sentences[i])))
    sentenc = sorted(sentencerank, key=lambda variable: variable[2], reverse=True)
    sentenc = sorted(sentenc, key=lambda variable: variable[1], reverse=True)
    sentenceN = []
    for i in sentenc:
        sentenceN.append(i[0])
    return sentenceN[:n]


if __name__ == "__main__":
    main()
