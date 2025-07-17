import heapq
from collections import defaultdict

def build_huffman_tree(text):
    freq = defaultdict(int)
    for char in text:
        freq[char] += 1
    heap = [[weight, [char, ""]] for char, weight in freq.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    return heap[0][1:]

if __name__ == "__main__":
    text = input("Enter text to encode: ")
    huffman_codes = build_huffman_tree(text)
    print("Huffman Codes:")
    for char, code in sorted(huffman_codes, key=lambda x: len(x[1])):
        print(f"'{char}': {code}")