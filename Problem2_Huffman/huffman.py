# TODO: Implement visualization of Huffman tree
# Reference: https://www.w3schools.com/dsa/dsa_ref_huffman_coding.php

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
        nodes.append(Node(unique_char, frequencies[unique_char]))


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

    # Recursively generate code, adding 0 for left and 1 for right (traversal)
    generate_huffman_codes(node.left, current_code + "0", codes)
    generate_huffman_codes(node.right, current_code + "1", codes)


def huffman_encoding(string):
    global nodes
    nodes = []
    calculate_frequencies(string)
    root = build_huffman_tree()
    huffman_codes = {}
    generate_huffman_codes(root, "", huffman_codes)
    return huffman_codes  # {char: code} dictionary format


"""
1. Get a reverse mapping of the conversion table; { code : character }, for efficient lookup (code_to_char)
2. Iterate through each bit in the encoded string, and append to current_code
3. At each iteration, check if current_code matches a huffman code
4. If it matches, append the associated character and reset current_code
5. Join all decoded characters into a string, and return
"""
def huffman_decoding(encoded_string, huffman_codes):
    current_code = ""  # Gathers bits from encoded string
    decoded_chars = []  # Stores decoded chars, to later be recombined

    # Get reverse mapping of huffman codes dictionary
    code_to_char = {v: k for k, v in huffman_codes.items()}

    for bit in encoded_string:
        current_code += bit
        if current_code in code_to_char:  # If the collected bits match a huffman code
            decoded_chars.append(code_to_char[current_code])
            current_code = ""

    return "".join(decoded_chars)


def display_results(word, codes, encoded_str, decoded_str):
    """
    Displays the Huffman coding results in a clean, organized format.
    """
    print("\n--- Huffman Coding Results ---")

    # --- 1. Create a readable, aligned breakdown of characters and codes ---
    # This avoids the fragile tab-based alignment.
    char_list = list(word)
    code_list = [codes[char] for char in char_list]

    # Calculate the proper width for each column for perfect alignment
    col_widths = [max(len(c), len(co)) for c, co in zip(char_list, code_list)]

    # Create formatted strings using f-string padding
    # The :^{width} syntax centers the text in a column of a given width
    char_row = " ".join(
        f"{char:<{width}}" for char, width in zip(char_list, col_widths)
    )
    code_row = " ".join(
        f"{code:<{width}}" for code, width in zip(code_list, col_widths)
    )

    print("Character-by-Character Breakdown:")
    print(f"  Word: {char_row}")
    print(f"  Code: {code_row}\n")

    # --- 2. Print the conversion table clearly ---
    print("Conversion Table:")
    # Sort items for consistent, predictable output
    for char, code in sorted(codes.items()):
        print(f"  '{char}' -> {code}")

    # --- 3. Print the final strings and a verification check ---
    print("\nFinal Output:")
    print(f"  Encoded String: {encoded_str}")
    print(f"  Decoded String: {decoded_str}")

    if word == decoded_str:
        print("\n✅ Verification successful: Original and decoded strings match.")
    else:
        print("\n❌ Verification failed: Strings do not match.")


def main():
    word = input("Enter text to encode: ")
    if not word:
        print("Error: Input text cannot be empty.")
        return

    huffman_codes = huffman_encoding(word)
    encoded_string = "".join(huffman_codes[char] for char in word)
    decoded_string = huffman_decoding(encoded_string, huffman_codes)

    display_results(word, huffman_codes, encoded_string, decoded_string)


if __name__ == "__main__":
    main()
