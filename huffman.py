from bytestream import *


class HuffmanTree:
  def __init__(self, freq: int, char: str = None, left = None, right = None):
    self.char = char
    self.freq = freq
    self.left = left
    self.right = right

  def __repr__(self):
    # N'hésitez pas à modifier cette fonction
    return f"({self.char}:{self.freq})"



def build_freqs(text: str) -> dict[str, int]:
  freqs = {}

  for char in text:
    if char in freqs:
        freqs[char] += 1
    else:
        freqs[char] = 1

  return freqs



def build_huffman_tree(freqs: dict[str, int]) -> HuffmanTree:
  freqs_list = []

  for elem in freqs:
    node = HuffmanTree(freqs[elem], elem)
    freqs_list.append(node)

  while len(freqs_list) > 1:

    low_freqs = []
    for _ in range(2):
      lowest_freq = min(freqs_list, key=lambda node: node.freq) # Aide d'une ia pour trouver ceci
      low_freqs.append(lowest_freq)
      freqs_list.remove(lowest_freq)

    new_freq = sum(node.freq for node in low_freqs)
    new_node = HuffmanTree(new_freq, None, low_freqs[0], low_freqs[1])
    
    freqs_list.append(new_node)
  
  return freqs_list[0]

def intermediaire(tree: HuffmanTree, coding_dict, path=""):
  if tree.char is not None:
    coding_dict[tree.char] = path
  else:
    if tree.left is not None:
      intermediaire(tree.left, coding_dict, path + "0")
    if tree.right is not None:
      intermediaire(tree.right, coding_dict, path + "1")
  
  return coding_dict

def build_encodings(tree: HuffmanTree) -> dict[str, str]:
  coding_dict = {}
  result = intermediaire(tree, coding_dict)

  return result



def huffman_encode(plain: str, tree: HuffmanTree) -> bytes:
  encodings = build_encodings(tree)

  compressed = ""

  for char in plain:
    code = encodings[char]
    compressed += code

  return bin2bytes(compressed)


def huffman_decode(bytestream: bytes, tree: HuffmanTree) -> str:
  compressed = bytes2bin(bytestream)

  plain = ""

  current = tree
  for bit in compressed:
    if current.char is not None:
      plain += current.char
      current = tree
    if bit == "0":
      current = current.left
    elif bit == "1":
      current = current.right

  if current.char is not None:
    plain += current.char

  return plain
