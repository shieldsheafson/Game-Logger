import tkinter as tk, re
from tkinter import ttk

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

class gui_maker:

    def __init__(self, file):
        
        self.root = tk.Tk()
        # self.choose_game_window = tk.Toplevel(self.root)
        
        self.centerCol = 0
        gameInputRow = 0
        dateInputRow = 2
        self.playersInputRow = 5
        self.numColsInChooseGameFrame = 3
        numRowsInChooseGameFrame = 10
        self.widgets = []

        # game input

        self.choose_game = ttk.Frame(self.root, padding=(5,10,10,10))
        self.choose_game.grid(column=0, row=0)
        choose_game_text = ttk.Label(self.choose_game, text='Choose Game')
        choose_game_text.grid(column=self.centerCol, row=gameInputRow, columnspan=self.numColsInChooseGameFrame)
        self.currentgame = tk.StringVar()

        with open(file, 'r') as file:
            text = file.readlines()[0].split(', ')
            text.sort()
        
        self.gameslist = text # list of all games in database

        self.games = ttk.Combobox(self.choose_game, 
                                  textvariable=self.currentgame, 
                                  values=text)
        self.currentgame.trace_add('write', self.autocomplete)
        self.games.grid(column=self.centerCol, row=gameInputRow+1, columnspan=self.numColsInChooseGameFrame)

        # date input

        date_label = ttk.Label(self.choose_game, text='Add Date')
        date_label.grid(column=self.centerCol, row=dateInputRow, columnspan=self.numColsInChooseGameFrame)

        self.year = tk.StringVar()
        self.month = tk.StringVar()
        self.day = tk.StringVar()
        self.check_if_int_and_less_than_3_wrapper = (self.choose_game.register(self.check_if_int_and_less_than_3), '%P')
        self.check_if_int_and_less_than_5_wrapper = (self.choose_game.register(self.check_if_int_length_and_less_than_5), '%P')

        year_entry_label = ttk.Label(self.choose_game, text='Year (2005)', foreground='gray')
        year_entry_label.grid(column=self.centerCol+2, row=dateInputRow+1, columnspan=1)
        self.year_entry = ttk.Entry(self.choose_game, textvariable=self.year, validate='key', validatecommand=self.check_if_int_and_less_than_5_wrapper, width=4)
        self.year_entry.grid(column=self.centerCol+2, row=dateInputRow+2, sticky='we', columnspan=1)
        
        month_entry_label = ttk.Label(self.choose_game, text='Month (04)', foreground='gray')
        month_entry_label.grid(column=self.centerCol+1, row=dateInputRow+1, columnspan=1)
        self.month_entry = ttk.Entry(self.choose_game, textvariable=self.month, validate='key', validatecommand=self.check_if_int_and_less_than_3_wrapper, width=2)
        self.month_entry.grid(column=self.centerCol+1, row=dateInputRow+2, sticky='we', columnspan=1)

        day_entry_label = ttk.Label(self.choose_game, text='Day (07)', foreground='gray')
        day_entry_label.grid(column=self.centerCol, row=dateInputRow+1, columnspan=1)
        self.day_entry = ttk.Entry(self.choose_game, textvariable=self.day, validate='key', validatecommand=self.check_if_int_and_less_than_3_wrapper, width=2)
        self.day_entry.grid(column=self.centerCol, row=dateInputRow+2, sticky='we', columnspan=1)

        # players input

        num_players_label = ttk.Label(self.choose_game, text='Number of Players')
        num_players_label.grid(row=self.playersInputRow, column=self.centerCol, columnspan=self.numColsInChooseGameFrame)

        self.players = []
        self.number_of_players = tk.StringVar()
        self.check_if_int_wrapper = (self.choose_game.register(self.check_if_int), '%P')

        self.num_players_entry = ttk.Entry(self.choose_game, textvariable=self.number_of_players, validate='key', validatecommand=self.check_if_int_wrapper)
        self.num_players_entry.grid(row=self.playersInputRow+1, column=self.centerCol, columnspan=self.numColsInChooseGameFrame)
        self.number_of_players.trace_add('write', self.add_players)
    
    def autocomplete(self, *args):

        # change the dropdown list to only contain games that match current search
        self.games['values'] = [x for x in self.gameslist if self.games.get() in x or self.games.get() == '']

    def add_players(self, *args):
        
        # creates a number of tk entry widgets equal to the number
        # provided in the num_of_players_entry widget
        numPlayers = self.num_players_entry.get()
        
        # checks to make sure numPlayers isn't an empty string
        if numPlayers:
            
            # when the number of players changes, 
            # this removes the previous widgets so they can replaced with the new ones
            for n, i in enumerate(self.widgets):
                self.widgets[n].destroy()
            self.widgets.clear()

            numPlayers = int(numPlayers)
            players_label = ttk.Label(self.choose_game, text='Add Players')
            players_label.grid(row=self.playersInputRow+2, column=self.centerCol, columnspan=self.numColsInChooseGameFrame)
            for n in range(numPlayers):
                self.players.append(tk.StringVar())
                self.widgets.append(ttk.Entry(self.choose_game, textvariable=self.players[n]))
                self.widgets[n].grid(row=self.playersInputRow+3+n, column=0, columnspan=self.numColsInChooseGameFrame)

    def check_if_int(self, value):

        return re.match('^[0-9]*$', value) is not None
    
    def check_if_int_and_less_than_3(self, value):
        
        return re.match('^[0-9]*$', value) is not None and len(value) <= 2
    
    def check_if_int_length_and_less_than_5(self, value):
        
        return re.match('^[0-9]*$', value) is not None and len(value) <= 4

def append_game_to_file(file, board_game_object):

    with open(file, 'at') as file:
        file.write(str(board_game_object)+'\n')

def make_dict_of_games(file):

    games_dict = {}

    with open(file, 'rt') as file:
        games = file.readlines()[1:]

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

def add_game_gui(file):

    gui = gui_maker(file)

    gui.root.mainloop()


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
    
add_game_gui('/Users/benedictsmith/Code/python/games/games.txt')

