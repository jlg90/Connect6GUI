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

    def __init__(self, repetitions = 1):
        self.players = []
        self.games = []
        self.repetitions = repetitions
        
    def add_player(self, player):
        self.players.append(player)
        
    def reset_players(self):
        self.players = []
        
    def reset_games(self):
        self.games = []
        
    def generate_games(self):
        self.games = []
        for p1 in players:
            for p2 in players:
                if p1 != p2:
                    for i in range(0, self.repetitions):
                        game = Game(p1,p2)
                        self.games.append(game)
                        
    def next_game(self):
        for game in self.games:
            if game.result == -1:
                return game
        
        return None
                        
    
                        
                    
            
