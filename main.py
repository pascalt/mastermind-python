from mastermindgame import MasterMindGame
from mastermindboard import MasterMindBoard


def main():
    """Create the master mind game and board and loop the board."""
    game = MasterMindGame()
    board = MasterMindBoard(game)
    board.mainloop()


if __name__ == "__main__":
    main()
