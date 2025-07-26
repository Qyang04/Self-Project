#TODO: Implement visualization of Huffman tree

# Node class; also stores character and its frequency
class Node:
    def __init__(self, char=None, freq=0):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

nodes = []  # Stores nodes for building Huffman tree

# Count occurences of characters in word, and append to nodes list
def calculate_frequencies(word):
    frequencies = {}
    for char in word:
        if char in frequencies:
            frequencies[char] += 1
        else:
            frequencies[char] = 1
    for unique_char in frequencies:
        nodes.append(Node(unique_char, frequencies[char]))
        
# Manual impl of bubble sort that sorts Nodes based on freq value
def bubble_sort_nodes(list):
    n = len(list)
    for i in range(n):
        for j in range(0, n - i - 1):
            if list[j].freq > list[j + 1].freq:
                list[j], list[j + 1] = list[j + 1], list[j]

def build_huffman_tree():
    while len(nodes) > 1:
        bubble_sort_nodes(nodes)  # Sort all nodes based on freq, in ascending order
        left = nodes.pop(0)
        right = nodes.pop(0)

        merged = Node(freq=left.freq + right.freq)
        merged.left = left
        merged.right = right

        nodes.append(merged)

    return nodes[0]  # Return the root

# Traverses Huffman tree to generate Huffman codes for each char
def generate_huffman_codes(node, current_code, codes):
    if not node:
        return

    if node.char:
        codes[node.char] = current_code

    # Recursively traverse tree, adding 0 and 1 to code for left and right respectively
    generate_huffman_codes(node.left, current_code + "0", codes)
    generate_huffman_codes(node.right, current_code + "1", codes)
    
def huffman_encoding(word):
    global nodes
    nodes = []
    calculate_frequencies(word)
    root = build_huffman_tree()
    codes = {}
    generate_huffman_codes(root, "", codes)
    return codes

if __name__ == "__main__":
    word = input("Enter text to encode: ")
    codes = huffman_encoding(word)
    encoded_string = '\t'.join(codes[char] for char in word)
    
    print(f"Word: {'\t\t'} {'\t'.join(char for char in word)}")
    print(f"Huffman code: {'\t'} {encoded_string}")
    print(f"Conversion table: {codes}")