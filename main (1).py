# Import and initialize the pygame library
import pygame
import random
from codes import *

from pygame.locals import (
  K_ESCAPE,
  K_RETURN,
  KEYDOWN,
  QUIT,
  MOUSEBUTTONDOWN,
  MOUSEBUTTONUP,
)

#CONSTANTS

WIDTH, HEIGHT = 768, 672

SCREEN = pygame.display.set_mode([768, 672])

START_LOGO = pygame.image.load("MASTERMIND/start_screen_logo.png")
START_LOGO_RECT = START_LOGO.get_rect(center=(384, 336))
START_TEXT = pygame.image.load("MASTERMIND/start_screen_text.png")
START_TEXT_RECT = START_TEXT.get_rect(center=(384, 336))
START_OVERLAY = pygame.image.load("MASTERMIND/start_screen_overlay.png")
START_OVERLAY_RECT = START_OVERLAY.get_rect(center=(384, 336))

GAME_BACKGROUND = pygame.image.load("MASTERMIND/game_bg.png")
GAME_BACKGROUND_RECT = GAME_BACKGROUND.get_rect(center=(384, 336))
ENTER_BUTTON_1 = pygame.image.load("MASTERMIND/enter_button_1.png")
ENTER_BUTTON_1_RECT = ENTER_BUTTON_1.get_rect(center=(187.5, 604.5))
ENTER_BUTTON_2 = pygame.image.load("MASTERMIND/enter_button_2.png")
ENTER_BUTTON_2_RECT = ENTER_BUTTON_2.get_rect(center=(187.5, 604.5))

WIN_BACKGROUND = pygame.image.load("MASTERMIND/YOU_WIN.png")
WIN_BACKGROUND_RECT = WIN_BACKGROUND.get_rect(center=(384, 336))
LOSE_BACKGROUND = pygame.image.load("MASTERMIND/GAME_OVER.png")
LOSE_BACKGROUND_RECT = LOSE_BACKGROUND.get_rect(center=(384, 336))

FADE = pygame.image.load("MASTERMIND/fade.png")
FADE_RECT = FADE.get_rect(center=(384, 336))

ICON = pygame.image.load("MASTERMIND/icon.png")

pygame.display.set_caption("MASTERMIND")
pygame.display.set_icon(ICON)

PEGS = ["MASTERMIND/redButton.png","MASTERMIND/blueButton.png","MASTERMIND/greenButton.png", "MASTERMIND/yellowButton.png"]

LIGHTS = ["MASTERMIND/redLight.png", "MASTERMIND/whiteLight.png"]

SCORES = ["MASTERMIND/10.png","MASTERMIND/9.png","MASTERMIND/8.png","MASTERMIND/7.png","MASTERMIND/6.png","MASTERMIND/5.png","MASTERMIND/4.png","MASTERMIND/3.png","MASTERMIND/2.png","MASTERMIND/1.png"]

START_BACKGROUNDS = ["MASTERMIND/start_screen_bg_1.png","MASTERMIND/start_screen_bg_2.png"]

CORRECT_CODE = random.choice(CODES)

PEG_X_SPACE = 39
PEG_Y_SPACE = 44.1
LIGHT_X_SPACE = 18
LIGHT_Y_SPACE = 18
SCORES_X_VALUE = [622.5, 630, 628.5, 631.5, 630, 631.5, 630, 631.5, 633, 634.5]

# Global variables

peg_X_value = 184.5
peg_Y_value = 508.5
light_X_value = 340.5
light_Y_value = 496.5
guesses_count = 10
guesses = [[], [], [], [], [], [], [], [], [], []]
peg_1_colour_counter = 1
peg_2_colour_counter = 1
peg_3_colour_counter = 1
peg_4_colour_counter = 1
guesses_counter = 0
lights = []

game_result = ""

# Classes


class pegClass(pygame.sprite.Sprite):

  def __init__(self, x_value, y_value):
    super(pegClass, self).__init__()
    self.image = pygame.image.load(str(PEGS[0]))
    self.rect = self.image.get_rect(center=(x_value, y_value))

# Initialisation of PEGS

peg_1 = pegClass(peg_X_value, peg_Y_value)
peg_X_value = peg_X_value + PEG_X_SPACE
peg_2 = pegClass(peg_X_value, peg_Y_value)
peg_X_value = peg_X_value + PEG_X_SPACE
peg_3 = pegClass(peg_X_value, peg_Y_value)
peg_X_value = peg_X_value + PEG_X_SPACE
peg_4 = pegClass(peg_X_value, peg_Y_value)

