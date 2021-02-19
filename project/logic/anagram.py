from collections import Counter
import logging


def find_anagrams(letters, trie):
    letter_counts = Counter(letters)
    return anagram_engine(letter_counts, [], trie, len(letters))


def anagram_engine(letter_counts, path, root, word_length):
    words = []
    if None in root.keys():
        word = ''.join(path)
        words.append(word)
    for letter, this_dict in root.items():
        count = letter_counts.get(letter, 0)
        if count == 0:
            continue
        letter_counts[letter] = count - 1
        path.append(letter)
        for word in anagram_engine(letter_counts, path, this_dict, word_length):
            words.append(word)
        path.pop()
        letter_counts[letter] = count
    return words


def find_words(words, trie):
    logging.basicConfig(filename='demo.log', level=logging.DEBUG)

    response = {}
    response['status'] = True
    words_status = []
    for word in words:
        logging.info(f"{word}")
        word_status = {}
        word_status['word'] = word
        if(find_word(word, trie)):
            word_status['exist'] = True
        else:
            word_status['exist'] = False
            response['status'] = False
        words_status.append(word_status)
    response['details'] = words_status
    return response


def find_word(word, trie):
    if(None in trie.keys() and len(word) == 0):
        return True
    try:
        this_dict = trie[word[0]]
    except:
        return False
    if(find_word(word[1:], this_dict)):
        return True
    else:
        return False
