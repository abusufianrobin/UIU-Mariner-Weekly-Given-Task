players = []

num = int(input("Enter number of players: "))
for i in range(num):
    name = input(f"Enter name of player {i + 1}: ")
    players.append(name)

print("\nList of Players:")
print(players)

for player in players:
    if player == 'Osman Dembele':
        print(f"{player} is the winner of Ballon d'Or.")
    else:
        print(f"{player} is a great player.")
