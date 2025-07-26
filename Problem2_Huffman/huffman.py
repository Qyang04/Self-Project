# import heapq
# from collections import defaultdict

# def build_huffman_tree(text):
#     freq = defaultdict(int)
#     for char in text:
#         freq[char] += 1
#     heap = [[weight, [char, ""]] for char, weight in freq.items()]
#     heapq.heapify(heap)
#     while len(heap) > 1:
#         lo = heapq.heappop(heap)
#         hi = heapq.heappop(heap)
#         for pair in lo[1:]:
#             pair[1] = '0' + pair[1]
#         for pair in hi[1:]:
#             pair[1] = '1' + pair[1]
#         heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
#     return heap[0][1:]

# if __name__ == "__main__":
#     text = input("Enter text to encode: ")
#     huffman_codes = build_huffman_tree(text)
#     print("Huffman Codes:")
#     for char, code in sorted(huffman_codes, key=lambda x: len(x[1])):
#         print(f"'{char}': {code}")

# Node class; also stores character and its frequency
class Node:
    def __init__(self, char=None, freq=0):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

nodes = []  # List of unique character Nodes

# Count occurences of characters in word, and append to nodes list
def calculate_frequencies(word):
    frequencies = {}
    for char in word:
        if char not in frequencies:
            freq = word.count(char)
            frequencies[char] = freq
            nodes.append(Node(char, freq))

def build_huffman_tree():
    while len(nodes) > 1:
        nodes.sort(
            key=lambda x: x.freq  # Sort all nodes based on freq, in ascending order
        )
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