import random


class CodeGame:
    def __init__(self, guesser_red, guesser_blue, hinter_red, hinter_blue):
        self.board = Board()
        self.template = Template()
        self.guesser_red = guesser_red
        self.guesser_blue = guesser_blue
        self.hinter_red = hinter_red
        self.hinter_blue = hinter_blue
        self.red_turn = True
        self.red_remaining = self.template.NUM_RED_SPIES
        self.blue_remaining = self.template.NUM_BLUE_SPIES

    def start_game(self):
        self.board.fill_board()
        self.board.print_board()

    # returns true if guess was made successfully
    def make_guess(self, guess):
        row = -1
        col = -1
        for i in range(self.board.HEIGHT):
            for j in range(self.board.WIDTH):
                if self.board.tiles[i][j] == guess.upper():
                    row = i
                    col = j
        if row == -1 or col == -1:
            raise ValueError("Word not on board")

        # updates counter and checks if guess was successful
        if (
            self.board.tiles[row][col] == "red_guess"
            or self.board.tiles[row][col] == "blue_guess"
        ):
            return False
        else:
            self.board.tiles[row][col] = "red_guess" if self.red_turn else "blue_guess"
        if self.template.tiles[row][col] is None:
            return False

        elif self.template.tiles == "red":
            self.red_remaining -= 1
            if not self.red_turn:
                return False
        elif self.template.tiles == "blue":
            self.blue_remaining -= 1
            if self.red_turn:
                return False

        return True

    # returns winner
    def game_over(self):
        if self.red_remaining == 0:
            return "RED"
        elif self.blue_remaining == 0:
            return "BLUE"

        for row in range(self.board.HEIGHT):
            for col in range(self.board.WIDTH):
                # mine collision
                if (
                    self.board.tiles[row][col] == "red_guess"
                    and self.template.tiles[row][col] == "mine"
                ):
                    return "BLUE"
                elif (
                    self.board.tiles[row][col] == "blue_guess"
                    and self.template.tiles[row][col] == "mine"
                ):
                    return "RED"

        return None


class Board:
    WIDTH = 5
    HEIGHT = 5
    WORD_FILES = ["wordlist-eng.txt"]  # configurable for more word packs

    def __init__(self):
        self.tiles = [
            [None for _ in range(self.WIDTH)] for _ in range(self.HEIGHT)
        ]  # initialize board as empty

    def fill_board(self):
        for row in range(self.HEIGHT):
            for col in range(self.WIDTH):
                self.tiles[row][col] = self.generate_word()

    def generate_word(self):
        # read file
        fileNum = random.randint(0, (len(self.WORD_FILES) - 1))
        file = open(self.WORD_FILES[fileNum], "r")
        lines = file.readlines()

        # grab a word that hasn't been used yet
        word = lines[random.randint(0, len(lines) - 1)]
        while word in self.tiles:
            lines.remove(word)
            word = lines[random.randint(0, len(lines) - 1)]
        return word.rstrip("\n")

    def print_board(self):
        for row in self.tiles:
            for cell in row:
                if cell is None:
                    print("_\t\t", end="")
                else:
                    print(cell + "\t" * (2 - int(len(cell) / 8)), end="")
            print("")


class Template(Board):
    NUM_RED_SPIES = 9  # configurable
    NUM_BLUE_SPIES = NUM_RED_SPIES - 1  # NO TOUCHY

    def __init__(self):
        self.tiles = [[None for _ in range(self.WIDTH)] for _ in range(self.HEIGHT)]
        self.fill_template()

    def fill_template(self):
        coords_remaining = [
            [j, i] for j in range(self.WIDTH) for i in range(self.HEIGHT)
        ]
        red_spies_placed = 0

        # place assassin
        pos = random.randint(0, len(coords_remaining) - 1)
        self.tiles[coords_remaining[pos][0]][coords_remaining[pos][1]] = "mine"
        del coords_remaining[pos]

        while red_spies_placed < self.NUM_RED_SPIES:
            # place blue spy
            if red_spies_placed < (self.NUM_BLUE_SPIES):
                pos = random.randint(0, len(coords_remaining) - 1)
                self.tiles[coords_remaining[pos][0]][coords_remaining[pos][1]] = "blue"
                del coords_remaining[pos]

            # place red spy
            pos = random.randint(0, len(coords_remaining) - 1)
            self.tiles[coords_remaining[pos][0]][coords_remaining[pos][1]] = "red"
            del coords_remaining[pos]

            red_spies_placed += 1
