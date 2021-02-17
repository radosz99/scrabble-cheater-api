from .anagram import find_anagrams
from enum import Enum  
import logging

class Algorithm:
    def __init__(self, letters, board, country):
        self.letters = [x.lower() for x in letters]
        self.board = board
        pattern_finder = PatternFinder()
        self.pattern_board = pattern_finder.create_patterns(self.board)
        self.country = country

    def algorithm_engine(self,trie):
        sorted_list_of_valid_words=self.get_valid_words(trie)
        json_word = self.convert_to_json(sorted_list_of_valid_words)
        return json_word

    def convert_to_json(self, words):
        word_list = []
        for word in words:
            word_json = {}
            coords = word[0][1]
            word_json['word'] = word[0][0]
            word_json['points'] = word[1]
            if(coords[5]==Orientation.vertical):
                x = coords[1] - coords[3]
                y = coords[2]
                ch_y = chr(65 + y)
                word_json['coordinate'] = str(ch_y) + str(x)
            elif(coords[5]==Orientation.horizontal):
                x = coords[1]
                y = coords[2] - coords[3]
                ch_y = chr(65 + y)
                word_json['coordinate'] = str(x) + str(ch_y)
                
            word_list.append(word_json)

        words_in_json = {}
        words_in_json['words'] = word_list
        words_in_json['quantity'] = len(word_list)
        return words_in_json

    def get_valid_words(self, trie):
        info = self.get_letters_for_anagram()
        board_letters = info[0]
        brigdes=info[1]
        #znajdowanie wszystkich anagramow
        anagrams = find_anagrams(str(self.letters) + board_letters,trie)
        #wybor wszystkich anagramow mogacych pasowac do patternow, wstepna selekcja
        valid_anagrams = self.find_probably_valid_words(anagrams=anagrams, letters=str(self.letters), board_letters=board_letters, brigdes=brigdes)
        #znajdowanie wyrazow rzeczywiscie pasujacych do patternow, ostateczna selekcja
        list_of_valid_words = self.find_certainly_valid_words(valid_anagrams)
        #sortowanie listy od najlepszych ruchow (najwiecej punktowanych)
        sorted_list_of_valid_words = sorted(list_of_valid_words, key=lambda tup: tup[1])

        return sorted_list_of_valid_words

    def check_if_valid(self,word):
        list_of_possible_patterns=[]
        _word = word
        for char in self.letters:
            position = _word.find(char)
            if(position!=-1):
                help_word = _word[0 : position ] + _word[position + 1 : len(_word)]
                _word = help_word
        positions=[]
        if(len(_word)!=0):
            for char in _word:
                index = word.find(char)
                positions.append(index)
        else:
            return ''

        for pattern in self.pattern_board:
            if(str(pattern[0])==_word):
                if(len(_word)==2):
                    if(pattern[3]>=positions[0] and len(word)<=9):
                        if(pattern[4]>=(len(word)-positions[1]-1)):
                            list_of_possible_patterns.append((word, (pattern[0],pattern[1],pattern[2],positions[0], pattern[4], pattern[5], pattern[6])))
                if(len(_word)==1):
                    if(pattern[3]==positions[0]):
                        if(pattern[4]>=(len(word)-positions[0]-1)):
                            list_of_possible_patterns.append((word, pattern))
 
        if(len(list_of_possible_patterns)!=0):
            return list_of_possible_patterns
        else:
            return ''

    def find_certainly_valid_words(self, sorted_by_length):
        word=''
        list_of_valid_words=[]
        counter=1
        while(counter!=len(sorted_by_length)+1):
            word_to_check=sorted_by_length[len(sorted_by_length)-counter]
            words = self.check_if_valid(word_to_check)  
            for word in words:
                if(word!=''):
                    result = self.evaluate_move(word)
                    list_of_valid_words.append((word,result))
            counter=counter+1

        return list_of_valid_words

    def find_probably_valid_words(self, anagrams, letters, board_letters, brigdes):
        max_letters_from_board_to_connect = 2 #maksymalny most, czyli przewiduje max 2
        new_anagrams = []

        for anagram in anagrams:
            new_anagram=anagram
            _board_letters=board_letters
            whether_letter=False
            help_counter=0
            letters_find_in_both_place=[]
            for char in letters:
                index = new_anagram.find(char)
                #sprawdzenie czy znak znajduje sie w literach uzytkownika
                if(index!=-1): 
                    whether_letter=True
                    index_board = _board_letters.find(char)
                    #sprawdzenie czy znak znajduje sie w literach dostepnych na planszy, jesli tak to usuwany jest z dostepnych liter na planszy
                    if(index_board==-1):
                        help_anagram = new_anagram[0 : index ] + new_anagram[index + 1 : len(new_anagram)]
                        new_anagram = help_anagram
                    else:
                        letters_find_in_both_place.append(char)
                        help_counter=help_counter+1
                        help_board_letters = _board_letters[0 : index_board ] + _board_letters[index_board + 1 : len(_board_letters)]
                        _board_letters = help_board_letters
            #pierwszy warunek to, sprawdzenie czy w slowie jest wiecej niz 2 znaki spoza liter uzytkownika, czyli z planszy (mostek = 2 litery, kat prosty = 1 litera)
            #drugi warunek to sprawdzenie czy w slowie znajduja sie litery z planszy (jesli nie to string mialby dlugosc 0, czyli zawieral jedynie litery uzytkownika, co jest niedopuszczalne)
            #trzeci warunek to sprawdzenie czy zostala usunieta chociaz jedna literka (czyli, ze slowo zawiera chociaz jedna litere uzytkownika)
            if(len(new_anagram)<=max_letters_from_board_to_connect+help_counter and len(new_anagram)>0 and whether_letter==True):
                #usuniecie tych co znalazly sie w obu miejscach w celach walidacji
                for ch in letters_find_in_both_place:
                    index = new_anagram.find(ch)
                    if(index!=-1):
                        help_new_anagram = new_anagram[0 : index ] + new_anagram[index + 1 : len(new_anagram)]
                        new_anagram = help_new_anagram
                #sprawdzenie czy pasuje do mostkow
                if(len(new_anagram)==2):
                    for key in brigdes:
                        if(new_anagram==key):
                            position1 = anagram.find(str(key)[0])
                            position2 = anagram.find(str(key)[1])
                            if(position2-position1==brigdes[key]):
                                new_anagrams.append(anagram)
                                break
                elif(len(new_anagram)<2):
                    new_anagrams.append(anagram)

        sorted_by_length = sorted(new_anagrams, key=len)
        return sorted_by_length
             
    def evaluate_move(self, word_with_pattern):
        coords = word_with_pattern[1]
        word = word_with_pattern[0]
        sum=0
        bonus=0
        if(len(word)-len(coords[0])==7):
            bonus=50
        multiplier=1
    
        if(coords[5]==Orientation.vertical):
            for x in range (len(word)):
                if(len(coords[0])==2):
                    info = self.get_field_value(word[x], coords[1]+x-coords[3],coords[2])
                    
                    if(x==coords[3] or x==(coords[3]+coords[6])):
                        sum=sum+info[1]
                    else:
                        sum=sum+int(info[0]*info[1])
                        multiplier=int(multiplier*int(info[2]))
                else:
                    info = self.get_field_value(word[x], coords[1]+x-coords[3],coords[2])
                    if(x==coords[3]):
                        sum=sum+info[1]
                    else:
                        sum=sum+int(info[0]*info[1])
                        multiplier=int(multiplier*int(info[2]))

        if(coords[5]==Orientation.horizontal):
            for x in range (len(word)):
                if(len(coords[0])==2):
                    info = self.get_field_value(word[x], coords[1],coords[2]+x-coords[3])
                    if(x==coords[3] or x==(coords[3]+coords[6])):
                        sum=sum+info[1]
                    else:
                        sum=sum+int(info[0]*info[1])
                        multiplier=int(multiplier*int(info[2]))
                else:
                    info = self.get_field_value(word[x], coords[1],coords[2]+x-coords[3])
                    if(x==coords[3]):
                        sum=sum+info[1]
                    else:
                        sum=sum+int(info[0]*info[1])
                        multiplier=int(multiplier*int(info[2]))
        return sum*multiplier+bonus
                            
    def get_field_value(self, char, x,y):
        word_multiplier=1
        letter_multiplier=1
        letter_value = self.get_char_value(char)

        if(((x==1 or x==13)and (y==1 or y==13)) or ((x==2 or x==12) and (y==2 or y==12)) or ((x==3  or x==11) and (y==3 or y==11)) or ((x==4 or x==10) and (y==4 or y==10)) or (x == 7 and y ==7)):
            word_multiplier=2
        if(((x==0 or x==14) and (y==0 or y==7 or y==14)) or (x==7 and (y==0 or y==14))):
            word_multiplier=3

        if(((x==5 or x==9) and (y==1 or y==5 or y==9 or y==13)) or ((x==1 or x==13) and (y==5 or y==9))):
            letter_multiplier=3
        if(((x==0 or x==7 or x==14) and (y==3 or y==11)) or ((x==3 or x==11) and (y==0 or y==7 or y==14))
            or((x==2 or x==6 or x==8 or x==12) and (y==6 or y==8)) or((y==2 or y==6 or y==8 or y==12) and (x==6 or x==8))):
            letter_multiplier=2

        return letter_multiplier,letter_value, word_multiplier

    def get_char_value(self,char):
        # if(self.country=='PL'):
        #     if(char=='a' or char=='e' or char=='i' or char=='n' or char=='o' or char=='r' or char=='s' or char=='w' or char=='z'):
        #         return 1
        #     if(char=='c' or char=='d' or char=='k' or char=='l' or char=='m' or char=='p' or char=='t' or char=='y'):
        #         return 2
        #     if(char=='b' or char=='g' or char=='h' or char=='j' or char=='ł' or char=='u'):
        #         return 3
        #     if(char=='ą' or char=='ę' or char=='f' or char=='ó' or char=='ś' or char=='ż'):
        #         return 5
        #     if(char=='ć'):
        #         return 6
        #     if(char=='ń'):
        #         return 7
        #     if(char=='ź'):
        #         return 9

        # if(self.country=='GB'):
        if(char=='a' or char=='e' or char=='i' or char=='n' or char=='o' or char=='r' or char=='s' or char=='t' or char=='u' or char=='l'):
            return 1
        if(char=='g' or char=='d'):
            return 2
        if(char=='b' or char=='c' or char=='m' or char=='p'):
            return 3
        if(char=='h' or char=='v' or char=='w' or char=='y' or char=='f'):
            return 4
        if(char=='k'):
            return 5
        if(char=='j' or char=='x'):
            return 8
        if(char=='q' or char=='z'):
            return 10
        return 1


    def get_letters_for_anagram(self):
        board_letters = ''
        bridges = {}
        for pattern in self.pattern_board:
            if(len(pattern[0])==2):
                bridges[pattern[0]]=pattern[6]
            elif(len(pattern[0])==1):
                board_letters=board_letters+pattern[0]

        
        letters = "".join(set(board_letters))
        


        print(letters)
        for key in bridges:
            position1 = letters.find(key[0])
            position2 = letters.find(key[1])
            if(position1==-1 and position2==-1):
                letters.join(key[0])
                letters.join(key[1])
            elif(position1==-1):
                letters.join(key[0])
            elif(position2==-1):
                letters.join(key[1])
        print(letters)
        return letters, bridges
        