# Start Music

clock = pygame.time.Clock()
running = True

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
pygame.init()

# Sub programs


def resetPegs():
  global peg_X_value, peg_Y_value, PEG_X_SPACE, PEG_Y_SPACE, peg_1, peg_2, peg_3, peg_4, peg_1_colour_counter, peg_2_colour_counter, peg_3_colour_counter, peg_4_colour_counter
  peg_X_value = peg_X_value - (PEG_X_SPACE * 3)
  peg_Y_value = peg_Y_value - PEG_Y_SPACE
  peg_1 = pegClass(peg_X_value, peg_Y_value)
  peg_X_value = peg_X_value + PEG_X_SPACE
  peg_2 = pegClass(peg_X_value, peg_Y_value)
  peg_X_value = peg_X_value + PEG_X_SPACE
  peg_3 = pegClass(peg_X_value, peg_Y_value)
  peg_X_value = peg_X_value + PEG_X_SPACE
  peg_4 = pegClass(peg_X_value, peg_Y_value)
  peg_1_colour_counter = 1
  peg_2_colour_counter = 1
  peg_3_colour_counter = 1
  peg_4_colour_counter = 1


def checkForInput():
  global peg_1_colour_counter, peg_2_colour_counter, peg_3_colour_counter, peg_4_colour_counter, guesses_counter, peg_1, peg_2, peg_3, peg_4, guesses_counter, light_Y_value, ENTER_BUTTON_1_RECT, ENTER_BUTTON_1, ENTER_BUTTON_2, ENTER_BUTTON_2_RECT, running
  for event in pygame.event.get():
    if event.type == KEYDOWN:
      if event.key == K_ESCAPE:
        running = False
    elif event.type == QUIT:
      running = False
    if event.type == pygame.MOUSEBUTTONDOWN:
      if peg_1.rect.collidepoint(pygame.mouse.get_pos()):
        if peg_1_colour_counter == 4:
          peg_1_colour_counter = 0
        peg_1.image =  pygame.image.load(str(PEGS[peg_1_colour_counter]))
        peg_1_colour_counter = peg_1_colour_counter + 1
        SCREEN.blit(peg_1.image, peg_1.rect)
    if event.type == pygame.MOUSEBUTTONDOWN:
      if peg_2.rect.collidepoint(pygame.mouse.get_pos()):
        if peg_2_colour_counter == 4:
          peg_2_colour_counter = 0
        peg_2.image = pygame.image.load(str(PEGS[peg_2_colour_counter]))
        peg_2_colour_counter = peg_2_colour_counter + 1
        SCREEN.blit(peg_2.image, peg_2.rect)
    if event.type == pygame.MOUSEBUTTONDOWN:
      if peg_3.rect.collidepoint(pygame.mouse.get_pos()):
        if peg_3_colour_counter == 4:
          peg_3_colour_counter = 0
        peg_3.image = pygame.image.load(str(PEGS[peg_3_colour_counter]))
        peg_3_colour_counter = peg_3_colour_counter + 1
        SCREEN.blit(peg_3.image, peg_3.rect)
    if event.type == pygame.MOUSEBUTTONDOWN:
      if peg_4.rect.collidepoint(pygame.mouse.get_pos()):
        if peg_4_colour_counter == 4:
          peg_4_colour_counter = 0
        peg_4.image = pygame.image.load(str(PEGS[peg_4_colour_counter]))
        peg_4_colour_counter = peg_4_colour_counter + 1
        SCREEN.blit(peg_4.image, peg_4.rect)
    if event.type == pygame.MOUSEBUTTONDOWN:
      if ENTER_BUTTON_1_RECT.collidepoint(pygame.mouse.get_pos()):
        guesses[guesses_counter] = [(peg_1_colour_counter - 1),(peg_2_colour_counter - 1),(peg_3_colour_counter - 1),(peg_4_colour_counter - 1)]
        guesses_counter = guesses_counter + 1
        resetPegs()
        checkWin()
        SCREEN.blit(ENTER_BUTTON_2, ENTER_BUTTON_2_RECT)
        pygame.display.update()
    if event.type == pygame.MOUSEBUTTONUP:
      if ENTER_BUTTON_1_RECT.collidepoint(pygame.mouse.get_pos()):
        if game_result == "":
          drawLights()
          drawPegs()
          SCREEN.blit(ENTER_BUTTON_1, ENTER_BUTTON_1_RECT)
          pygame.display.update()
          if guesses_counter == 0 or guesses_counter == 1 or guesses_counter == 5 or guesses_counter == 8:
            light_Y_value = light_Y_value - 42
          else:
            light_Y_value = light_Y_value - 45


