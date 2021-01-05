from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")


def exclusive_or(x, y):
    return And(Or(x, y), Not(And(x, y)))


def knowledge_by_sentence(sentence, Knight, Knave):
    return And(
        Biconditional(sentence, Knight),
        Biconditional(Not(sentence), Knave)
    )


# Puzzle 0
# A says "I am both a knight and a knave."
sentence_0_A = And(AKnight, AKnave)
knowledge0 = And(
    exclusive_or(AKnight, AKnave),
    knowledge_by_sentence(sentence_0_A, AKnight, AKnave)
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
sentence_1_A = And(AKnave, BKnave)
knowledge1 = And(
    exclusive_or(AKnight, AKnave),
    exclusive_or(BKnight, BKnave),
    knowledge_by_sentence(sentence_1_A, AKnight, AKnave)
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
sentence_2_A = exclusive_or(And(AKnight, BKnight), And(AKnave, BKnave))
sentence_2_B = exclusive_or(And(AKnight, BKnave), And(AKnave, BKnight))
knowledge2 = And(
    exclusive_or(AKnight, AKnave),
    exclusive_or(BKnight, BKnave),
    knowledge_by_sentence(sentence_2_A, AKnight, AKnave),
    knowledge_by_sentence(sentence_2_B, BKnight, BKnave)
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge_3_A_B = exclusive_or(
    And(knowledge_by_sentence(AKnave, AKnight, AKnave), BKnight),
    And(knowledge_by_sentence(AKnight, AKnight, AKnave), BKnave)
)
sentence_3_B_2 = CKnave
sentence_3_C = AKnight
knowledge3 = And(
    exclusive_or(AKnight, AKnave),
    exclusive_or(BKnight, BKnave),
    exclusive_or(CKnight, CKnave),
    knowledge_3_A_B,
    knowledge_by_sentence(sentence_3_B_2, BKnight, BKnave),
    knowledge_by_sentence(sentence_3_C, CKnight, CKnave)
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
