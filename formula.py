playerOne = input("Enter Your Pick: ")
playerTwo = input("Enter Pick's Opponent: ")
odds = input("Enter Odds: ")

playerOne_percentage = 0.0
playerTwo_percentage = 0.0

playerOne_total = 0
playerTwo_total = 0

f = open("player_data.txt", "r")
for x in f:
    first_name = x.split()[0]
    last_name = x.split()[1]
    name = first_name + ' ' + last_name
    if (playerOne == name):
        playerOne_percentage = float(x.split()[len(x.split())-1])
        playerOne_total = int(x.split()[len(x.split())-2])
    elif (playerTwo == name):
        playerTwo_percentage = float(x.split()[len(x.split())-1])
        playerTwo_total = int(x.split()[len(x.split())-2])

numerator = playerOne_percentage * (1 - playerTwo_percentage)
denominator = numerator + playerTwo_percentage * (1 - playerOne_percentage)

chance_of_predicting_jump = numerator / denominator

part_one = (chance_of_predicting_jump * .63925438596491226)
part_two = (1 - chance_of_predicting_jump) * (1 - .63925438596491226)

chance_of_winning = (part_one + part_two) * 100

print("Chance of Winning: ", end=' ')
print(chance_of_winning)

num = int(odds[1:])
prob = 0.0
if (odds[0] == '-'):
    prob = num / (num+100) * 100
else:
    prob = 100 / (num+100) * 100

print("Vegas Odds: ", end=' ')
print(prob)

print()
if (prob < chance_of_winning):
    print("TAKE THE BET!")
else:
    print("DON'T TAKE BET!")

owp_playerOne = 0.0
owp_playerTwo = 0.0
owp_differential = 0.0
f = open("player_owp.txt", "r")
for x in f:
    first_name = x.split()[0]
    last_name = x.split()[1]
    name = first_name + ' ' + last_name
    if (playerOne == name):
        owp_playerOne = float(x.split()[len(x.split())-1])
    elif (playerTwo == name):
        owp_playerTwo = float(x.split()[len(x.split())-1])

owp_differential = abs(owp_playerOne-owp_playerTwo)

if (playerOne_total < 10.0 or playerTwo_total < 10.0 or owp_differential > 10.0):
    print('Caution!')

print()
f.close()