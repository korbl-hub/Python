import random

MIN_BALL = 1
MAX_BALL = 49
NUMS = 6
COST_PER_TICKET = 10
PRIZE7 = 40
PRIZE6 = 320
PRIZE5 = 640
PRIZE4 = 9600
PRIZE3 = 96000
PRIZE2 = 960000
PRIZE1 = 9600000

banner = """<-. (`-')   (`-')  _    (`-') <-.(`-')      (`-').->  _     (`-')     
   \(OO )_  (OO ).-/ <-.(OO )  __( OO)      ( OO)_   (_)    (OO )_.-> 
,--./  ,-.) / ,---.  ,------,)'-'. ,--.    (_)--\_)  ,-(`-')(_| \_)--.
|   `.'   | | \ /`.\ |   /`. '|  .'   /    /    _ /  | ( OO)\  `.'  / 
|  |'.'|  | '-'|_.' ||  |_.' ||      /)    \_..`--.  |  |  ) \    .') 
|  |   |  |(|  .-.  ||  .   .'|  .   '     .-._)   \(|  |_/  .'    \  
|  |   |  | |  | |  ||  |\  \ |  |\   \    \       / |  |'->/  .'.  \ 
`--'   `--' `--' `--'`--' '--'`--' '--'     `-----'  `--'  `--'   '--'"""

def get_decimal(message, min_value, max_value=None):
    input_ok = False
    while not input_ok:
        value = input(message)
        if value.isdecimal() and int(value) >= min_value:
            if max_value is None:
                input_ok = True
            else:
                input_ok = int(value) <= max_value
    return int(value)

def draw_ticket(pool, num_count):
    ticket = []
    if len(pool) <= NUMS+1:
        pool = list(range(MIN_BALL, MAX_BALL+1))
    for _ in range(num_count):
        ticket.append(pool.pop(random.randint(0, len(pool)-1)))
        ticket.sort()
    return ticket

def draw_tickets(pool, ticket_count):
    tickets = []
    for _ in range(ticket_count):
        if len(pool) <= NUMS+1:
            pool = list(range(MIN_BALL, MAX_BALL+1))
        ticket = draw_ticket(pool, NUMS)
        tickets.append(ticket)
    return tickets

def check_ticket(ticket, win_balls, extra_ball):
    score = 0.0
    for number in ticket:
        if number in win_balls:
            score += 1.0
        elif number == extra_ball:
            score += 0.5
    return check_prize(score)

def check_prize(score):
    if score < 3:
        prize = "No Prize"
    elif score == 3:
        prize = "7th Prize"
    elif score == 3.5:
        prize = "6th Prize"
    elif score == 4:
        prize = "5th Prize"
    elif score == 4.5:
        prize = "4th Prize"
    elif score == 5:
        prize = "3rd Prize"
    elif score == 5.5:
        prize = "2nd Prize"
    else:
        prize = "1st Prize"
    return prize

def check_luck(capital, tickets_each):
    pool = list(range(MIN_BALL, MAX_BALL+1))
    count = 0
    prize_counts = [0] * 8
    capital_start = capital
    while capital >= COST_PER_TICKET * tickets_each:
        win_ticket = draw_ticket(pool, NUMS)
        extra = pool[random.randint(0, len(pool)-1)]
        tickets = draw_tickets(pool, tickets_each)
        capital -= COST_PER_TICKET * tickets_each
        # No, 7, 6, 5, 4, 3, 2, 1
        for ticket in tickets:
            count += 1
            prize = check_ticket(ticket, win_ticket, extra)
            if prize == "No Prize":
                prize_counts[0] += 1
            elif prize == "7th Prize":
                prize_counts[1] += 1
                capital += PRIZE7
            elif prize == "6th Prize":
                prize_counts[2] += 1
                capital += PRIZE6
            elif prize == "5th Prize":
                prize_counts[3] += 1
                capital += PRIZE5
            elif prize == "4th Prize":
                prize_counts[4] += 1
                capital += PRIZE4
            elif prize == "3rd Prize":
                prize_counts[5] += 1
                capital += PRIZE3
                print(f"Ticket #{count}: {ticket} ... 3rd Prize")
            elif prize == "2nd Prize":
                prize_counts[6] += 1
                capital += PRIZE2
                print(f"Ticket #{count}: {ticket} ... 2nd Prize")
            else:
                prize_counts[7] += 1
                capital += PRIZE1
                print(f"Ticket #{count}: {ticket} ... 1st Prize")
            print(f"Ticket #{count}: | Current Capital: ${capital}")
            
        if capital > capital_start:
            break
            
    if capital < COST_PER_TICKET * tickets_each:
        print("You can't afford buying more tickets.")
    elif capital > capital_start:
        print("Congratulations. You've more money than start.")
    print()
    total = prize_counts[0] + prize_counts[1]
    total += prize_counts[2] + prize_counts[3]
    total += prize_counts[4] + prize_counts[5]
    total += prize_counts[6] + prize_counts[7]
    print(f"No Prize: {prize_counts[0]} ({(prize_counts[0] / total):.2%})")
    print(f"7th Prize: {prize_counts[1]} ({(prize_counts[1] / total):.2%})")
    print(f"6th Prize: {prize_counts[2]} ({(prize_counts[2] / total):.2%})")
    print(f"5th Prize: {prize_counts[3]} ({(prize_counts[3] / total):.2%})")
    print(f"4th Prize: {prize_counts[4]} ({(prize_counts[4] / total):.2%})")
    print(f"3rd Prize: {prize_counts[5]} ({(prize_counts[5] / total):.2%})")
    print(f"2nd Prize: {prize_counts[6]} ({(prize_counts[6] / total):.2%})")
    print(f"1st Prize: {prize_counts[7]} ({(prize_counts[7] / total):.2%})")
        
            
def print_menu():
    menu = [
        "Draw Tickets",
        "Check Luck",
        "Check Ticket",
        "Quit"
    ]
    index = 0
    print()
    while index < len(menu):
        print(f"{index+1}: {menu[index]}")
        index += 1
        
def main():
    pool = list(range(MIN_BALL, MAX_BALL+1))
    print(banner)
    while True:
        print_menu()
        print()
        option = get_decimal("Select an option: ", 1, 4)
        print()
        if option == 1:
            ticket_count = get_decimal("How many tickets would you like?: ", 1)
            tickets = draw_tickets(pool, ticket_count)
            count = 1
            for ticket in tickets:
                print(f"Ticket #{count}: {ticket}")
                count += 1
        elif option == 2:
            tickets_each = get_decimal("How many tickets would you buy each time: ", 1)
            capital = get_decimal("How much money would you invest in Mark Six?: ", COST_PER_TICKET * tickets_each)
            check_luck(capital, tickets_each)
        elif option == 3:
            ticket = []
            pool = list(range(MIN_BALL, MAX_BALL+1))
            ordinals = ["1st", "2nd", "3rd", "4th", "5th", "6th"]
            for i in range(NUMS):
                ticket.append(get_decimal(f"Enter {ordinals[i]} number of ticket: ", 1))
            win_ticket = draw_ticket(pool, NUMS)
            extra = pool[random.randint(0, len(pool)-1)]
            print(check_ticket(ticket, win_ticket, extra))
        elif option == 4:
            break
        
main()