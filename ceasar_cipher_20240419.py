import random
import string

POOL_SIZE = 26

def create_pool():
    pool = []
    for i in range(POOL_SIZE):
        pool.append(create_available_letters())
    return pool

def create_available_letters():
    lowercases = string.ascii_lowercase # 'abcdefghijklmnopqrstuvwxyz'
    digits = string.digits # '0123456789'
    symbols = string.punctuation # '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
    available_letters = list(lowercases) + list(digits) + list(symbols)
    random.shuffle(available_letters)
    available_letters = "".join(available_letters)
    return available_letters

def encode_char(letters, char, key):
    if char in letters:
        char_pos = letters.index(char)
        new_pos = (char_pos + key) % len(letters)
        new_char = letters[new_pos]
    else:
        new_char = char
    return new_char

def create_key_list(text):
    text = text.lower()
    key_list = []
    lowercases = string.ascii_lowercase
    for char in text:
        if char in lowercases:
            key = (lowercases.index(char) + 1) % len(lowercases)
            key_list.append(key)
    return key_list

def get_key():
    input_ok = False
    while not input_ok:
        key = input("Enter a number or a word to encode or decode your message: ")
        key_list = []
        if key.isdecimal(): # '\u00b2'.isdigit() is True
            key_list = [int(key)]
            input_ok = True
        elif key.isalpha():
            key_list = create_key_list(key)
            input_ok = True
    return key_list

def get_letters(pool, key_list):
    return pool[len(key_list) % POOL_SIZE]

def encode_text(text, letters, key_list, method):
    new_chars = []
    index = 0
    for char in text:
        key = key_list[index % len(key_list)]
        if method == "decode":
            key = -key
        new_char = encode_char(letters, char, key)
        new_chars.append(new_char)
        index += 1
    return "".join(new_chars)

def main():
    pool = create_pool()
    while True:
        text = input("Enter text or 'quit' to quit: ")
        if text == 'quit':
            break
        text = text.lower()
        text = text.replace(" ", "")
        key_list = get_key()
        letters = get_letters(pool, key_list)
        encoded_text = encode_text(text, letters, key_list, "encode")
        print(f"Encoded text: {encoded_text}")
    
        decoded_text = encode_text(encoded_text, letters, key_list, "decode")
        print(f"Decoded text: {decoded_text}")
        print()
    
main()