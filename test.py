from project.logic.trie import make_trie
from project.logic.algorithm import Algorithm

trie_GB = make_trie("GB")

letters = "pietrus"
country = "gb"    
board = [[' ' for i in range(15)] for x in range(15)]

sixth_line = [' ', 'o', 'p', 'e', 'r', 'a', 't', 'i', 'o', 'n', 'a', 'l', ' ', ' ', ' ']
board[6] = sixth_line
# board[8] = sixth_line

# board[4][7] = 't'
# board[5][7] = 'r'
# board[6][7] = 'a'
# board[7][7] = 'v'
# board[8][7] = 'e'
# board[9][7] = 'r'
# board[10][7] = 's'
# board[11][7] = 'a'
# board[12][7] = 'l'

# board[5][0] = 's'
# board[6][0] = 't'

# board =  [([board[y][14 - x] for y in range(15)]) for x in range(15)]

for line in board:
    print(line)

algorithm = Algorithm(letters, board, country)
best_moves = algorithm.algorithm_engine(trie_GB)
quantity = int(best_moves['quantity'])
print(best_moves)
print(quantity)