def checkWin():
  global guesses_counter, game_result, CORRECT_CODE
  if guesses[guesses_counter - 1] == CORRECT_CODE:
    game_result = "W"
  elif guesses_counter == 10:
    game_result = "L"


def checkCode():
  global CORRECT_CODE, guesses, guesses_counter
  GUESS = guesses[guesses_counter - 1]
  CORRECT_CODE_TEMP = CORRECT_CODE[:]
  GUESS_TEMP = GUESS[:]
  flags = []

  for i in range(0, 4):
    if CORRECT_CODE[i] == GUESS[i]:
      flags.append(2)
      CORRECT_CODE_TEMP.remove(GUESS[i])
      GUESS_TEMP.remove(GUESS[i])

  for j in range(0, len(GUESS_TEMP)):
    if CORRECT_CODE_TEMP.count(GUESS_TEMP[j]) > 0:
      flags.append(1)
      CORRECT_CODE_TEMP.remove(GUESS_TEMP[j])

  return flags


def drawPegs():
  global peg_1, peg_2, peg_3, peg_4
  SCREEN.blit(peg_1.image, peg_1.rect)
  SCREEN.blit(peg_2.image, peg_2.rect)
  SCREEN.blit(peg_3.image, peg_3.rect)
  SCREEN.blit(peg_4.image, peg_4.rect)


def drawLights():
  global light_X_value, light_Y_value, LIGHT_X_SPACE, LIGHT_Y_SPACE, LIGHTS
  x_value = light_X_value
  y_value = light_Y_value
  lightsList = checkCode()
  for i in range(0, len(lightsList)):
    if i == 2:
      x_value = light_X_value
      y_value = light_Y_value + LIGHT_Y_SPACE
    if lightsList[i] == 2:
      light = pygame.image.load(LIGHTS[0])
      light_rect = light.get_rect(center=(x_value, y_value))
    elif lightsList[i] == 1:
      light = pygame.image.load(LIGHTS[1])
      light_rect = light.get_rect(center=(x_value, y_value))
    SCREEN.blit(light, light_rect)
    x_value = x_value + LIGHT_X_SPACE


def drawEndPegs():
  global guesses, guesses_counter, PEGS, CORRECT_CODE
  peg_X_value = 598.5
  peg_Y_value = 331.5
  PEG_X_SPACE = 39
  for i in range(0, 4):
    peg = pygame.image.load(PEGS[CORRECT_CODE[i]])
    peg_rect = peg.get_rect(center=(peg_X_value, peg_Y_value))
    SCREEN.blit(peg, peg_rect)
    peg_X_value = peg_X_value + PEG_X_SPACE
  peg_X_value = 598.5
  peg_Y_value = 409.5
  FINAL_GUESS = guesses[guesses_counter - 1]
  for i in range(0, 4):
    peg = pygame.image.load(PEGS[FINAL_GUESS[i]])
    peg_rect = peg.get_rect(center=(peg_X_value, peg_Y_value))
    SCREEN.blit(peg, peg_rect)
    peg_X_value = peg_X_value + PEG_X_SPACE


def drawWinScreen():
  global WIN_BACKGROUND, WIN_BACKGROUND_RECT, PEGS, SCORES, SCORES_X_VALUE, guesses_counter
  for i in range(0, 6):
    SCREEN.blit(FADE, FADE_RECT)
    pygame.display.update()
    clock.tick(10)
  for j in range(0, 5):
    SCREEN.blit(WIN_BACKGROUND, WIN_BACKGROUND_RECT)
    for x in range(0, (5 - j)):
      SCREEN.blit(FADE, FADE_RECT)
    pygame.display.update()
    clock.tick(10)
  SCREEN.blit(WIN_BACKGROUND, WIN_BACKGROUND_RECT)
  pygame.display.update()

  SCORE = pygame.image.load(SCORES[guesses_counter - 1])
  SCORE_RECT = SCORE.get_rect(center=(SCORES_X_VALUE[guesses_counter - 1],
                                      270))
  peg = pygame.image.load(PEGS[0])
  counter = 0
  timer_interval = 500
  timer_event = pygame.USEREVENT + 1
  pygame.time.set_timer(timer_event , timer_interval)
  start = True
  while start == True:
    clock.tick(60)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
          start = False
      elif event.type == timer_event:
        SCREEN.blit(SCORE, SCORE_RECT)
        drawEndPegs()
        peg_rect = peg.get_rect(center=(565.5, 499.5))
        SCREEN.blit(peg, peg_rect)
        counter = counter + 1
        if counter == 4:
          counter = 0
        peg = pygame.image.load(PEGS[counter])
        pygame.display.update()
  for i in range(0, 6):
    SCREEN.blit(FADE, FADE_RECT)
    pygame.display.update()
    clock.tick(10)


