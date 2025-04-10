import pygame
import os
import sys

# Получение пути к ресурсам
def resource_path(relative_path):
    try:
        # PyInstaller создаёт временную папку _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Пример использования
icon_path = resource_path("icons/icon.png")



clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((618, 359)) #,  flags=pygame.NOFRAME для того чтоб запускать без рамок
pygame.display.set_caption("DmS game v1.0")
icon=pygame.image.load(icon_path + "icons/icon.png").convert_alpha()
pygame.display.set_icon(icon)


bground = pygame.image.load(icon_path  + "icons/background.png").convert_alpha()

mob = pygame.image.load(icon_path + "icons/ghost.png").convert_alpha()
ghost_list_ingame = []

walk_right = [
    pygame.image.load(icon_path + "icons/walkingright1.png")
    , pygame.image.load(icon_path + "icons/walkingright2.png")
    , pygame.image.load(icon_path + "icons/walkingright3.png")
    , pygame.image.load(icon_path + "icons/walkingright4.png")
    , pygame.image.load(icon_path + "icons/walkingright5.png")
]
walk_left = [
    pygame.image.load(icon_path + "icons/walkingleft1.png")
    , pygame.image.load(icon_path + "icons/walkingleft2.png")
    , pygame.image.load(icon_path + "icons/walkingleft3.png")
    , pygame.image.load(icon_path + "icons/walkingleft4.png")
    , pygame.image.load(icon_path + "icons/walkingleft5.png")
]

player_anim_count = 0
bg_x=0

player_speed=5
player_X=150
player_y=250

is_jump = False
jump_count = 8

bg_sound = pygame.mixer.Sound(icon_path + "sounds/Underclocked.mp3")
bg_sound.play()

bullet_last = 5
guns_sound = pygame.mixer.Sound(icon_path + "sounds/WRY.mp3")
gun=pygame.image.load(icon_path + "icons/bullet.png").convert_alpha()
guns=[]

gameduring=True


fonts=pygame.font.Font(icon_path + "fonts/PixelifySans.ttf", 40)
lose_text=fonts.render(icon_path + "You Lose", False, (87, 11, 181))
text_rect=lose_text.get_rect(center=(618//2, 359//2))

restart_text=fonts.render("Play Again", False, (181, 11, 170))
restart_button_rect=restart_text.get_rect(center=(618//2, 359//2 + 30))


ghost_respawn = pygame.USEREVENT + 1
pygame.time.set_timer(ghost_respawn, 1800)

running = True
while running:
    screen.blit(bground, (bg_x, 0))
    screen.blit(bground, (bg_x + 618, 0))


    if gameduring:

        player_layer=walk_left[0].get_rect(topleft=(player_X, player_y))
    
        if ghost_list_ingame:
            for (i, ele) in enumerate(ghost_list_ingame):
                screen.blit(mob, ele)
                ele.x -= 10
            
                if ele.x < -10:
                    ghost_list_ingame.pop(i)

                if player_layer.colliderect(ele):
                    gameduring=False

        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            screen.blit(walk_left[player_anim_count], (player_X, player_y))
        else:
            screen.blit(walk_right[player_anim_count], (player_X, player_y))

    
        if keys[pygame.K_LEFT] and player_X > 30:
            player_X -= player_speed
        elif keys[pygame.K_RIGHT] and player_X < 300:
            player_X += player_speed

        if not is_jump:
            if keys[pygame.K_SPACE]:
                is_jump = True
        else:
            if jump_count >= -8:
                if jump_count > 0:
                    player_y -= (jump_count **2 ) /2
                else:
                    player_y += (jump_count **2 ) /2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 8


        if player_anim_count == 3:
            player_anim_count = 0
        else:
            player_anim_count += 1

        bg_x -= 2
        if bg_x == -618:
            bg_x = 0


        if guns:
            for (g ,el) in enumerate(guns):
                screen.blit(gun, (el.x, el.y))
                el.x += 5

                if el.x > 618:
                    guns.pop(g)

                if ghost_list_ingame:
                    for (i, enemy) in enumerate(ghost_list_ingame):
                        if el.colliderect(enemy):
                            guns.pop(g)
                            ghost_list_ingame.pop(i)


    else:
        screen.fill((0, 0, 0))
        screen.blit(lose_text, text_rect)
        screen.blit(restart_text, restart_button_rect)

        mouse=pygame.mouse.get_pos()
        if restart_button_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameduring=True
            player_X=150
            ghost_list_ingame.clear()
            guns.clear()



    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == ghost_respawn:
            ghost_list_ingame.append(mob.get_rect(topleft=(620, 250)))
        if gameduring and event.type == pygame.KEYUP and event.key == pygame.K_f and bullet_last > 0:
            guns.append(gun.get_rect(topleft=(player_X  + 30, player_y + 10)))
            bullet_last -= 1
            guns_sound.play()
        
    clock.tick(15) #FPS