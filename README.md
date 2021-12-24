## Instructions

The game is played in the terminal. It is written in Python3 language and only non-system library is Numpy. If you don't have numpy installed on your machine, you can simply install it by `pip install numpy`. 

1. One player runs the game without the ip address and the other player runs it with the ip address:

    * First player: `python battleship.py`
    * Second player: `python battleship.py 127.0.0.1`

2. After the connection is completed between players, the game asks players to position their ships on the board. Here, the user needs to specify the start position of the ship and its orientation. For example to place vertically at A1, the player enters `A1V` or to place horizontally at G8, the player enters `G8H`,
3. After each type of the ship is placed on both sides, the game starts. The second player who provided the ip sends the first move. To send your moves, you simply enter the position such `B4` and press enter when prompted in terminal. The game will then tell you if it was a hit or miss and update the opponent's map. 
4. The game will be finished when all the ships are hit on either side.  