def drawLoseScreen():
  global LOSE_BACKGROUND, LOSE_BACKGROUND_RECT, PEGS, SCORES, SCORES_X_VALUE, guesses_counter
  for i in range(0, 6):
    SCREEN.blit(FADE, FADE_RECT)
    pygame.display.update()
    clock.tick(10)
  for j in range(0, 5):
    SCREEN.blit(LOSE_BACKGROUND, LOSE_BACKGROUND_RECT)
    for x in range(0, (5 - j)):
      SCREEN.blit(FADE, FADE_RECT)
    pygame.display.update()
    clock.tick(10)
  SCREEN.blit(LOSE_BACKGROUND, LOSE_BACKGROUND_RECT)
  pygame.display.update()

  SCORE = pygame.image.load(SCORES[guesses_counter - 1])
  SCORE_RECT = SCORE.get_rect(center=(SCORES_X_VALUE[guesses_counter - 1],
                                      270))
  SCREEN.blit(SCORE, SCORE_RECT)
  drawEndPegs()
  peg = pygame.image.load(PEGS[0])
  counter = 0
  timer_interval = 500
  timer_event = pygame.USEREVENT + 1
  pygame.time.set_timer(timer_event , timer_interval)
  start = True
  while start == True:
    clock.tick(60)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
          start = False
      elif event.type == timer_event:
        peg_rect = peg.get_rect(center=(565.5, 499.5))
        SCREEN.blit(peg, peg_rect)
        counter = counter + 1
        if counter == 4:
          counter = 0
        peg = pygame.image.load(PEGS[counter])
        pygame.display.update()
  for i in range(0, 6):
    SCREEN.blit(FADE, FADE_RECT)
    pygame.display.update()
    clock.tick(10)


def startScreen():
  global START_BACKGROUNDS
  START_BACKGROUND =  pygame.image.load(START_BACKGROUNDS[0])
  counter = 0
  timer_interval = 250
  timer_event = pygame.USEREVENT + 1
  pygame.time.set_timer(timer_event , timer_interval)
  start = True
  while start == True:
    clock.tick(60)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
          start = False
      elif event.type == timer_event:
        START_BACKGROUND_RECT = START_BACKGROUND.get_rect(center=(384, 336))
        SCREEN.blit(START_BACKGROUND, START_BACKGROUND_RECT)
        SCREEN.blit(START_LOGO, START_LOGO_RECT)
        SCREEN.blit(START_TEXT, START_TEXT_RECT)
        SCREEN.blit(START_OVERLAY, START_OVERLAY_RECT)
        counter = counter + 1
        if counter == 2:
          counter = 0
        START_BACKGROUND = pygame.image.load(START_BACKGROUNDS[counter])
        pygame.display.update()
  for i in range(0, 6):
    SCREEN.blit(FADE, FADE_RECT)
    pygame.display.update()
    clock.tick(10)

  pygame.mixer.music.stop()

  for j in range(0, 5):
    SCREEN.blit(GAME_BACKGROUND, GAME_BACKGROUND_RECT)
    for x in range(0, (5 - j)):
      SCREEN.blit(FADE, FADE_RECT)
    pygame.display.update()
    clock.tick(10)

  SCREEN.blit(GAME_BACKGROUND, GAME_BACKGROUND_RECT)
  drawPegs()
  SCREEN.blit(ENTER_BUTTON_1, ENTER_BUTTON_1_RECT)


def mainLoop():
  global running, game_result
  while running:
    if game_result == "":
      checkForInput()
      pygame.display.flip()
    elif game_result == "W":
      drawWinScreen()
      running = False
    elif game_result == "L":
      drawLoseScreen()
      running = False

  pygame.quit()


def main():
  # play startScreen music

  pygame.mixer.music.load("MASTERMIND/start_screen_soundtrack.wav")
  pygame.mixer.music.play(-1)

  # display startScreen

  startScreen()

  # play mainScreen music

  pygame.mixer.music.load("MASTERMIND/game_soundtrack.wav")
  pygame.mixer.music.play(-1)

  # start mainLoop

  mainLoop()

# Main Program
if __name__ == "__main__":
  main()