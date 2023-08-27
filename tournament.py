from engine import *

class GameState:

    Exit = -1;

    Idle = 0;
    AI2AI = 1;
    AI2Human = 2
    Human2Human = 3;

    WaitForEngine = 1;
    WaitForHumanFirst = 2;
    WaitForHumanSecond = 3;

    Win = 4;
    Draw = 5;

class Player:
    HUMAN = 0
    BOT = 1
    
    def __init__(self):
        self.type = None
        
    def get_name(self):
        return ""
        
    def start_player(self, move, level, vcf):
        return
        
    def is_ready(self):
        return False
        
    def release(self):
        return;
        
class HumanPlayer(Player):
    def __init__(self):
        super().__init__()
        self.type = Player.HUMAN
        
    def is_ready(self):
        return True
        
class BotPlayer(Player):
    def __init__(self):
        super().__init__()
        self.path = ""
        self.type = Player.BOT
        self.engine = GameEngine()
        
    def has_correct_name(self):
        return self.path is not None and len(self.path) > 0
        
    def release(self):
        if self.engine is not None:
            self.engine.release()
            self.engine = GameEngine()
            
    def init_engine(self, level, vcf, move):
        self.engine.init(self.path, level, vcf);
    
    def get_short_name(self):
        return self.engine.shortName;
        
    def get_name(self):
        return self.engine.name;
        
    def start_player(self, move, level, vcf):
        self.init_engine(level,vcf, move)
        return
        
    def is_ready(self):
        return self.path is not None and len(self.path) > 0
        
class Game:
    def __init__(self, black, white):
        self.black = black
        self.white = white
        self.result = -1
        self.moves = []
        
    def release(self):
        self.black.release()
        self.white.release()
        self.result = -1
        self.moves = []
        
    def is_ready(self):
        return self.black.is_ready(), self.white.is_ready()
        
    def start_players(self, level, vcf):
        self.black.start_player(Move.BLACK, level, vcf)
        self.white.start_player(Move.WHITE, level, vcf)
        
        #Return mode and next state
    def get_game_state(self):
        black_t = self.black.type
        white_t = self.white.type
        
        if black_t == Player.HUMAN and white_t == Player.HUMAN:
            return GameState.Human2Human, GameState.WaitForHumanFirst
        elif black_t == Player.BOT and white_t == Player.BOT:
            return GameState.AI2AI, GameState.WaitForEngine
        else:
            if black_t == Player.BOT:
                return GameState.AI2Human, GameState.WaitForEngine
            else:
                return GameState.AI2Human, GameState.WaitForHumanFirst

class Tournament:

    def __init__(self):
        self.players = []
        self.games = []
        
    def add_player(self, player):
        self.players.append(player)
        
    def reset_players(self):
        self.players = []
        
    def reset_games(self):
        self.games = []
        
    def generate_games(self):
        self.games = []
        return;
                        
    def next_game(self):
        for game in self.games:
            if game.result == -1:
                return game
        
        return None
        
    def load_from_file(self, f):
        reader = PlayerReader()
        self.players = reader.read_from_file(f)
        
    def save_results(self, f):
        #Print players
        f.write('Players:\n')
        for player in self.players:
            f.write(player.name)
            f.write(";")
        f.write("\n")
        
        #Print games
        f.write('Games:\n')
        for game in self.games:
            black = game.black
            white = game.white
            f.write(black.name)
            f.write(";")
            f.write(white.name)
            f.write(";")
            f.write(str(game.result))
            f.write(";")
            
            #Write moves
            for move in game.moves:
                move = move.toPlaceCmd().strip()+" "
                f.write(move)
            
            f.write('\n')
            
            
        
class RoundRobinTournament(Tournament):
    def __init__(self, repetitions = 1):
        super().__init__()
        self.repetitions = repetitions
        
    def generate_games(self):
        self.games = []
        for p1 in self.players:
            for p2 in self.players:
                if p1 != p2:
                    for i in range(0, self.repetitions):
                        game = Game(p1,p2)
                        self.games.append(game)
        
        return None
        
class PlayerReader:

    def __init__(self):
        return
        
    def read_from_file(self, path):
        # Using readline()
        file1 = open(path, 'r')
        players = []
         
        while True:
         
            # Get next line from file
            line = file1.readline()
         
            # if line is empty
            # end of file is reached
            if not line:
                break
            
            #Create player from file
            player = BotPlayer()
            player.path = line.strip()
            
            try:
                player.start_player(Move.BLACK, 1, True);
                player.release()
                players.append(player)
            except Exception as e:
                print("Error to load the engine: " + player.path + ", errors: " + str(e));
             
        file1.close()
        return players
        
            
    
                        
                    
            
