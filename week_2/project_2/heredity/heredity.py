import csv
import itertools
import sys
from typing import Any, Dict, Set


PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def number_of_genes(person, one_gene, two_genes):
    return 1 if person in one_gene else 2 if person in two_genes else 0


def normalize_distribution(dist: Dict[Any, float]):
    norm = sum(val for val in dist.values())
    dist.update({key: val / norm for key, val in dist.items()})


def p_not_p(p):
    """p is the probability that something occurs 1 - p that something
    does not occur"""
    return [p, 1 - p]


def inherit_n_genes_prob(n_father, n_mother, mutation_prob) -> Dict:
    """Returns dictionary with distribution of conditional probability of
    inherited genes given that father has n_father genes and mother has
    n_mother genes, taking into account probability of mutations."""
    # Probabilities: [inherits from father, does not inherit from father]
    probs_f = p_not_p(n_father / 2)

    # Probabilities: [inherits from mother, does not inherit from mother]
    probs_m = p_not_p(n_mother / 2)

    # Probabilities: [gene mutates, gene does not mutate]
    mutation_prob = p_not_p(mutation_prob)
    probs_mut = {
        # Both genes mutate
        2: mutation_prob[0] ** 2,
        # Just one gene mutates
        1: 2 * mutation_prob[1] * mutation_prob[0],
        # None of the genes mutate
        0: mutation_prob[1] ** 2
    }

    # Assuming no mutations at all
    genes_prob_no_mut = {
        # Prob to inherit from both parents (no mutation)
        2: probs_f[0] * probs_m[0],
        # Prob to inherit from one parent only (no mutation)
        1: probs_f[0] * probs_m[1] + probs_f[1] * probs_m[0],
        # Prom to not inherit at all (no mutation)
        0: probs_f[1] * probs_m[1],
    }

    # Include mutations
    genes_prob = {
        # Prob to inherit from both parents
        2: (genes_prob_no_mut[2] * probs_mut[0] 
            + genes_prob_no_mut[1] * mutation_prob[0] * mutation_prob[1]   
            + genes_prob_no_mut[0] * probs_mut[2]),
        # Prob to inherit from one parent only
        1: (genes_prob_no_mut[1] * probs_mut[0]
            + (genes_prob_no_mut[0] + genes_prob_no_mut[2]) * probs_mut[1]),
        # Prob to not inherit at all
        0: (genes_prob_no_mut[2] * probs_mut[2]
            + genes_prob_no_mut[1] * mutation_prob[0] * mutation_prob[1]
            + genes_prob_no_mut[0] * probs_mut[0])
    }

    return genes_prob


def joint_probability(people: Set, one_gene: Set, two_genes: Set, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    joint_prob = 1

    for person in people:
        n_genes_person = number_of_genes(person, one_gene, two_genes)
        father = people[person]["father"]
        mother = people[person]["mother"]

        # Include probabilities of number of genes
        if father and mother:
            n_genes_father = number_of_genes(father, one_gene, two_genes)
            n_genes_mother = number_of_genes(mother, one_gene, two_genes)
            genes_probab = inherit_n_genes_prob(
                n_genes_father, n_genes_mother, PROBS["mutation"]
            )
            joint_prob *= genes_probab[n_genes_person]
        else:
            joint_prob *= PROBS["gene"][n_genes_person]

        # Include probabilities of trait
        joint_prob *= PROBS["trait"][n_genes_person][person in have_trait]

    return joint_prob


def update(probabilities: Dict, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person, probability in probabilities.items():
        n_genes = number_of_genes(person, one_gene, two_genes)
        has_trait = person in have_trait

        probability['gene'][n_genes] += p
        probability['trait'][has_trait] += p


def normalize(probabilities: Dict[str, Dict[str, Dict[Any, float]]]):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for distributions in probabilities.values():
        for distribution in distributions.values():
            normalize_distribution(distribution)


if __name__ == "__main__":
    main()
