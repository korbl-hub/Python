import random

MAX_SCORE = 100

def roll_dice(name, current_score, is_turn):
    dice = random.randint(1, 6)
    if dice == 1:
        current_score = 0
        print(f"{name} rolled a 1. Current Score is 0.")
        is_turn = False
    else:
        current_score += dice
        print(f"{name} rolled a {dice}. Current Score is: {current_score}.")
    return current_score, is_turn
                
def user_turn():
    current_score = 0
    is_user_turn = True
    while is_user_turn:
        to_roll = input("Do you want to roll a dice? 'yes' or 'no': ")
        if to_roll.lower() == "yes":
            current_score, is_user_turn = roll_dice("User", current_score, True)
        else:
            is_user_turn = False
    return current_score

def com_turn():
    current_score = 0
    is_com_turn = True
    current_score, is_com_turn = roll_dice("Com", current_score, True)
    while is_com_turn:
        to_roll = random.choice((True, False))
        if to_roll:
            current_score, is_com_turn = roll_dice("Com", current_score, True)
        else:
            print("Com pass.")
            is_com_turn = False
    return current_score

def main():
    user_score = 0
    com_score = 0
    is_user_turn = True
    while user_score < MAX_SCORE and com_score < MAX_SCORE:
        if is_user_turn:
            print(f"User Turn (User Score = {user_score}):")
            user_score += user_turn()
            is_user_turn = not is_user_turn
        else:
            print(f"Com Turn (Com Score = {com_score}):")
            com_score += com_turn()
            is_user_turn = not is_user_turn
        print()
    if user_score > MAX_SCORE:
        print(f"User Score = {user_score} (>= {MAX_SCORE}). User wins.")
    else:
        print(f"Com Score = {com_score} (>= {MAX_SCORE}). Com wins.")
            
main()