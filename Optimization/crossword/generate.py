import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        for i in self.domains:
            new = set()
            for j in self.domains[i]:
                if i.length == len(j):
                    new.add(j)
            self.domains[i] = new

    def revise(self, x, y):
        cx = self.crossword.overlaps[x, y][0]
        cy = self.crossword.overlaps[x, y][1]
        newD = set()
        revised = False
        for i in self.domains[x]:
            satisfies = False
            for j in self.domains[y]:
                if i[cx] == j[cy]:
                    satisfies = True
            if satisfies == False:
                revised = True
            else:
                newD.add(i)
        self.domains[x] = newD
        return revised

    def ac3(self, arcs=None):
        if arcs == None:
            queue = []
            for i in self.crossword.overlaps:
                if self.crossword.overlaps[i]:
                    queue.append(i)
        else:
            queue = arcs
        while queue:
            (x, y) = queue.pop(0)
            if self.revise(x, y):
                if not self.domains[x]:
                    return False
                for i in self.crossword.neighbors(x):
                    if i != y:
                        queue.append((x, i))
        return True

    def assignment_complete(self, assignment):
        complete = True
        for i in self.crossword.variables:
            if not i in assignment:
                complete = False
            else:
                if assignment[i] is None:
                    complete = False
        return complete

    def consistent(self, assignment):
        for i in assignment:
            if i.length != len(assignment[i]):
                return False
            for j in assignment:
                if i != j:
                    if assignment[i] == assignment[j]:
                        return False
                    if self.crossword.overlaps[(i, j)] is not None:
                        if assignment[i][self.crossword.overlaps[(i, j)][0]] != assignment[j][self.crossword.overlaps[(i, j)][1]]:
                            return False
        return True

    def order_domain_values(self, var, assignment):
        values = []
        if not var in assignment:
            for i in self.domains[var]:
                count = 0
                for j in self.domains:
                    if var != j:
                        if not j in assignment:
                            for h in self.domains[j]:
                                if self.crossword.overlaps[(var, j)]:
                                    if i[self.crossword.overlaps[(var, j)][0]] != h[self.crossword.overlaps[(var, j)][1]]:
                                        count = count+1
                values.append((i, count))
            values = sorted(values, key=lambda variable: variable[1])
            list = []
            for i in values:
                list.append(i[0])
            return list

    def select_unassigned_variable(self, assignment):
        vars = []
        for i in self.domains:
            if not i in assignment:
                vars.append((i, len(self.domains[i]), len(self.crossword.neighbors(i))))
        varsS = sorted(vars, key=lambda variable: variable[2], reverse=True)
        varsS = sorted(varsS, key=lambda variable: variable[1])
        return varsS[0][0]

    def backtrack(self, assignment):
        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        self.order_domain_values(var, assignment)
        for value in self.domains[var]:
            new_assignment = assignment.copy()
            new_assignment[var] = value
            if self.consistent(new_assignment):
                result = self.backtrack(new_assignment)
                if result is not None:
                    return result
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
