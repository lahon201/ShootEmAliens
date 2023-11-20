import pygame as pg
from pygame import mixer as mx
import random as rd
import math

# initializes pygame
pg.init()

# creates the window
# pg.display.set_mode((width(x-axis), height(y-axis))
screen = pg.display.set_mode((800, 600))

# title and icon
pg.display.set_caption("ShootEmAliens")
icon = pg.image.load('icon.png')
pg.display.set_icon(icon)

# background of the game
background = pg.image.load('background.png')

# background music
mx.music.load('background.wav')
mx.music.play(-1)

# player
playerImg = pg.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# enemy1
enemy1Img = []
enemy1X = []
enemy1Y = []
enemy1X_change = []
enemy1Y_change = []
no_of_enemies = 5
for i in range(no_of_enemies):
    enemy1Img.append(pg.image.load('enemy1.png'))
    enemy1X.append(rd.randint(0, 735))
    enemy1Y.append(rd.randint(30, 145))
    enemy1X_change.append(2.8)
    enemy1Y_change.append(40)

# bullet
''' bulletX_change : None because bullet won't move in the x-axis 
    bullet_state: 'ready' means bullet is ready to fire
    bullet_state: 'fired' means bullet is fired and is moving '''
bulletImg = pg.image.load('bullet.png')
bulletX = 0
bulletY = playerY
bulletX_change = None
bulletY_change = 5
bullet_state = 'ready'

# score_value
score_value = 0
font = pg.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# game over
game_over_font = pg.font.Font('freesansbold.ttf', 64)
game_over_font2 = pg.font.Font('freesansbold.ttf', 16)


def show_score(x, y):
    score = font.render('Score : ' + str(score_value), True, (0, 255, 255))
    screen.blit(score, (x, y))


def game_over():
    game_over_text = game_over_font.render('GAME OVER', True, (0, 255, 255))
    game_over_text2 = game_over_font2.render('To play again : close and open the game again', True, (0, 128, 128))
    screen.blit(game_over_text, (200, 250))
    screen.blit(game_over_text2, (225, 350))


def player(x, y):
    # blit() method basically draws the image on the screen
    screen.blit(playerImg, (x, y))


def enemy1(img, x, y):
    screen.blit(img, (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fired'
    screen.blit(bulletImg, (x, y - 28))


def is_collide(a, b, c, d):
    distance = math.sqrt((c - a)**2 + (d - b)**2)
    if distance < 27:
        return True


# game loop
running = True
while running:

    # screen.fill((Red, Green, Blue)) (sets background colour)
    screen.fill((0, 0, 0))

    # background image
    screen.blit(background, (0, 0))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        # check if a key was pressed or not
        if event.type == pg.KEYDOWN:
            # check which key was pressed
            if event.key == pg.K_a or event.key == pg.K_LEFT:
                playerX_change = - 2
            if event.key == pg.K_d or event.key == pg.K_RIGHT:
                playerX_change = 2
            if event.key == pg.K_w or event.key == pg.K_UP:
                playerY_change = - 2
            if event.key == pg.K_s or event.key == pg.K_DOWN:
                playerY_change = 2
            if event.key == pg.K_SPACE:
                if bullet_state == 'ready':
                    bullet_sound = mx.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        # check if a key was pressed and released or not
        if event.type == pg.KEYUP:
            # check which key was pressed and released or not
            if event.key == pg.K_a or event.key == pg.K_LEFT or event.key == pg.K_d or event.key == pg.K_RIGHT:
                playerX_change = 0
            if event.key == pg.K_w or event.key == pg.K_UP or event.key == pg.K_s or event.key == pg.K_DOWN:
                playerY_change = 0

    # PLAYER
    player(playerX, playerY)
    playerX += playerX_change
    playerY += playerY_change

    # setting the game boundaries for the player
    if playerX < 0:
        playerX = 0
    if playerX >= 736:
        playerX = 736
    if playerY < 450:
        playerY = 450
    if playerY >= 526:
        playerY = 526

    # ENEMY
    for i in range(no_of_enemies):

        # GAME OVER
        if enemy1Y[i] > 400:
            for j in range(no_of_enemies):
                enemy1Y[j] = 2000
            game_over()
            break

        enemy1(enemy1Img[i], enemy1X[i], enemy1Y[i])
        enemy1X[i] += enemy1X_change[i]

        # setting the game boundaries & movement for the enemies
        if enemy1X[i] <= 0:
            enemy1X_change[i] = 0.6
            enemy1Y[i] += enemy1Y_change[i]
        if enemy1X[i] >= 736:
            enemy1X_change[i] = -0.6
            enemy1Y[i] += enemy1Y_change[i]

        # COLLISION
        collision = is_collide(enemy1X[i], enemy1Y[i], bulletX, bulletY)
        if collision:
            explosion_sound = mx.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = playerY
            bullet_state = 'ready'
            enemy1X[i] = rd.randint(0, 735)
            enemy1Y[i] = rd.randint(30, 145)
            score_value += 1

    # BULLET
    # setting the game boundaries & movement for the bullets
    if bullet_state == 'fired':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    if bulletY <= 0:
        bullet_state = 'ready'
        bulletY = playerY

    # SCORE
    show_score(textX, textY)

    # updates the screen
    pg.display.update()