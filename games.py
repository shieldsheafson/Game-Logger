class board_game: 

    def __init__(self, 
                 gameName: str, 
                 date: str, 
                 players: list, 
                 winners: list, 
                 scores: list, 
                 extra_info: list):
        
        self.gameName = gameName.strip().casefold()
        self.date = date
        self.players = list([x.strip().casefold() for x in players])
        self.winners = list(x.strip().casefold() for x in winners)
        self.scores = list(scores) if scores is not None else None
        self.special = list(extra_info) if extra_info is not None else None
    
    def __str__(self):
        return f"{self.gameName}; {self.date}; {self.players}; {self.winners}; {self.scores}; {self.special}"

def append_game_to_file(file, board_game_object):

    with open(file, 'at') as file:
        file.write(str(board_game_object)+'\n')

def make_dict_of_games(file):

    games_dict = {}

    with open(file, 'rt') as file:
        games = file.readlines()
    
    # create dict of games
    for item in games:
        
        items = item.split('; ')

        # takes string representation of each parameter 
        # and uses eval to make it into python code
        # also strips final parameter to remove the \n
        item = board_game(items[0], 
                          items[1], 
                          eval(items[2]), 
                          eval(items[3]), 
                          eval(items[4]), 
                          eval(items[5].strip()))

        if games_dict.get(item.gameName):
            games_dict[item.gameName].append(item)
        else:
            games_dict[item.gameName] = [item]

    return(games_dict)

def score(file, player):
    
    # returns num of people player has beat
    # over num of people who player has been beaten by
    
    games_dict = make_dict_of_games(file)
    people_beat = 1 #starts at one to prevent division by zero
    people_beaten_by = 1 #starts at one to prevent division by zero
    
    for key in games_dict:
        for game in games_dict[key]:

                if player.lower() in game.winners:
                    people_beat += len(game.players)-len(game.winners)
                elif player.lower() in game.players:
                    people_beaten_by += len(game.winners)
        
    return(people_beat/people_beaten_by)

def add_game_to_list(file):

    # temp solution until I make a GUI

    gameName = input('Game Name: ')
    date = input('Date (ex. 2000-01-30): ')
    players = []
    winners = []
    scores = None
    data = None
    
    while True:
        player = input('Player (break to end): ')
        if player.lower() == 'break': break
        players.append(player)
    
    while True:
        winner = input('Winner (break to end): ')
        if winner.lower() == 'break': break
        winners.append(winner)
    
    if input('Add scores (y/n)? ').lower() == 'y':
        scores = []
        for item in players:
            score = input(item + "'s score: ")
            scores.append(score)
    
    if input('Add extra data (y/n)? ').lower() == 'y':
        data = []
        while True:
            data_point = input('Data (break to end): ').lower()
            if data_point == 'break': break
            data.append(data_point)

    if input(f'''Is this correct (y/n)? 
    Game name: {gameName} 
    Date: {date} 
    Players: {str(players)} 
    Winners: {str(winners)} 
    Scores: {str(scores)} 
    Extra Data: {str(data)} ''').lower() != 'n':
        game = board_game(gameName, date, players, winners, scores, data)
        append_game_to_file(file, game )
    else: 
        add_game_to_list(file)
    
