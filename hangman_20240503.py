import random
import string

# 準備驗證用, 如果在 set 内, 則是長度是1的細楷
LOWERCASES = set(string.ascii_lowercase)
# random.choice 的 argument 要是 sequence, 所以轉成 tuple
WORDS = tuple({word for word in dir(random) if word.islower() and '_' not in word})

MAX_LIVES = 6

def get_secret_word():
    return random.choice(WORDS)

def create_secret_dict(secret_word):
    # key 是 index, value 是對應的字母
    secret_dict = dict()
    for i in range(len(secret_word)):
        secret_dict[i] = secret_word[i]
    return secret_dict

def get_secret_chars(secret_dict):
    # 因爲 secret_word 的字母可能有重複, 取 set 就可以
    return set(secret_dict.values())

def get_hints_dict(secret_dict, correct_chars):
    # secret_dict 的 key 是 secret_word 的位置
    # 如果該位置的字母已猜對, 可以顯示字母, 否則顯示 '-'
    hints_dict = dict()
    for pos, char in secret_dict.items():
        if char in correct_chars:
            hints_dict[pos] = char
        else:
            hints_dict[pos] = '-'
    return hints_dict

def show_hints(secret_word, hints_dict):
    hints_tuple = tuple(hints_dict[index] for index in range(len(secret_word)))
    return " ".join(hints_tuple)

def get_guess(guessed_chars):
    guess_ok = False
    while not guess_ok:
        guess = input("Guess a letter: ")
        if guess in LOWERCASES:
            guess_ok = True
            guessed_chars.add(guess)
    return guess, guessed_chars

def check_guess(guess, secret_chars, correct_chars, lives):
    if guess in secret_chars:
        correct_chars.add(guess)
    else:
        lives -= 1
    return correct_chars, lives

def check_win(secret_chars, correct_chars):
    # 全被猜對即是勝利了
    return secret_chars == correct_chars

def check_lose(lives):
    return lives == 0

def show_chars(chars_set):
    # 傳入 dicts, 顯示已猜的字母和猜錯的字母
    return " ".join(chars_set)
    
def main():
    while True:
        guessed_chars = set()
        correct_chars = set()
        lives = MAX_LIVES
        
        secret_word = get_secret_word()
        secret_dict = create_secret_dict(secret_word)
        secret_chars = get_secret_chars(secret_dict)
        
        is_win = False
        is_lose = False
        
        while not is_win and not is_lose:
        
            hints_dict = get_hints_dict(secret_dict, correct_chars)
            print(show_hints(secret_word, hints_dict))
            
            print(f"Lives = {lives}")
            guess, guessed_chars = get_guess(guessed_chars)
            correct_chars, lives = check_guess(guess, secret_chars, correct_chars, lives)
            print()

            print(f"Guessed chars: {show_chars(guessed_chars)}")

            # 猜過而不在猜對的 set 内即是猜錯
            wrong_chars = guessed_chars - correct_chars
            if len(wrong_chars) > 0:
                print(f"Wrong chars: {show_chars(wrong_chars)}")
            
            is_win = check_win(secret_chars, correct_chars)
            is_lose = check_lose(lives)
        
        if is_win:
            print(f"You are so smart. You guessed the secret word {secret_word}.")
            print()
        if is_lose:
            print(f"Game Over. The secret word was {secret_word}.")
            print()
            
main()
