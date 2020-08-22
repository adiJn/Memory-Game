"""
Program implements a text-based version of the game memory where the user has to find matching pair of cards.
Numbers represent cards, and alphabets represent values of those cards.
The game terminates when all such pairs have been found. No. of guesses made and time elapsed is displayed.

CSCI150 Fall 2019 Test Project 2

Name: Aditya Jain
Section: A
"""
#----- Modules imported ------
import random
import time

#-----Constants-------
N_ROWS = 4
N_COLUMNS = 4
# Storing alphabet pairs eliminates need for a for loop to double alphabets
ALPHABET_PAIRS = list('AABBCCDDEEFFGGHHIIJJKKLLMMNNOOPPQQRRSSTTUUVVWWXXYY')  #Since only 25 pairs of letters allowed in the maximum case, Z is excluded
BLANK_LINES = 100

#-----Functions-----
def board_config():
    """
    Generate the board configuration as a mapping of digits to alphabets
    
    Returns:
      mapping: board configuration as dictionary mapping between digits and letters
    """
    n_letters = (N_ROWS * N_COLUMNS)   # number of letters of the alphabet on the board, assuming n_letters <= 50     
    mapping = {}
    
    for i in range(n_letters):
        mapping[i+1] = ALPHABET_PAIRS[i]
        
    return mapping


def print_board(objects_list):
    """
    Given list of objects, function prints them as a memory board
    
    Args:
      objects_list: list of objects to be printed on the board
    """
    while len(objects_list) > 0:
        board_display = ''
        
        for object in objects_list[:N_COLUMNS]:
            board_display = str(object)
            print(board_display.ljust(3), end = '')
            
        print()   # new line
        objects_list = objects_list[N_COLUMNS:] # change list to print next row
        
        
def obtain_guesses(input_digits):
    """
    Extract separate integer values from input
    
    Args:
      input_digits: user input of two numbers representing squares
      
    Returns:
      sq_1, sq_2: numbers for squares 1 and 2
    """
    sq_1 = int(input_digits.split()[0])  # convert to int since input is a string
    sq_2 = int(input_digits.split()[1])
    return sq_1, sq_2


def valid_print(sq_1, sq_2, mapping, digits_list):
    """
    Prints board and flips corresponding squares if guessed numbers have same underneath letters
    
    Args:
      sq_1, sq_2: number for squares 1 and 2
      mapping: board configuration as a dictionary
      digits_list: the list of digits to be printed on game board
    
    Return:
      valid_guesses: if the underneath letters match then guesses are stored in set
    """
    valid_guesses = set()
    
    if mapping[sq_1] == mapping[sq_2]:
        digits_list[sq_1-1] = mapping[sq_1] # e.g no. 4 will be at index (4-1 = 3) in the digits_list
        digits_list[sq_2-1] = mapping[sq_2] # Pull back the mapping value to the original list
        print_board(digits_list)
        valid_guesses.add(sq_1)
        valid_guesses.add(sq_2)
        
    else:
        print_board(digits_list) 
        
    return valid_guesses
        
        
def print_blank():
    """
    Prints 100 blank lines
    """
    for i in range(BLANK_LINES):
        print()

def guess_check(sq_1, sq_2, valid_guesses, digits_set):
    """
    Checks if input guesses have not already been correctly guessed, are not outside the digits on the board, and
    are not both the same.
    
    Args:
      sq_1, sq_2: number for squares 1 and 2
      valid_guesses: set of guesses that were correct 
      digits_list: the list of digits printed on game board
    """
    # Return true only if every single condition true; not possible to divide code into different lines
    return (sq_1 not in valid_guesses and sq_2 not in valid_guesses) and (sq_1 in digits_set and sq_2 in digits_set) and (sq_1 != sq_2)
        
        
def update_game(mapping = board_config()): # default random board configuration inputted
    """
    Run the game loop until all squares have been flipped
    
    Args:
      mapping: board_configuration as a dictionary, by default takes random mapping
      
    Returns:
      tuple containing no. of guesses made, and the underneath values
    """
    correct = False
    digits_list = list(mapping)
    digits_values = list(mapping.values())
    digits_updated = digits_list[:] # Deep copy to prevent aliasing
    print_board(digits_list)
    n_guesses = 0
    valid_guesses = set()
    
    while not correct:
        guesses = input('Guess two squares: ')
        sq_1, sq_2 = obtain_guesses(guesses)
        # Following loop entered only when some guess_check condition not met:
        while not guess_check(sq_1 , sq_2, valid_guesses, set(mapping)): 
            print('Invalid number(s).')
            guesses = input('Guess two squares: ')
            sq_1, sq_2 = obtain_guesses(guesses)  
            
        n_guesses += 1  # at this point, guess is valid
        digits_updated[sq_1-1] = mapping[sq_1]
        digits_updated[sq_2-1] = mapping[sq_2]
        
        if mapping[sq_1] == mapping[sq_2]:
            valid_guesses = valid_print(sq_1,sq_2, mapping,digits_updated)
            correct = digits_updated == digits_values # The only way to exit loop is to complete the game
            
        else:
            print_board(digits_updated)
            time.sleep(2)
            print_blank()
            valid_print(sq_1,sq_2, mapping, digits_list)
            digits_updated[sq_1-1] = sq_1 # don't store underneath letters in current version of game
            digits_updated[sq_2-1] = sq_2
            digits_list = digits_updated[:] # update to allow for any new pairings added to digits_updated
            
    return n_guesses, digits_updated  # digits_updated at this point is the same as mapping.values()
      

def play_game():
    """
    Runs memory game using update_game and prints no. of guesses and time taken to complete
    """
    start_time = time.time()
    n_guesses, game_answer = update_game()   
    time_elapsed = time.time() - start_time
    print_blank()  
    print('You win!')
    print_board(game_answer)  # print final game answer once again
    print('It took you ', n_guesses, ' guesses and ', int(time_elapsed), ' seconds.')   # we round time elapsed to preceding integer
    
    
if __name__ == '__main__': # played only when run
    play_game()

    
    
