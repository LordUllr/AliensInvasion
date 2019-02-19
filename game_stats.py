import json

class GameStats():
    """Armazena dados estatisticos do Jogo"""

    def __init__(self, ai_settings):
        """Inicializa os dados estatisticos"""
        self.ai_settings = ai_settings
        self.reset_stats()
        #Inicia a Invasão Alien em um estado inativo
        self.game_active = False
        self.get_high_score = 0
        #Pontuação máxima conquistada pelo jogador
        with open('high_score.txt') as f_obj:
            for line in f_obj.readlines():
                self.get_high_score = int(line)
        self.high_score = self.get_high_score

    def reset_stats(self):
        """Inicializa os dados que podem mudar durante o jogo"""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
