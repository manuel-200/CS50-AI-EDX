import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    res = dict()
    for i in corpus:
        res[i] = (1-damping_factor)/len(corpus)
    if not bool(corpus[page]):
        for i in res:
            res[i] = res[i]+damping_factor/len(corpus)
    else:
        for i in res:
            for j in corpus[page]:
                if i == j:
                    res[i] = res[i]+damping_factor/len(corpus[page])
    return res


def sample_pagerank(corpus, damping_factor, n):
    keys = list(corpus.keys())
    Page = random.choice(keys)
    samples = []
    for j in range(n):
        sum = 0
        ran = random.random()
        tran = transition_model(corpus, Page, damping_factor)
        for i in tran:
            sum = sum+tran[i]
            if ran <= sum:
                samples.append(i)
                Page = i
                break
    results=dict()
    for i in corpus:
        count=0
        for j in samples:
            if j == i:
                count = count+1
        results[i] = count/len(samples)
    
    return results


def iterate_pagerank(corpus, damping_factor):
    results = dict()
    results2 = dict()
    for i in corpus:
        results2[i] = 1/len(corpus)
        results[i] = 0
    N = len(corpus)
    conv = 0
    while conv < len(corpus):
        """ sum=0
        ran=random.random()
        tran = transition_model(corpus,Page,damping_factor) """
        conv = 0
        for i in results2:
            sump=0
            for j in corpus:
                if i in corpus[j]:
                    sump=sump+results2[j]/len(corpus[j])
            results = results2.copy()
            results2[i] = (1-damping_factor)/N+damping_factor*sump
            if abs(results[i]-results2[i]) < 0.001:
                conv = conv+1

        """ for i in tran:
            sum=sum+tran[i]
            if ran <= sum:
                Page=i
                sump=0
                for j in results2:
                    sump=sump+results2[j]/len(corpus[j])
                results=results2.copy()
                results2[i]=(1-damping_factor)/N+damping_factor*sump
                print(results2)
                break """
    return results2



if __name__ == "__main__":
    main()