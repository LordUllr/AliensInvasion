import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
import game_functions as gf
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button

bg = pygame.image.load('images/space.bmp')


def runGame(): #Inicializa o pygame, as configuraçẽs e o objeto screen
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption('Alien Invasion')
    #Cria o botão Play
    play_button = Button(ai_settings, screen, "PLAY")
    #Cria uma instância para armazenar dados do jogo
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    #Cria a nave, um grupo de projéteis e um grupo de aliens
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()
    #Cria a frota de aliens
    gf.create_fleet(ai_settings, screen,ship, aliens)
    while True: #Inicia o laço principal do jogo
            gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets) #Verifica eventos do teclado e do mouse
            if stats.game_active:
                ship.update() #Chama a função de movimento da nave
                gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
                gf.update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets)
            gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)


runGame()