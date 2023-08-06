# Code for the Trie Data Structure.

import dill

class node():
    def __init__(self, char, parent, end=False):
        # Initialize all the variables used by a Trie Node.
        self.character = char  # The letter this node represents.
        self.parent = parent  # Pointer to the parent node, which is needed when removing keywords from the Trie.
        self.links = [None]*26  # There are 26 letters in the alphabet.
        self.ending = end  # If this node marks the end of a word.


class trie_class():
    def __init__(self):
        self.alpha = {}  # Alphabet and corresponding Index.
        for i in range(97,123):
            self.alpha[chr(i)] = i-97
        self.data = node('ROOT', 'is_root')  # The root node of the Trie.

    def add_keyword(self, word):
        # Adds any input string into the Trie.

        curr_index_value = self.data
        for letter in range(len(word)):
            letter_index = self.alpha[word[letter]]  # Converts character to an index from 0 to 25.
            if curr_index_value.links[letter_index] is None:
                if letter < len(word)-1:
                    # Adds node that is not end of word.
                    curr_index_value.links[letter_index] = node(word[letter], curr_index_value)
                else:
                    # Adds node that is end of word.
                    curr_index_value.links[letter_index] = node(word[letter], curr_index_value, True)
            # Check if word was already added.
            elif letter == len(word)-1 and curr_index_value.links[letter_index].ending:
                return f"The word '{word}' is already in the Trie"
            curr_index_value = curr_index_value.links[letter_index]
        return f"The word '{word}' was added to the Trie"

    def remove_keyword(self, word):
        # Remove any input string from the Trie, given it exists.

        curr_index_value = self.reach_node_required(self.data, word)
        # Return if word to remove does not exist.
        if type(curr_index_value) is str:
            return curr_index_value
        # If word never existed.
        if not curr_index_value.ending:
            return f"'{word}' was not in the Trie"
        # Set node ending to false if it has links to other nodes.
        links = 0
        for link in curr_index_value.links:
            links += 1 if link is not None else 0
        if links > 0:
            curr_index_value.ending = False
        # If node has no links, delete unused nodes.
        else:
            while True:
                if curr_index_value.character == 'ROOT':
                    break  # Break if ROOT is reached
                letter_index = self.alpha[curr_index_value.character]
                curr_index_value = curr_index_value.parent
                curr_index_value.links[letter_index] = None
                links = 0
                for link in curr_index_value.links:
                    links += 1 if link is not None else 0
                if links > 0:
                    break
        return f"The word '{word}' was removed from the Trie"

    def keyword_exists(self, word):
        # Checks if an input string is stored in the Trie.

        curr_index_value = self.reach_node_required(self.data, word)
        try:
            if curr_index_value.ending:
                return f"The word '{word}' exists in the Trie"
            return f"The word '{word}' does not exist in the Trie"
        except AttributeError:
            # Handles error when returned value is a string saying "This word does not exist"
            return curr_index_value

    def reach_node_required(self, node, prefix):
        # Finds the node for a certain word/prefix.

        for letter in range(len(prefix)):
            # For each letter, it further traverses down the Trie unless the needed letter does not exist.
            letter_index = self.alpha[prefix[letter]]
            if node.links[letter_index] is None:
                return f"The word {prefix} does not exist in the Trie"
            node = node.links[letter_index]
        return node

    def autocomplete(self, prefix):
        # Returns all strings in Trie that contain the prefix.

        def find_all_words(node, prefix):
            # Perform depth first search to get all words with required prefix.

            found_words = []
            for link in node.links:
                if link is not None:
                    if link.ending:
                        found_words.append(prefix + link.character)
                    found_words += find_all_words(link, prefix + link.character)
            return found_words

        words_with_prefix = []
        curr_index_value = self.reach_node_required(self.data, prefix)

        # Check if result was not error.
        if type(curr_index_value) is str:
            return words_with_prefix

        if curr_index_value.ending:
            words_with_prefix.append(prefix)
        words_with_prefix += find_all_words(curr_index_value, prefix)
        return words_with_prefix

    def print(self, node=False, indentation=0):
        # Returns a readable format of the Trie

        # If node not provided, use root node.
        if node is False:
            node = self.data

        output = [""]  # Array needs to be used so can be accessed in loop function

        def loop(node, indentation=0):
            for link in node.links:
                if link is not None:
                    output[0] += ' ' * indentation + link.character + "\n"
                    loop(link, indentation=indentation+2)

        loop(node)
        return output[0]


