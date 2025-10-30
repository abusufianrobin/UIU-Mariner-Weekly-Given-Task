dict=[{'name': 'Messi', 'Team': 'Inter Miami'},
{'name': 'Vinicious Jr.', 'Team': 'Real Madrid'},
{'name': 'Desire Due', 'Team': 'PSG'},
{'name': 'Kyllian MBappe', 'Team': 'Real Madrid'},
{'name': 'Jude Bellingham', 'Team': 'Real Madrid'},
{'name': 'Erling Haaland', 'Team': 'Manchester City'},
{'name': 'Osman Dembele', 'Team': 'PSG'},
{'name': 'Vithinha', 'Team': 'PSG'},
{'name': 'Luka Modric', 'Team': 'AC Milan'},
{'name': 'Robert Lewandowski', 'Team': 'Barcelona'}]

for person in dict:
    print(f"Name: {person['name']}, Team: {person['Team']}")
    print("Person details processed.")


if 'Osman Dembele' in [person['name'] for person in dict]:
    print("Osman Dembele is winner of Ballon d'Or.")