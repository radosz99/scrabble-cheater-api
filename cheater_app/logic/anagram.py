from collections import Counter

from cheater_app.logger import logger


# TODO: big refactor needed
def find_anagrams(letters, trie):
    letters = [letter.lower() for letter in letters]
    letter_counts = Counter(letters)
    logger.info(f"Letters counts = {letter_counts}, looking for anagrams")
    anagrams = anagram_engine(letter_counts, [], trie, len(letters))
    anagrams = [anagram for anagram in anagrams if len(anagram) > 1]
    logger.info(f"Found {len(anagrams)} anagrams")
    return anagrams


def anagram_engine(letter_counts, path, root, word_length):
    anagrams = []
    if None in root.keys():
        word = list(path)
        anagrams.append(word)
    for letter, this_dict in root.items():
        count = letter_counts.get(letter, 0)
        if count == 0:
            continue
        letter_counts[letter] = count - 1
        path.append(letter)
        for word in anagram_engine(letter_counts, path, this_dict, word_length):
            anagrams.append(word)
        path.pop()
        letter_counts[letter] = count
    return anagrams


def validate_words(words, trie):
    details = [{'word': word, "exist": True if find_word(word, trie) else False} for word in words]
    return {'details': details, 'status': True if all([status['exist'] for status in details]) else False}


def find_word(word, trie):
    if None in trie.keys() and len(word) == 0:
        return True
    try:
        this_dict = trie[word[0]]
        return True if find_word(word[1:], this_dict) else False
    except (KeyError, IndexError):
        return False

