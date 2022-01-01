# Connect4
Players alternatively take turns placing red and yellow pieces on a 6 by 7 board. Implemented with pygame. This version has a minimax algorithm optimized with alpha-beta pruning to play against an AI player. There is also a local 2 player game mode.

![game](https://user-images.githubusercontent.com/48500458/147859947-a2ce26b2-5603-4d96-9fde-9d338312171e.png)

Rules: 
The players' colors are decided randomly. 
Players alternate turns and only one disc is dropped per turn.
On your turn, drop one of your colored discs from the top into one of any of the seven columns.
The game is over when a player earns a connect 4 either horizontally, vertically, or diagonally, or there is a stalemate.

Classes:
main.py contains the pygame event loop.
Board.py contains the board game functions.
Tile.py contains the path file to tiles: WHITE, YELLOW, or RED.
AI.py contains the logic for the AI player to make a move using the minimax algorithm optimized with alpha-beta pruning.
Colors.py is an Enum class containing the values WHITE, YELLOW, and RED, along with some useful class methods.

In AI.py, the MAX_DEPTH class variable is set to 2. To change the AI difficulty, make changes to the MAX_DEPTH class variable.
