import random
from string import ascii_uppercase

def pad(array, min_size, value = None):
    if len(array) >= min_size: 
    	return array

    difference = min_size - len(array)
    #array = array + [value] * difference
    for i in range(difference): 
        array.append(value)
    return array 

print(pad([1,2,3],0))

class GuessingGame:
    def __init__(self):
        """
        initialize answer as number as 0 , 1
        """
        self.answer_number = random.randint(0,2)
    def guess(self,user_guess: int):
        # guess method take in integer from user
        self.user_guess = user_guess
        # correct if users guess is the same as the answer else incorrect
        return 'correct' if self.user_guess == self.answer_number else 'incorrect'

# initialized Guessing game object as game
game = GuessingGame()
# printed the values of users guess
print(game.guess(int(input('please enter number: '))))

class boggle_board:
    def __init__(self):
        self.board = [
            [],
            [],
            [],
            []
            ]
    def shake(self):
        alphabet = [i for i in ascii_uppercase]
        self.board[0] = [random.choice(alphabet) for i in range(4)]
        self.board[1] = [random.choice(alphabet) for i in range(4)]
        self.board[2] = [random.choice(alphabet) for i in range(4)]
        self.board[3] = [random.choice(alphabet) for i in range(4)]
    
    def print_board(self):
        print(self.board)

board = boggle_board()
board.shake()
board.print_board()
        