class PatternFinder:
    def __init__(self):
        pass

    def create_patterns(self, board):
        pattern_board=[]
        vertical_patterns = self.get_right_angle_patterns(self._transpose_board(board),Orientation.vertical)
        horizontal_patterns = self.get_right_angle_patterns(board, Orientation.horizontal)
        pattern_board.extend(vertical_patterns)
        pattern_board.extend(horizontal_patterns)
        pattern_board.extend(self.get_bridge_patterns(vertical_patterns, self._transpose_board(board)))
        pattern_board.extend(self.get_bridge_patterns(horizontal_patterns, board))
        return pattern_board
        

    def get_bridge_patterns(self,pattern_board, board):
        bridge_patterns=[]
        for pattern in pattern_board:
            char = pattern[0]

            for sub_pattern in pattern_board:
                row=pattern[1]
                col=pattern[2]
                sub_row=sub_pattern[1]
                sub_col=sub_pattern[2]
                if(sub_row>row+1 and sub_col==col and sub_pattern[5]== Orientation.vertical and ((sub_pattern[3]+pattern[4]>=sub_row-row-1)or(sub_row==row+2))):
                    cont=True
                    if(sub_row==row+2):
                        if(board[row+1][col-1]!=' '):
                            cont=False
                        elif(col+1<15):
                            if(board[row+1][col+1]!=' '):
                                cont=False   
                    for i in range(sub_row-row-1):
                        if(board[row+1+i][col]!=' '):
                            cont=False
                    if(cont==False):
                        continue
                    difference = sub_row-row
                    if(pattern[3]<=7-(difference-1)):
                        left_shift=pattern[3]
                        right_shift=7-(difference-1)-left_shift
                        if(right_shift>sub_pattern[4]):
                            right_shift=sub_pattern[4]   
                        bridge_pattern=(char+sub_pattern[0],row,col,left_shift,right_shift,Orientation.vertical,difference)
                        bridge_patterns.append(bridge_pattern)

                if(sub_col>col+1 and sub_row==row and sub_pattern[5]==Orientation.horizontal and ((sub_pattern[3]+pattern[4]>=sub_col-col-1) or(sub_col==col+2))):
                    cont=True
                    if(sub_col==col+2):
                        if(board[row-1][col+1]!=' '):
                            cont=False
                        elif(row+1<15):
                            if(board[row+1][col+1]!=' '):
                                cont=False                           
                    for i in range(sub_col-col-1):
                        if(board[row][col+1+i]!=' '):
                            cont=False
                    if(cont==False):
                        continue
                    difference = sub_col-col
                    if(pattern[3]<=7-(difference-1)):
                        left_shift=pattern[3]
                        right_shift=7-(difference-1)-left_shift
                        if(right_shift>sub_pattern[4]):
                            right_shift=sub_pattern[4]   
                        bridge_pattern=(char+sub_pattern[0],row,col,left_shift,right_shift,Orientation.horizontal,difference)
                        bridge_patterns.append(bridge_pattern)

        return list(set(bridge_patterns))


    def get_right_angle_patterns(self, board, node_orient):
        pattern_board=[]
        for x in range(15):
            for y in range(15):
                if(board[x][y]!=' '):
                    left=False
                    right=False
                    empty_left_side=0
                    empty_right_side=0
                    check=False
                    if(y+1>14):
                        check=True
                    elif(board[x][y+1]==' '):
                        check=True
                    if((board[x][y-1]==' ' or y==0)and check):
                        left = self.check_whether_left_is_possible(x,y,board)
                        right = self.check_whether_right_is_possible(x,y,board)
                        
                        if(left==True):
                            empty_left_side=1
                        if(right==True):
                            empty_right_side=1

                        if(empty_left_side!=1 and empty_right_side!=1):
                            continue

                        if(empty_left_side==1):
                            empty_left_side = self._get_empty_cells_on_the_left(x,y,board)

                        if(empty_right_side==1):
                            empty_right_side = self.get_empty_cells_on_the_right(x,y,board)

                        help_index_right = empty_right_side
                        help_index_left = empty_left_side
                        #maksymalnie 7 liter mozna wlozyc nawet jesli bedzie wiecej miejsca
                        if(empty_right_side>7):
                            help_index_right=7
                        if(empty_left_side>7):
                            help_index_left=7
                        
                        pattern_board.extend(self.make_patterns(help_index_left, help_index_right, node_orient, board, x,y))

        return pattern_board

    def check_whether_left_is_possible(self, x, y, board):
        if(x!=14 and x!=0):
            if(board[x-1][y-1]==' ' and board[x+1][y-1]==' '):
                if(board[x][y-2]==' ' or y-1==0):
                    return True
        elif(x==14):
            if(y-1>=0):
                if(board[x-1][y-1]==' '):
                    if(board[x][y-2]==' ' or y-1==0):
                        return True
        elif(x==0):
            if(board[x+1][y-1]==' '):
                if(board[x][y-2]==' ' or y-1==0):
                    return True
        return False

    def check_whether_right_is_possible(self,x,y,board):
        if(x!=14 and x!=0 and y!=14):
            if(board[x-1][y+1]==' ' and board[x+1][y+1]==' '):
                if(y+1==14):
                    return True
                elif(board[x][y+2]==' '):
                    return True
        elif(x==14):
            if(y<14):
                if(board[x-1][y+1]==' '):
                    if(y+1==14):
                        return True
                    elif(board[x][y+2]==' '):
                        return True
        elif(x==0 and y!=14):
            if(board[x+1][y+1]==' '):
                if(y+1==14):
                    return True
                elif(board[x][y+2]==' '):
                    return True
        return False


    def _transpose_board(self, board):
        return [([board[y][14 - x] for y in range(15)]) for x in range(15)]    

    def _get_empty_cells_on_the_left(self, x, y, board):
        empty_cells_on_left = 0
        while(self._check_if_left_cell_is_available(board, x, y - empty_cells_on_left)):
            empty_cells_on_left += 1
        return empty_cells_on_left

    def _check_if_left_cell_is_available(self, board, x, y):
        if(y == 0):
            return False
        top_not_adjacent = self._check_if_not_adjacent_to_top(board, x, y - 1)
        bottom_not_adjacent = self._check_if_not_adjacent_to_bottom(board, x, y - 1)
        left_not_adjacent = self._check_if_not_adjacent_to_left(board, x, y - 1)
        return top_not_adjacent and bottom_not_adjacent and left_not_adjacent

    def _check_if_not_adjacent_to_top(self, board, x, y):
        if(self._check_if_cell_is_in_top_row(x)): return True
        elif(self._check_if_cell_on_the_top_is_empty(board, x, y)): return True
        else: return False

    def _check_if_cell_on_the_top_is_empty(self, board, x, y):
        if(board[x - 1][y] == ' '): return True
        else: return False

    def _check_if_cell_is_in_top_row(self, x):
        if(x==0): return True
        else: return False

    def _check_if_not_adjacent_to_bottom(self, board, x, y):
        if(self._check_if_cell_is_in_bottom_row(x)): return True
        elif(self._check_if_cell_on_the_bottom_is_empty(board, x, y)): return True
        else: return False

    def _check_if_cell_on_the_bottom_is_empty(self, board, x, y):
        if(board[x + 1][y] == ' '): return True
        else: return False

    def _check_if_cell_is_in_bottom_row(self, x):
        if(x == 14): return True
        else: return False

    def _check_if_not_adjacent_to_left(self, board, x, y):
        if(self._check_if_cell_is_in_left_column(y)): return True
        elif(self._check_if_cell_on_the_left_is_empty(board, x, y)): return True
        else: return False

    def _check_if_cell_is_in_left_column(self, y):
        if(y == 0): return True
        else: return False

    def _check_if_cell_on_the_left_is_empty(self, board, x, y):
        if(board[x][y - 1] == ' '): return True
        else: return False

    def _check_if_not_adjacent_to_right(self, board, x, y):
        if(self._check_if_cell_is_in_right_column(y)): return True
        elif(self._check_if_cell_on_the_right_is_empty(board, x, y)): return True
        else: return False

    def _check_if_cell_is_in_right_column(self, y):
        if(y == 14): return True
        else: return False

    def _check_if_cell_on_the_right_is_empty(self, board, x, y):
        if(board[x][y + 1] == ' '): return True
        else: return False

    def _check_if_right_cell_is_available(self, board, x, y):
        if(y == 14):
            return False
        top_not_adjacent = self._check_if_not_adjacent_to_top(board, x, y + 1)
        bottom_not_adjacent = self._check_if_not_adjacent_to_bottom(board, x, y + 1)
        right_not_adjacent = self._check_if_not_adjacent_to_right(board, x, y + 1)
        return top_not_adjacent and bottom_not_adjacent and right_not_adjacent

    def get_empty_cells_on_the_right(self, x, y, board):
        empty_cells_on_right = 0
        while(self._check_if_right_cell_is_available(board, x, y + empty_cells_on_right)):
            empty_cells_on_right += 1
        return empty_cells_on_right

    def get_coordinates_according_to_board_orientation(self, orientation, x, y):
        if(orientation == Orientation.horizontal):
            return x, y
        elif(orientation == Orientation.vertical):
            return y, 14 - x

    def make_patterns(self, empty_left, empty_right, orientation, board, x, y):
        pattern_board=[]
        empty_left = 7 if empty_left > 7 else empty_left
        for i in range (empty_left + 1):
            free_cells_on_right = empty_right if (i + empty_right <= 7) else 7 - i
            real_x, real_y = self.get_coordinates_according_to_board_orientation(orientation, x, y)
            pattern_board.append((board[x][y].lower(), real_x, real_y, i, free_cells_on_right, orientation))
        return pattern_board

class Orientation(Enum):
    horizontal = 1
    vertical = 2