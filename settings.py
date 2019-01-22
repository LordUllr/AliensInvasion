import pygame


class Settings():
    """Classe para armazenar todas as configurações do Alien Invasion"""
    def __init__(self): #Configurações da Tela
        self.screen_width = 1200
        self.screen_height = 680
        self.bg = pygame.image.load('images/space.bmp')
        #Configurações da espaçonave
        self.ship_limit = 3
        #Configurações dos projeteis
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 79, 4, 5
        self.bullets_allowed = 5
        #Cofigurações dos Aliens
        self.fleet_drop_speed = 10
        #Taxa com que a velocidade do jogo aumenta
        self.speedup_scale = 1.1
        #Taxa com que os pontos para cada alien aumenta
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Inicializa as configurações que mudam no decorrer do jogo"""
        self.ship_speed_factor = 2.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 2
        #fleet_direction igual a 1 representa a direita, -1 representa a esquerda
        self.fleet_direction = 1
        #Pontuação
        self.alien_points = 50

    def increase_speed(self):
        """Aumenta as config. de velocidade"""
        self.ship_speed_factor  *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)