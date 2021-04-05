# importing the required libraries
import pygame as pg
import sys
import time
from pygame.locals import *

position_x = None
position_y = None
XO = 'X'
winner = None
draw = None
width = 400
height = 400
white = (255, 255, 255)
line_color = (0, 0, 0)
board = [[None] * 3, [None] * 3, [None] * 3]
pg.init()
fps = 60
CLOCK = pg.time.Clock()
screen = pg.display.set_mode((width, height + 100), 0, 32)
pg.display.set_caption("My Tic Tac Toe")
initiating_window = pg.image.load("img_background.jpg")
x_img = pg.image.load("img_x.png")
y_img = pg.image.load("img_o.png")
initiating_window = pg.transform.scale(initiating_window, (width, height + 100))
x_img = pg.transform.scale(x_img, (80, 80))
o_img = pg.transform.scale(y_img, (80, 80))


def game_initiating_window():
    screen.blit(initiating_window, (0, 0))
    pg.display.update()
    time.sleep(1)
    screen.fill(white)
    pg.draw.line(screen, line_color, (width / 3, 0), (width / 3, height), 7)
    pg.draw.line(screen, line_color, (width / 3 * 2, 0), (width / 3 * 2, height), 7)
    pg.draw.line(screen, line_color, (0, height / 3), (width, height / 3), 7)
    pg.draw.line(screen, line_color, (0, height / 3 * 2), (width, height / 3 * 2), 7)
    draw_status()


def draw_status():
    global draw, XO
    if winner is None:
        message = f'{XO}\'s turn'
    else:
        message = f'{winner} has won!'
    if draw:
        message = "Game Draw !"
    font = pg.font.Font(None, 30)
    text = font.render(message, True, (255, 255, 255))
    screen.fill((0, 0, 0), (0, 400, 500, 100))
    text_rect = text.get_rect(center=(width / 2, 500 - 50))
    screen.blit(text, text_rect)
    pg.display.update()


def check_win():
    global board, winner, draw, XO
    for row in range(0, 3):
        if (board[row][0] == board[row][1] == board[row][2]) and (board[row][0] is not None):
            winner = board[row][0]
            pg.draw.line(screen, (250, 0, 0),
                         (0, ((row + 1) * height / 3) - (height / 6)),
                         (width, ((row + 1) * height / 3) - (height / 6)),
                         4)
            break
    for col in range(0, 3):
        if (board[0][col] == board[1][col] == board[2][col]) and (board[0][col] is not None):
            winner = board[0][col]
            pg.draw.line(screen, (250, 0, 0), ((col + 1) * width / 3 - width / 6, 0),
                         (((col + 1) * width / 3) - (width / 6), height), 4)
            break
    # check for diagonal winners
    if (board[0][0] == board[1][1] == board[2][2]) and (board[0][0] is not None):
        # game won diagonally left to right
        winner = board[0][0]
        pg.draw.line(screen, (250, 70, 70), (50, 50), (350, 350), 4)

    if (board[0][2] == board[1][1] == board[2][0]) and (board[0][2] is not None):
        # game won diagonally right to left
        winner = board[0][2]
        pg.draw.line(screen, (250, 70, 70), (350, 50), (50, 350), 4)
    if all([all(row) for row in board]) and winner is None:
        global XO
        draw = True


def drawXO(row, col):
    global board, XO, position_x, position_y
    if row == 1:
        position_x = 30
    if row == 2:
        position_x = width / 3 + 30
    if row == 3:
        position_x = width / 3 * 2 + 30
    if col == 1:
        position_y = 30
    if col == 2:
        position_y = height / 3 + 30
    if col == 3:
        position_y = height / 3 * 2 + 30
    board[row - 1][col - 1] = XO
    if XO == 'X':
        screen.blit(x_img, (position_y, position_x))
        XO = 'O'
        check_win()
        draw_status()
    else:
        screen.blit(o_img, (position_y, position_x))
        XO = 'X'
        check_win()
        draw_status()
    pg.display.update()


def user_click():
    x, y = pg.mouse.get_pos()
    if x < width / 3:
        col = 1
    elif x < width / 3 * 2:
        col = 2
    elif x < width:
        col = 3
    else:
        col = None
    if y < height / 3:
        row = 1
    elif y < height / 3 * 2:
        row = 2
    elif y < height:
        row = 3
    else:
        row = None
    if row and col and board[row - 1][col - 1] is None:
        global XO
        drawXO(row, col)


def reset_game():
    global board, winner, XO, draw
    time.sleep(1)
    XO = 'X'
    draw = False
    game_initiating_window()
    winner = None
    board = [[None] * 3, [None] * 3, [None] * 3]


game_initiating_window()
while True:
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            user_click()
            if winner or draw:
                reset_game()
    pg.display.update()
    CLOCK.tick(fps)
