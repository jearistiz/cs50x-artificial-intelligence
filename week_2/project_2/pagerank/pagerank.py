import os
import random
import re
import sys
from collections import Counter

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
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # If page has no links at all, assume it has links to all pages
    links_in_page = corpus[page]
    links_in_page = links_in_page if links_in_page else set(corpus)

    # Probability associated with links in current page
    prob_links = damping_factor / len(links_in_page)
    # Probability associated with all pages
    prob_page = (1 - damping_factor) / len(corpus)

    # Build the transition model
    transition_distribution = {}
    for page_i in corpus:
        prob_links_i = prob_links if page_i in links_in_page else 0
        transition_distribution[page_i] = (prob_links_i + prob_page)

    return transition_distribution


def sample_pagerank(corpus: dict, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Dictionary with info of all transition probabilities. Format:
    # {page_i: [(page_1, page_2, ...), (prob_i1, prob_i2, ...)], ...}
    # transition from page_i to page_j is prob_ij
    transition_prob = {
        page: list(zip(*transition_model(corpus, page, damping_factor).items()))
        for page in corpus
    }

    # Sample all pages according to transition probabilities
    samples = [random.choice(list(corpus.keys()))]
    for i in range(n - 1):
        current_page = samples[-1]
        pages, probabilities = transition_prob[current_page]
        sample = random.choices(pages, probabilities).pop()
        samples.append(sample)

    # Count frequencies from samples and deduce probabilities (i.e. PageRank)
    frequencies = Counter(samples)
    page_rank = {page: freq / n for page, freq in frequencies.items()}

    return page_rank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.

    Warning
    -------
    If this fails just try to evaluate the while loop by one iteration less.
    """
    def page_rank_formula(
        page: str, parents: dict, pages_rank: dict, N_links: dict, N_pages
    ):
        """Formula used to calculate the PageRank value of a page"""
        links_prob = [
            pages_rank[page_i] / N_links[page_i] for page_i in parents[page]
        ]
        return (1 - damping_factor) / N_pages + damping_factor * sum(links_prob)

    # Total number of pages
    N_pages = len(corpus)

    # Number of links per page
    N_links = {}
    for page in corpus:
        n_links = len(corpus[page])
        # If page has no links at all, assume it has links to all pages
        corpus[page] = corpus[page] if n_links else set(corpus)
        n_links = n_links if n_links else N_pages
        N_links[page] = n_links

    # format: {page: set(all pages that have a link to page)}
    parents = {
        page: set(parent for parent, links in corpus.items() if page in links)
        for page in corpus
    }

    # Initialize probability and precision
    a_priori_prob = 1 / N_pages
    pages_rank = {page: a_priori_prob for page in corpus}
    precision = [1]

    desired_precision = 0.001

    # Calculate page rank until values are sufficiently precise
    while list(filter(lambda x: x >= desired_precision, precision)):
        new_pages_rank = {
            page: page_rank_formula(page, parents, pages_rank, N_links, N_pages)
            for page in corpus
        }
        precision = [
            abs(pages_rank[page] - new_pages_rank[page]) for page in corpus
        ]
        pages_rank = new_pages_rank

    return pages_rank


if __name__ == "__main__":
    main()
