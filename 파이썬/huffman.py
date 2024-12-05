import heapq
from collections import defaultdict

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_frequency_dict(text):
    freq = defaultdict(int)
    for char in text:
        freq[char] += 1
    return freq

def build_huffman_tree(freq_dict):
    heap = [HuffmanNode(char, freq) for char, freq in freq_dict.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)
    return heap[0]

def build_codes(node, prefix="", code_map=None):
    if code_map is None:
        code_map = {}
    if node.char is not None:
        code_map[node.char] = prefix
    else:
        build_codes(node.left, prefix + "0", code_map)
        build_codes(node.right, prefix + "1", code_map)
    return code_map

def huffman_encode(text, code_map):
    encoded_text = ''.join(code_map[char] for char in text)
    byte_array = bytearray()
    for i in range(0, len(encoded_text), 8):
        byte = encoded_text[i:i+8].ljust(8, '0')
        byte_array.append(int(byte, 2))
    return byte_array

def huffman_decode(encoded_data, root):
    result = []
    node = root
    for byte in encoded_data:
        # 8비트씩 처리
        bits = format(byte, '08b')  # 8비트로 변환
        for bit in bits:
            node = node.left if bit == '0' else node.right
            if node.char:
                result.append(node.char)
                node = root
    return ''.join(result)

def save_encoded_data(encoded_data, filename):
    with open(filename, 'wb') as file:
        file.write(encoded_data)

def read_encoded_data(filename):
    with open(filename, 'rb') as file:
        return file.read()

def main():
    import os
    print("Current working directory:", os.getcwd())
    
    with open("./파이썬/data.txt", "r", encoding="utf-8") as file:
        text = file.read()

    freq_dict = build_frequency_dict(text)
    root = build_huffman_tree(freq_dict)
    code_map = build_codes(root)
    encoded_text = huffman_encode(text, code_map)

    save_encoded_data(encoded_text, "./파이썬/encode_result.bin")

    encoded_data = read_encoded_data("./파이썬/encode_result.bin")

    decoded_text = huffman_decode(encoded_data, root)

    with open("./파이썬/decode_result.txt", "w", encoding="utf-8") as file:
        file.write(decoded_text)

    original_size = len(text.encode('utf-8'))
    compressed_size = len(encoded_data)
    compression_rate = (1 - compressed_size / original_size) * 100

    print(f"Original size: {original_size} bytes")
    print(f"Compressed size: {compressed_size} bytes")
    print(f"Compression rate: {compression_rate:.2f}%")

if __name__ == "__main__":
    main()
