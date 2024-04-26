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

# 第一次做用了split(), join(), 想到不用的方法

def encode_line(line):
    line = line.lower()
    for key, value in morse_code_dict.items():
        # 字元之間插入 "/", 等同將密碼 + "/"
        line = line.replace(key, value + "/")
        # 字與字之間用另一種分隔符
        line = line.replace("/ ", "|")
    # "|" 保留到decode用, 不要最尾的 "/"
    return line[:-1]

def decode_line(line):
    # 頭尾 + "/" 方便分隔
    line = f"/{line}/"
    for key, code in morse_code_dict.items():
        # 先換字元之間, 因爲 "/密碼/密碼/" 中間重叠, 所以要用while迴圈
        while f"/{code}/" in line:
            line = line.replace(f"/{code}/", f"/{key}/")
    # 換每個字的頭尾
    for key, code in morse_code_dict.items():
        line = line.replace(f"|{code}/", f"|{key}/")
        line = line.replace(f"/{code}|", f"/{key}|")
    line = line.replace("|", " ")
    line = line.replace("/", "")
    return line

def main():
    line = input("Enter your line: ")
    print()
    
    encoded_line = encode_line(line)
    print(f"Encoded Line: {encoded_line.replace('|', ' ')}")
    print()
    
    decoded_line = decode_line(encoded_line)
    print(f"Decoded Line: {decoded_line}")

main()