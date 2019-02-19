import sys
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """Responde a pressionamentos de teclas"""
    if event.key == pygame.K_RIGHT: #Move a espaçonave para a direita
        ship.moving_right = True
    elif event.key == pygame.K_LEFT: #Move a espaçonave para a esquerda
        ship.moving_left = True
    elif event.key == pygame.K_SPACE: #Inicia a função de projeteis
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key ==  pygame.K_q: #Fecha o jogo
        sys.exit()


def check_keyup_events(event, ship):
    """Responde a solturas de tecla"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    """Responde a eventos de pressionamento de teclas e do mouse"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)
        elif event.type == pygame.KEYDOWN: check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP: check_keyup_events(event, ship)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """Inicia um novo jogo quando o jogador clicar em Play"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        #Reinicia as config. de velocidade do jogo
        ai_settings.initialize_dynamic_settings()
        #Oculta cursor do mouse quando o jogo estiver ativo
        pygame.mouse.set_visible(False)
        if play_button.rect.collidepoint(mouse_x, mouse_y):
            stats.reset_stats()
            stats.game_active = True
            #Reinicia as imagens do painel de pontuação
            sb.prep_score()
            sb.prep_high_score()
            sb.prep_level()
            sb.prep_ships()
            #Esvazia a lista de aliens e de projéteis
            aliens.empty()
            bullets.empty()
            #Cria uma nova nave
            create_fleet(ai_settings, screen, ship, aliens)
            ship.center_ship()


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    """Atualiza as imagens na tela para a nova tela"""
    #Redesenha a tela a cada passagem do laço
    screen.blit(ai_settings.bg, (0, 0))
    #Redesenha todos os projéteis atras da nave e dos aliens
    for bullet in bullets.sprites(): bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    #Desenha a informação sobre a pontuação
    sb.show_score()
    #Desenha o botão play se o jogo estiver inativo
    if not stats.game_active: play_button.draw_button()
    #Deixa a tela mais recente visivel
    pygame.display.flip()


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Responde as colisões entre projeteis e aliens"""
    #Remove qualquer projétil e alien que tenham colidido
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        pygame.mixer.init()
        pygame.mixer.music.load('Sounds/explosao.ogg')
        pygame.mixer.music.play(0)
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
            check_high_score(stats, sb)
    #Quando o número de aliens chega a zero, destroi os projéteis restantes e cria uma nova frota
    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        #Aumenta o nível do jogo
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Atualiza a posição dos projéteis e se livra dos projeteis antigos"""
    bullets.update()
    # Livra-se dos projéteis que desapareceram
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)


def fire_bullet(ai_settings, screen, ship, bullets):
    """Cria um novo projétil e o adiciona ao grupo de projéteis"""
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)



def get_number_aliens_x(ai_settings, alien_width):
    """Determina o numero de aliens que cabe em uma linha"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """Determnina o numero de linhas com aliens que cabem na tela"""
    available_space_y = (ai_settings.screen_height - 3 * alien_height - ship_height)
    number_rows = int(available_space_y/ (2*alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
        alien = Alien(ai_settings, screen)
        alien_width = alien.rect.width
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y =alien.rect.height + 2 * alien.rect.height * row_number
        aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    for row_number in range(number_rows - 2):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """"Verifica se a frota está em uma das bordas e atualiza as posições de todos os aliens da frota"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    #Verifica se colisões entre aliens e a nave
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
    #Verifica se algum alien atingiu a parte inferior da tela
    check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets)


def check_fleet_edges(ai_settings, aliens):
    """Responde se algum alien tocar a borda"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """Faz toda a frota descer e mudar de direção"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """Responde ao fato de a nave ter sido atingida por um alien"""
    if stats.ships_left > 0:
        #Decrementa ships_left
        stats.ships_left -= 1
        #Atualiza o painel de pontuações
        sb.prep_ships()
        #Esvazia a lista de aliens e projeteis
        aliens.empty()
        bullets.empty()
        #Cria uma nova frota e centraliza a nave
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        #Faz uma pausa no jogo
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """Verifica se algum alien tocar a parte inferior da tela."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #Trata esse caso do mesmo modo que é feito quando a nave é atingida
            ship_hit(ai_settings, stats, screen,sb, ship, aliens, bullets)
            break


def check_high_score(stats, sb):
    """Verifica se há uma nova pontuação maxima"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        with open('high_score.txt', 'w') as f_obj:
            new_high_score = str(stats.high_score)
            f_obj.write(new_high_score)
        sb.prep_high_score()