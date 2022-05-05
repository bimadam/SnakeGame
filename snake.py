import pygame
import time
import random
from tkinter import *
import os

had_rychlost = 15

konec_okno = Tk ()
windowWidth = 600
windowHeight = 250
positionRight = int(konec_okno.winfo_screenwidth()/2 - windowWidth/2)
positionDown = int(konec_okno.winfo_screenheight()/2 - windowHeight/2)
konec_okno.title = ('Konec hry')

window_x = 1200
window_y = 720

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

pygame.init()

pygame.display.set_caption('Snake - hra')
hra_okno = pygame.display.set_mode((window_x, window_y))

fps = pygame.time.Clock()

# tělo hada
had_pozice = [100, 50]
had_telo = [[100, 50], [90, 50], [80, 50], [70, 50]]

# generace jídla
papani_pozice = [random.randrange(1, (window_x // 10)) * 10,
                 random.randrange(1, (window_y // 10)) * 10]
papani_spawn = True

# výchozí směr hada
smer = 'RIGHT'
change_to = smer

skore = 0

def ukaz_skore(choice, color, font, size):
    skore_font = pygame.font.SysFont(font, size)
    skore_surface = skore_font.render('Skóre: ' + str(skore), True, color)
    skore_rect = skore_surface.get_rect()

    hra_okno.blit(skore_surface, skore_rect)

def leavegame():
    pygame.quit()
    quit()

def resetgame():
    konec_okno.destroy()
    pygame.quit()
    while 1:
        os.system("python code.py")
        exit()
    quit()

def konechry():
    my_font = pygame.font.SysFont('Verdana', 50)

    konechry_surface = my_font.render('Tvé skóre je: ' + str(skore), True, red)

    konechry_rect = konechry_surface.get_rect()
    konechry_rect.midtop = (window_x / 2, window_y / 4)

    hra_okno.blit(konechry_surface, konechry_rect)
    pygame.display.flip()

    time.sleep(0.5)

    konec_okno.geometry("+{}+{}".format(positionRight, positionDown))

    reset = Button (konec_okno, text = "Znova", command = resetgame)
    leave = Button (konec_okno, text = "Ukončit", command = leavegame)

    reset.pack()
    leave.pack()
  
    konec_okno.mainloop()  

while True:

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'

    if change_to == 'UP' and smer != 'DOWN':
        smer = 'UP'
    if change_to == 'DOWN' and smer != 'UP':
        smer = 'DOWN'
    if change_to == 'LEFT' and smer != 'RIGHT':
        smer = 'LEFT'
    if change_to == 'RIGHT' and smer != 'LEFT':
        smer = 'RIGHT'

    if smer == 'UP':
        had_pozice[1] -= 10
    if smer == 'DOWN':
        had_pozice[1] += 10
    if smer == 'LEFT':
        had_pozice[0] -= 10
    if smer == 'RIGHT':
        had_pozice[0] += 10

    had_telo.insert(0, list(had_pozice))
    if had_pozice[0] == papani_pozice[0] and had_pozice[1] == papani_pozice[1]:
        skore += 10
        papani_spawn = False
    else:
        had_telo.pop()

    if not papani_spawn:
        papani_pozice = [random.randrange(1, (window_x // 10)) * 10,
                         random.randrange(1, (window_y // 10)) * 10]

    papani_spawn = True
    hra_okno.fill(white)

    for pos in had_telo:
        pygame.draw.rect(hra_okno, black,
                         pygame.Rect(pos[0], pos[1], 10, 10))
        pygame.draw.rect(hra_okno, red, pygame.Rect(
            papani_pozice[0], papani_pozice[1], 10, 10))

    if had_pozice[0] < 0 or had_pozice[0] > window_x - 10:
        konechry()
    if had_pozice[1] < 0 or had_pozice[1] > window_y - 10:
        konechry()

    for block in had_telo[1:]:
        if had_pozice[0] == block[0] and had_pozice[1] == block[1]:
            konechry()

    ukaz_skore(1, black, 'Verdana', 18)

    pygame.display.update()
    fps.tick(had_rychlost)
