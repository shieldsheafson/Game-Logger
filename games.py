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
        self.file =  file

        self.choose_game_frame(self.file)

    def choose_game_frame(self, file):
        
        self.centerCol = 0
        gameInputRow = 0
        dateInputRow = 2
        self.playersInputRow = 5
        winnersInputRow = 55 # allows for 40+ players
        extraInfoInputRow = 58
        enterButtonRow = 60
        self.numColsInChooseGameFrame = 3
        self.widgets = []

        # game input

        self.choose_game = ttk.Frame(self.root, padding=(5,10,10,10))
        self.choose_game.grid(column=0, row=0)
        choose_game_text = ttk.Label(self.choose_game, text='Choose Game')
        choose_game_text.grid(column=self.centerCol, row=gameInputRow, columnspan=self.numColsInChooseGameFrame)
        self.currentgame = tk.StringVar()

        with open(file, 'r') as file:
            self.fullText = file.read()
            firstLine = self.fullText.split('\n')[0].split(', ')
            firstLine.sort()

        self.gameslist = firstLine # list of all games in database

        self.games = ttk.Combobox(self.choose_game, 
                                  textvariable=self.currentgame, 
                                  values=firstLine)
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

        day_entry_label = ttk.Label(self.choose_game, text='Day (07)', foreground='gray')
        day_entry_label.grid(column=self.centerCol, row=dateInputRow+1, columnspan=1)
        self.day_entry = ttk.Entry(self.choose_game, textvariable=self.day, validate='key', validatecommand=self.check_if_int_and_less_than_3_wrapper, width=2)
        self.day_entry.grid(column=self.centerCol, row=dateInputRow+2, sticky='we', columnspan=1)
        
        month_entry_label = ttk.Label(self.choose_game, text='Month (04)', foreground='gray')
        month_entry_label.grid(column=self.centerCol+1, row=dateInputRow+1, columnspan=1)
        self.month_entry = ttk.Entry(self.choose_game, textvariable=self.month, validate='key', validatecommand=self.check_if_int_and_less_than_3_wrapper, width=2)
        self.month_entry.grid(column=self.centerCol+1, row=dateInputRow+2, sticky='we', columnspan=1)
        
        year_entry_label = ttk.Label(self.choose_game, text='Year (2005)', foreground='gray')
        year_entry_label.grid(column=self.centerCol+2, row=dateInputRow+1, columnspan=1)
        self.year_entry = ttk.Entry(self.choose_game, textvariable=self.year, validate='key', validatecommand=self.check_if_int_and_less_than_5_wrapper, width=4)
        self.year_entry.grid(column=self.centerCol+2, row=dateInputRow+2, sticky='we', columnspan=1)

        # players and scores input

        num_players_label = ttk.Label(self.choose_game, text='Number of Players')
        num_players_label.grid(row=self.playersInputRow, column=self.centerCol, columnspan=self.numColsInChooseGameFrame)

        self.players = []
        self.scores_list = []
        self.number_of_players = tk.StringVar()
        self.check_if_int_wrapper = (self.choose_game.register(self.check_if_int), '%P')

        self.num_players_entry = ttk.Entry(self.choose_game, textvariable=self.number_of_players, validate='key', validatecommand=self.check_if_int_and_less_than_3_wrapper)
        self.num_players_entry.grid(row=self.playersInputRow+1, column=self.centerCol, columnspan=self.numColsInChooseGameFrame)
        self.number_of_players.trace_add('write', self.add_players)

        # winners input

        self.winners = tk.StringVar()

        self.winners_label = ttk.Label(self.choose_game, text='Add Winner', padding=(0,60,0,0))
        self.winners_label.grid(row=winnersInputRow, column=self.centerCol, columnspan=self.numColsInChooseGameFrame)
        second_winners_label = ttk.Label(self.choose_game, text='If more than one winner, \nseparate via commas: Bob, Bill', foreground='gray', justify='center')
        second_winners_label.grid(row=winnersInputRow+1, column=self.centerCol, columnspan=self.numColsInChooseGameFrame)

        self.winners_entry = ttk.Entry(self.choose_game, textvariable=self.winners)
        self.winners_entry.grid(row=winnersInputRow+2, column=self.centerCol, columnspan=self.numColsInChooseGameFrame)

        # extra info input
    
        self.extra_info = tk.StringVar()

        extra_info_label = ttk.Label(self.choose_game, text='Add Extra Information')
        extra_info_label.grid(row=extraInfoInputRow, column=self.centerCol, columnspan=self.numColsInChooseGameFrame)

        self.extra_info_entry = ttk.Entry(self.choose_game, textvariable=self.extra_info)
        self.extra_info_entry.grid(row=extraInfoInputRow+1, column=self.centerCol, columnspan=self.numColsInChooseGameFrame)

        # enter button

        self.enter_button = ttk.Button(self.choose_game, text='Enter', command=self.enter)
        self.enter_button.grid(row=enterButtonRow, column=self.centerCol, columnspan=self.numColsInChooseGameFrame)

    def autocomplete(self, *args):

        # change the dropdown list to only contain games that match current search
        self.games['values'] = [x for x in self.gameslist if self.games.get() in x or self.games.get() == '']

    def add_players(self, *args):

        # adds a number of entry widgets equal to double the number of players
        # one set for player names and the other for scores
        
        # creates a number of tk entry widgets equal to the number
        # provided in the num_of_players_entry widget
        numPlayers = self.num_players_entry.get()
        
        # checks to make sure numPlayers isn't an empty string
        if numPlayers:
            
            numPlayers = int(numPlayers)
            
            # this removes widgets for when the number of players changes
            for i in self.widgets:
                i.destroy()
            self.widgets.clear()
            self.players = self.players[:numPlayers] 
            self.scores_list = self.scores_list[:numPlayers]

            players_label = ttk.Label(self.choose_game, text='Add Players')
            players_label.grid(row=self.playersInputRow+2, column=self.centerCol, columnspan=self.numColsInChooseGameFrame)
            second_players_label = ttk.Label(self.choose_game, text='Players', foreground='gray')
            second_players_label.grid(row=self.playersInputRow+3, column=self.centerCol, columnspan=2)
            scores_label = ttk.Label(self.choose_game, text='Scores', foreground='gray')
            scores_label.grid(row=self.playersInputRow+3, column=2)
            
            for n in range(numPlayers*2):

                if not n%2: # even
                    if int(n/2) >= len(self.players):
                        self.players.append(tk.StringVar())
                    self.widgets.append(ttk.Entry(self.choose_game, textvariable=self.players[int(n/2)]))
                    self.widgets[n].grid(row=self.playersInputRow+4+n, column=self.centerCol, columnspan=2)

                else: # odd
                    if int((n-1)/2) >= len(self.scores_list):
                        self.scores_list.append(tk.StringVar())
                    self.widgets.append(ttk.Entry(self.choose_game, textvariable=self.scores_list[int((n-1)/2)], width=5))
                    self.widgets[n].grid(row=self.playersInputRow+3+n, column=2, sticky='ew')

        self.winners_label['padding'] = (0,0,0,0)
        self.winners_entry.lift()
        self.extra_info_entry.lift()
        self.enter_button.lift()

    def enter(self):

        if self.extra_info.get():
            self.extra_info = [x for x in self.extra_info.get().split(', ')]
        else: 
            self.extra_info = None

        if self.widgets[1].get():
            self.scores_list = [x.get() for x in self.scores_list]
        else: 
            self.scores_list = None

        game = board_game(gameName=self.currentgame.get(), 
                          date='-'.join([self.year.get(), self.month.get(), self.day.get()]),
                          players=[x.get() for x in self.players],
                          scores=self.scores_list,
                          winners=[x for x in self.winners.get().split(', ')],
                          extra_info=self.extra_info
                          )
        
        # modifies the list of games in the database if needed
        if game.gameName not in self.gameslist:
            with open(self.file, 'w') as file:
                if self.fullText:
                    self.fullText = self.fullText.replace('\n', ', ' + game.gameName + '\n', 1)
                    file.write(self.fullText)
                else: 
                    file.write(game.gameName + '\n') # for initializing a database

        self.append_game_to_file(self.file, game)

        self.choose_game.destroy()

        self.enter_frame = ttk.Frame(self.root, padding=(5,5,5,5))     
        self.enter_frame.grid(row=0,column=0)   

        enter_label = ttk.Label(self.enter_frame, text='Game has been added')
        enter_label.grid(row=0, column=0, columnspan=2)

        new_game_button = ttk.Button(self.enter_frame, text='Add another Game', command=self.new_game)
        new_game_button.grid(row=1, column=0)

        quit_button = ttk.Button(self.enter_frame, text='Quit', command=self.root.destroy)
        quit_button.grid(row=1, column=1)

    def new_game(self):

        self.enter_frame.destroy()
        self.choose_game_frame(self.file)

    def check_if_int(self, value):

        return re.match('^[0-9]*$', value) is not None
    
    def check_if_int_and_less_than_3(self, value):
        
        return re.match('^[0-9]*$', value) is not None and len(value) <= 2
    
    def check_if_int_length_and_less_than_5(self, value):
        
        return re.match('^[0-9]*$', value) is not None and len(value) <= 4

    def append_game_to_file(self, file, board_game_object):

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
    
    # returns num of people the player has beat
    # over num of people who the player has been beaten by
    
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
