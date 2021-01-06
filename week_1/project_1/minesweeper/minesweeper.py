import itertools
import random
from typing import List
from copy import deepcopy


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        return self.cells if len(self.cells) == self.count else set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        return self.cells if self.count == 0 else set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        self.cells.discard(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        def mark_cells():
            for sentence in self.knowledge:
                for mine_cell in sentence.known_mines().copy():
                    self.mark_mine(mine_cell)
                for safe_cell in sentence.known_safes().copy():
                    self.mark_safe(safe_cell)
        
        def purge_knowledge():
            """Deletes all null sentences from knowledge ({} = 0)"""
            self.knowledge = [
                sentence for sentence in self.knowledge if sentence != Sentence(set(), 0)
            ]

        def update_knowledge_once():
            updated_knowledge: bool = False
            purge_knowledge()
            knowledge_copy = deepcopy(self.knowledge)
            for sentence_1 in knowledge_copy:
                for sentence_2 in knowledge_copy:
                    if sentence_1 == sentence_2 or not sentence_2.cells:
                        continue
                    elif sentence_1.cells > sentence_2.cells:
                        new_sentence = Sentence(
                            sentence_1.cells - sentence_2.cells,
                            sentence_1.count - sentence_2.count
                        )
                        if new_sentence not in self.knowledge:
                            self.knowledge.append(new_sentence)
                            updated_knowledge = True
            return updated_knowledge
        
        def print_status():
            print('Move: ', cell)
            print('KNOWLEDGE BASE:')
            for sentence in self.knowledge:
                print(str(sentence))
            print('SAFE: ', self.safes)
            print('MINES: ', self.mines)

        def update_knowledge():
            # print_status()
            mark_cells()
            updated_knowledge = update_knowledge_once()
            if not updated_knowledge:
                return
            else:
                return update_knowledge()
        
        self.moves_made.add(cell)
        self.mark_safe(cell)

        i, j = cell
        deltas = (-1, 0, 1)
        values_i = range(self.height)
        values_j = range(self.width)
        sentence_cells = set()

        for k in deltas:
            for l in deltas:
                ni, nj = new_cell = (i + k, j + l)
                if not (ni in values_i and nj in values_j):
                    continue
                elif new_cell not in (self.safes | self.moves_made):
                    sentence_cells.add(new_cell)

        self.knowledge.append(Sentence(sentence_cells, count))

        update_knowledge()

        # print('##############################################################')
        # print('\n\n')
        # print('##############################################################')

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        possible_moves = self.safes - self.moves_made
        return next(iter(possible_moves)) if possible_moves else None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        all_cells = set(
            (i, j) for i in range(self.height) for j in range(self.width)
        )
        possible_moves = all_cells - (self.mines | self.moves_made)
        return next(iter(possible_moves)) if possible_moves else None
