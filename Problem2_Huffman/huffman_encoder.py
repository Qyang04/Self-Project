# Reference: https://www.w3schools.com/dsa/dsa_ref_huffman_coding.php

# Node class; stores a key(char) and its frequency
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
# Bubble sort algorithm is chosen, to decrease code complexity
def bubble_sort_nodes(list):
    n = len(list)
    for i in range(n):
        for j in range(0, n - i - 1):
            if list[j].freq > list[j + 1].freq:
                list[j], list[j + 1] = list[j + 1], list[j]


def build_huffman_tree():
    while len(nodes) > 1:
        bubble_sort_nodes(nodes)  # Sort nodes in ascending order
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
    huffman_codes = {}  # {char : code} dictionary format
    generate_huffman_codes(root, "", huffman_codes)
    return root, huffman_codes  # Returns root for visualization class


def huffman_decoding(encoded_string, huffman_codes):
    """
    Decoding:
    1. Get a reverse mapping of the conversion table; {code : char}, for efficient lookup
    2. Iterate through each bit in the encoded string, and append to current_code
    3. At each iteration, check if current_code matches a huffman code
    4. If it matches, append the associated character to decoded_chars, and reset current_code
    5. Join all decoded characters into a string, and return
    """
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


def display_results(word, codes, encoded_str, decoded_str, show_table=True, show_results=True, show_analysis=True):
    """
    Displays the Huffman coding results in a polished, table-based format,
    with sections that can be toggled on or off.
    """
    print("\n\n╔═══════════════════════════════╗")
    print("║   Huffman Coding Analysis     ║")
    print("╚═══════════════════════════════╝")

    # --- 1. Frequency and Code Table ---
    if show_table:
        print("\n--- Character Frequencies & Codes ---\n")
        if not codes:
            print("No character codes to display.")
        else:
            frequencies = {char: word.count(char) for char in sorted(codes.keys())}
            char_w = max([len(c) for c in frequencies.keys()] + [len("Char")]) + 2
            freq_w = max([len(str(f)) for f in frequencies.values()] + [len("Freq")])
            code_w = max([len(c) for c in codes.values()] + [len("Code")])
            
            print(f"┌─{'─'*char_w}─┬─{'─'*freq_w}─┬─{'─'*code_w}─┐")
            print(f"│ {'Char':<{char_w}} │ {'Freq':<{freq_w}} │ {'Code':<{code_w}} │")
            print(f"├─{'─'*char_w}─┼─{'─'*freq_w}─┼─{'─'*code_w}─┤")
            for char, freq in sorted(frequencies.items()):
                code = codes.get(char, "N/A")
                print(f"│ '{char}'{' '*(char_w-3)} │ {freq:<{freq_w}} │ {code:<{code_w}} │")
            print(f"└─{'─'*char_w}─┴─{'─'*freq_w}─┴─{'─'*code_w}─┘")

    # --- 2. Results & Verification ---
    if show_results:
        print("\n\n--- Encoding & Decoding Results ---\n")
        print(f"Original String:  {word}")
        print(f"Encoded String:   {encoded_str}")
        print(f"Decoded String:   {decoded_str}")

    # --- 3. Compression Analysis ---
    if show_analysis:
        print("\n\n--- Compression Analysis ---\n")
        original_bits = len(word) * 8
        encoded_bits = len(encoded_str)
        if original_bits > 0:
            savings = (1 - (encoded_bits / original_bits)) * 100
            savings_str = f"{savings:.2f}%"
        else:
            savings_str = "N/A"
        print(f"Original Size:    {original_bits} bits ({len(word)} chars x 8 bits)")
        print(f"Encoded Size:     {encoded_bits} bits")
        print(f"Space Savings:    {savings_str}")

    # --- 4. Final Verification Status ---
    print("\n" + "─" * 40)
    if word == decoded_str:
        print("✅ Verification: SUCCESS! Original and decoded strings match.")
    else:
        print("❌ Verification: FAILED! Strings do not match.")
    print("─" * 40 + "\n")


