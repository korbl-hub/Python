morse_code_dict = {
    'a': ".-",      'b': "-...",    'c': "-.-.",    'd': "-..",     'e': ".",
    'f': "..-.",    'g': "--.",     'h': "....",    'i': "..",      'j': ".---", 
    'k': "-.-",     'l': ".-..",    'm': "--",      'n': "-.",      'o': "---",
    'p': ".--.",    'q': "--.-",    'r': ".-.",     's': "...",     't': "-",    
    'u': "..-",     'v': "...-",    'w': ".--",     'x': "-..-",    'y': "-.--",
    'z': "--..",
    
    '1': ".----",   '2': "..---",   '3': "...--",   '4': "....-",   '5': ".....",
    '6': "-....",   '7': "--...",   '8': "---..",   '9': "----.",   '0': "-----"
}

def encode_line(line):
    line = line.lower()
    # 第一次做時用了split(), join(), 想到其實可以不用
    for key, value in morse_code_dict.items():
        # 字母之間插入 "/", 等同將密碼 + "/"
        line = line.replace(key, value + "/")
        # 字與字之間只有空格, 所以要換
        line = line.replace("/ ", " ")
    return line[:-1] # 最尾的 "/" 不要

def decode_line(encoded_line):
    # 因爲 "/" 前只有 "." "-", 直接換會撞, 所以保留舊方法
    words = encoded_line.split()
    decoded_line = []
    for word in words:
        decoded_word = []
        chars = word.split("/")
        for char in chars:
            for key, code in morse_code_dict.items():
                if char == code:
                    decoded_word.append(key)
                    break
        decoded_line.append("".join(decoded_word))
    return " ".join(decoded_line)

def print_morse_words(encoded_line):
    # 用列印文字方法代替發聲
    words = encoded_line.split()
    for word in words:
        chars = word.split("/")
        for char in chars:
            codes = list(char)
            for code in codes:
                if code == ".":
                    print("dot", end=" ")
                elif code == "-":
                    print("dash", end=" ")
            print("pause")
        print()

def main():
    line = input("Enter your line: ")
    encoded_line = encode_line(line)
    print(f"Encoded Line: {encoded_line}")
    print()
    
    print_morse_words(encoded_line)
    
    decoded_line = decode_line(encoded_line)
    print(f"Decoded Line: {decoded_line}")

main()