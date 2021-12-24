import sys
import socket
import numpy as np

#column names are letters, so LETTER_TO_INDEX dictionary is defined
LETTER_TO_INDEX = {
    'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4,
    'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9}

#Define Ships object class, Carrier-5, Battleship-4, Submarine-3, Destroyer-2, 
class Ships:
    C = {'SIZE': 5, 'ID': 'C'}
    B = {'SIZE': 4, 'ID': 'B'}
    S = {'SIZE': 3, 'ID': 'S'}
    D = {'SIZE': 2, 'ID': 'D'}

#The main part of project, Battleship game logic coded in this class
class Battleship:
    #def means you start a function (definition), and it needs a space to follow. The function __init__ is the constructor.
    def __init__(self, ip=None):
        #self represents the instance of the class. By using the “self” keyword we can access the attributes and methods of the class
        #in python. It binds the attributes with the given arguments
        
        #np.zeros(10,10) Return a new array of 10x10 and type 7-character Unicode String, filled with zeros
        # Intitalize the boards
        
        self.my_board = np.zeros((10, 10), dtype='<U7')
        self.op_board = np.zeros((10, 10), dtype='<U7')
        
        # Create a TCP/IP socket
        self.ip = ip #server ip argument takes in code
        self.port = 34000 #default port that server and client connect through this port and game is played on this port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #The arguments passed to socket() specify the address family and socket type. AF_INET is the Internet address family for IPv4.
        #SOCK_STREAM is the socket type for TCP, the protocol that will be used to transport our messages in the network.
        
        self.my_turn = False
        self.finished = False
        self.num_of_hits = 0

    def ask_for_ships(self):
        # Ask for ship positions and orientations
        print('Place the ships with their position and orinetation e.g. A1V for vertical at position 11')
        self.c_loc = input('Please place the Carrier:')
        self.b_loc = input('Please place the Battleship:')
        self.s_loc = input('Please place the Submarine:')
        self.d_loc = input('Please place the Destroyer:')

        c_loc_x = int(self.c_loc[1]) - 1
        c_loc_y = LETTER_TO_INDEX[self.c_loc[0]]

        b_loc_x = int(self.b_loc[1]) - 1
        b_loc_y = LETTER_TO_INDEX[self.b_loc[0]]

        s_loc_x = int(self.s_loc[1]) - 1
        s_loc_y = LETTER_TO_INDEX[self.s_loc[0]]

        d_loc_x = int(self.d_loc[1]) - 1
        d_loc_y = LETTER_TO_INDEX[self.d_loc[0]]


        if self.c_loc[2] == 'V':
            self.my_board[c_loc_x:c_loc_x+Ships.C['SIZE'], c_loc_y] = Ships.C['ID']
        elif self.c_loc[2] == 'H':
            self.my_board[c_loc_x, c_loc_y:c_loc_y+Ships.C['SIZE']] = Ships.C['ID']

        if self.b_loc[2] == 'V':
            self.my_board[b_loc_x:b_loc_x+Ships.B['SIZE'], b_loc_y] = Ships.B['ID']
        elif self.b_loc[2] == 'H':
            self.my_board[b_loc_x, b_loc_y:b_loc_y+Ships.B['SIZE']] = Ships.B['ID']

        if self.s_loc[2] == 'V':
            self.my_board[s_loc_x:s_loc_x+Ships.S['SIZE'], s_loc_y] = Ships.S['ID']
        elif self.s_loc[2] == 'H':
            self.my_board[s_loc_x, s_loc_y:s_loc_y+Ships.S['SIZE']] = Ships.S['ID']

        if self.d_loc[2] == 'V':
            self.my_board[d_loc_x:d_loc_x+Ships.D['SIZE'], d_loc_y] = Ships.D['ID']
        elif self.d_loc[2] == 'H':
            self.my_board[d_loc_x, d_loc_y:d_loc_y+Ships.D['SIZE']] = Ships.D['ID']

        self.print_board()

    def print_board(self):
        print('------------You-----------')
        print(self.my_board)
        print('------------Opponent------------')
        print(self.op_board)

    def connect(self):
        # Bind the socket and wait for other player to connect
        if self.ip is None:
            print('Waiting for other opponent to connect')
            self.sock.bind(('192.168.1.93', self.port))
            self.sock.listen(5)
            # while True:
            connection, cli_address = self.sock.accept()
            #Accept a connection. The socket must be bound to an address and listening for connections.
            #The return value is a pair (connection, client address) where connection is a new socket object usable to send and receive data on the connection,
            #and client address is the address bound to the socket on the other end of the connection.

            print('Other player is connected at: {}'.format(cli_address))
            self.sock = connection
        # Connect to other player
        else:
            self.sock.connect((self.ip, self.port))
            self.my_turn = True

    def decode_move(self, move):
        return int(move[1])-1, LETTER_TO_INDEX[move[0]]

    def play(self):
        if self.my_turn:
            print('You are the first player')

        while not self.finished:
            if self.my_turn:
                self.my_turn = False # you play in this turn 
                move = input('Please enter your next move:') # take move like A4

                #encode a string to bytes in the send method of a socket connection
                self.sock.send(move.encode('ascii'))

                #socket.recv(1024) will read at most 1024 bytes, blocking if no data is waiting to be read
                hit_or_miss = self.sock.recv(1024)
                
                #decode() is a method specified in Strings in Python .
                #This method is used to convert from one encoding scheme, in which argument string is encoded to the desired
                #encoding scheme. 
                hit_or_miss = hit_or_miss.decode('ascii')
                
                print('Hit or miss: {}'.format(hit_or_miss))
                move = self.decode_move(move)
                if hit_or_miss == 'HIT':
                    self.op_board[move[0], move[1]] = 'H' #HIT symbol
                else:
                    self.op_board[move[0], move[1]] = 'X' # MISS case sembol on the board
            else:
                self.my_turn = True
                print('Waiting for opponent\'s move..')
                opponent_move = self.sock.recv(1024)
                opponent_move = opponent_move.decode('ascii')
                opponent_move = self.decode_move(opponent_move)
                print('Move by the opponent', opponent_move)
                if self.my_board[opponent_move[0], opponent_move[1]] != '': 
                    hit = 'HIT'
                    self.my_board[opponent_move[0], opponent_move[1]] += '-HIT' # write cell-HIT
                    self.num_of_hits += 1
                else:
                    hit = 'MISS'
                    self.my_board[opponent_move[0], opponent_move[1]] = 'X'
                self.sock.send(hit.encode('ascii'))

            self.print_board() #print board after each move
            if self.num_of_hits == 14: #total ship length 
                self.finished = True
                print('Game is over! Your opponent won the game!!!')

        self.sock.close() # close the TCP socket when game is finished
    

if __name__ == '__main__':
    ip = None
    if len(sys.argv) == 2:
        ip = sys.argv[1]
    battleship = Battleship(ip=ip)
    battleship.connect()
    battleship.ask_for_ships()
    battleship.play()