def main():
    """
    Provides a command-line interface to run Huffman coding on test cases
    or custom user input with configurable output.
    """
    test_cases = [
        "hello world",      # Simple string with varied frequencies
        "hi hi hi hilda",   # Characters with similar frequencies
        "abcdefg",          # No repeated characters (balanced tree)
        "aaaaaaaaaaabbc",   # Highly skewed frequencies
        "",                 # Edge case: empty string
        "a",                # Edge case: single character
        "bbbbbb",           # Edge case: one unique character
        "0101010101",       # Edge case: two unique characters
        "!@#$%^&*()_+",     # Special characters
        "a b\tc\nd",        # Whitespace characters
    ]

    # Check if the visualizer is available (not in-use)
    visualizer_available = False
    try:
        from visualize_huffman import HuffmanVisualizer
        visualizer_available = True
    except ImportError:
        pass # Visualizer not found, will not be offered as an option.

    while True:
        print("\n╔══════════════════════════════╗")
        print("║   Huffman Coding Toolkit     ║")
        print("╚══════════════════════════════╝")
        print("1. Run Predefined Test Cases")
        print("2. Encode Custom Text")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            run_test_suite(test_cases)
        elif choice == '2':
            # --- Configure Custom Run ---
            print("\n--- Output Configuration ---")
            show_table = input("Show Huffman table? (y/n): ").lower() == 'y'
            show_results = input("Show full encoding/decoding results? (y/n): ").lower() == 'y'
            show_analysis = input("Show compression analysis? (y/n): ").lower() == 'y'
            show_viz = False
            if visualizer_available:
                show_viz = input("Generate tree visualization? (y/n): ").lower() == 'y'
            
            # --- Get Input and Run ---
            word = input("\nEnter text to encode: ")
            if not word:
                print("\n❌ Error: Input text cannot be empty.")
                continue

            if len(set(word)) <= 1:
                print("\n✅ Encoding complete, but no complex tree was built for a single unique character.")
                root, huffman_codes = huffman_encoding(word) # Still run encoding
                encoded_string = "".join(huffman_codes.get(char, '') for char in word)
                decoded_string = huffman_decoding(encoded_string, huffman_codes)
                display_results(word, huffman_codes, encoded_string, decoded_string, show_table, show_results, show_analysis)
                if show_viz:
                    print("(Visualization skipped for single-character inputs)")
                continue

            # --- Process and Display ---
            root, huffman_codes = huffman_encoding(word)
            encoded_string = "".join(huffman_codes[char] for char in word)
            decoded_string = huffman_decoding(encoded_string, huffman_codes)
            display_results(word, huffman_codes, encoded_string, decoded_string, show_table, show_results, show_analysis)

            if show_viz:
                print("\nLaunching visualization window...")
                HuffmanVisualizer(root)

        elif choice == '3':
            print("Exiting toolkit. Goodbye! 👋")
            break
        else:
            print("\nInvalid choice, please try again.")


def run_test_suite(test_cases):
    """
    Runs the Huffman coding algorithm on a list of test strings and
    prints a summary of the results.
    """
    print("\n--- Running Test Suite ---")
    total_passed = 0
    total_skipped = 0
    
    for i, test_str in enumerate(test_cases, 1):
        status = ""
        details = ""
        
        # Handle edge cases that don't produce a tree
        if len(set(test_str)) <= 1:
            status = "⏭️  SKIPPED"
            details = "Input has 0 or 1 unique characters."
            total_skipped += 1
        else:
            try:
                # Run the full encoding/decoding process
                root, huffman_codes = huffman_encoding(test_str)
                encoded_string = "".join(huffman_codes[char] for char in test_str)
                decoded_string = huffman_decoding(encoded_string, huffman_codes)

                if decoded_string == test_str:
                    status = "✅ PASSED"
                    original_bits = len(test_str) * 8
                    encoded_bits = len(encoded_string)
                    savings = (1 - (encoded_bits / original_bits)) * 100
                    details = f"Space Savings: {savings:.2f}%"
                    total_passed += 1
                else:
                    status = "❌ FAILED"
                    details = "Decoded string does not match original."
            except Exception as e:
                status = "💥 ERROR"
                details = f"An exception occurred: {e}"

        # Use repr() to make whitespace like '\t' and '\n' visible
        str_repr = repr(test_str)
        print(f"Case {i:<2}: {status:<9} | Input: {str_repr:<25} | {details}")

    print("\n--- Summary ---")
    print(f"Passed: {total_passed}/{len(test_cases)}")
    print(f"Skipped/Invalid: {total_skipped}")
    print(f"Failed/Errors: {len(test_cases) - total_passed - total_skipped}")


if __name__ == "__main__":
    main()
