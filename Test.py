from CodeGame import CodeGame


def main():
    game = CodeGame()
    game.template.print_board()
    print("\n\nStarting Game:")
    game.start_game()
    guesses_remaining = 0

    while game.game_over() is None:
        if guesses_remaining == 0:
            print(
                ("Red" if game.red_turn else "Blue")
                + " informant, enter your clue ('word', number): "
            )

            # the clue and how many words fit that clue
            clue, words = input().split(", ")
            guesses_remaining = int(words)
            if (
                guesses_remaining == 0
                or (guesses_remaining > game.red_remaining and game.red_turn)
                or (guesses_remaining > game.blue_remaining and not game.red_turn)
            ):
                # set to max number of possible guesses for that team
                guesses_remaining = (
                    game.red_remaining if game.red_turn else game.blue_remaining
                )
            else:
                guesses_remaining += 1

        print(
            ("Red" if game.red_turn else "Blue")
            + " guesser, your clue is '"
            + clue
            + "'. Enter the word you wish to eliminate: "
        )

        successful_guess = game.make_guess(input())
        guesses_remaining -= 1
        winner = game.game_over()

        if winner is None:
            if successful_guess and guesses_remaining > 0:
                print(
                    "Would you like to make another guess? You have "
                    + str(guesses_remaining)
                    + " guesses remaining. \n(y/n)"
                )
                if input() != "y":
                    game.red_turn = not game.red_turn
                    guesses_remaining = 0
            else:
                game.red_turn = not game.red_turn
                guesses_remaining = 0
        else:
            print("GAME OVER! THE WINNER IS THE " + winner + " TEAM!")


if __name__ == "__main__":
    main()
