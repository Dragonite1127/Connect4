import pygame
from pygame import transform
from pygame.locals import *
import Board
import random
import Color
import AI

pygame.init()
FPS = 60

"""Board dimensions."""
WIDTH, HEIGHT = 700, 600
TILE_SIZE = 100
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect 4 by Mehul Gandhi")
font = pygame.font.SysFont(None, 20)

"""Colors."""
BLUE = [0, 0, 255]
BLACK = [0, 0, 0]

"""True iff a button is selected."""
click = False


def main_menu():
    """Main menu."""
    global click
    clock = pygame.time.Clock()
    while True:
        SCREEN.fill(BLACK)
        draw_text("Main Menu", 20, (255, 255, 255), SCREEN, 300, 20)

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(250, 50, 200, 50)  # AI
        button_2 = pygame.Rect(250, 200, 200, 50)  # Multiplayer
        button_3 = pygame.Rect(250, 350, 200, 50)  # AI vs AI
        button_4 = pygame.Rect(250, 500, 200, 50)  # QUIT

        if button_1.collidepoint((mx, my)):
            if click:
                click = False
                main_ai()
                break
        elif button_2.collidepoint((mx, my)):
            if click:
                click = False
                main()
                break
        elif button_3.collidepoint((mx, my)):
            if click:
                click = False
                ai_against_ai()
                break
        elif button_4.collidepoint((mx, my)):
            if click:
                click = False
                pygame.quit()
                break
        else:
            click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        pygame.draw.rect(SCREEN, (255, 0, 0), button_1)
        draw_text("Single Player Game", 30, (255, 255, 255), SCREEN, 252, 65)
        pygame.draw.rect(SCREEN, (255, 0, 0), button_2)
        draw_text("Multiplayer Game", 30, (255, 255, 255), SCREEN, 265, 215)
        pygame.draw.rect(SCREEN, (255, 0, 0), button_3)
        draw_text("AI vs AI", 40, (255, 255, 255), SCREEN, 295, 360)
        pygame.draw.rect(SCREEN, (255, 0, 0), button_4)
        draw_text("Quit Game", 30, (255, 255, 255), SCREEN, 295, 515)
        pygame.display.update()
        clock.tick(FPS)


def play_again(player: Color.Colors):
    """Creates two buttons: play again and quit.
    Quits the game if quit is selected.
    Runs the function main if play again is selected."""
    global click
    click = False
    clock = pygame.time.Clock()
    player = Color.Colors.tostring(player)
    while True:
        if player == "YELLOW":
            draw_text(f"{player} wins!", 50, BLACK, SCREEN, 225, 20)
        elif player == "RED":
            draw_text(f"{player} wins!", 50, BLACK, SCREEN, 270, 20)
        else:
            draw_text("DRAW!", 50, BLACK, SCREEN, 225, 20)

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(250, 50, 200, 50)  # AI
        button_2 = pygame.Rect(250, 200, 200, 50)  # Multiplayer
        button_3 = pygame.Rect(250, 350, 200, 50)  # AI vs AI
        button_4 = pygame.Rect(250, 500, 200, 50)  # QUIT

        if button_1.collidepoint((mx, my)):
            if click:
                click = False
                main_ai()
                break
        elif button_2.collidepoint((mx, my)):
            if click:
                click = False
                main()
                break
        elif button_3.collidepoint((mx, my)):
            if click:
                click = False
                ai_against_ai()
                break
        elif button_4.collidepoint((mx, my)):
            if click:
                click = False
                pygame.quit()
                break
        else:
            click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        pygame.draw.rect(SCREEN, (255, 0, 0), button_1)
        draw_text("Single Player Game", 30, (255, 255, 255), SCREEN, 252, 65)
        pygame.draw.rect(SCREEN, (255, 0, 0), button_2)
        draw_text("Multiplayer Game", 30, (255, 255, 255), SCREEN, 265, 215)
        pygame.draw.rect(SCREEN, (255, 0, 0), button_3)
        draw_text("AI vs AI", 40, (255, 255, 255), SCREEN, 295, 360)
        pygame.draw.rect(SCREEN, (255, 0, 0), button_4)
        draw_text("Quit Game", 30, (255, 255, 255), SCREEN, 295, 515)
        pygame.display.update()
        clock.tick(FPS)


def draw_text(text: str, size: int, color, surface, x: int, y: int):
    """Draw text on the screen."""
    font = pygame.font.SysFont(None, size)
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


def generate_game(screen):
    """Generates the board game with player1 and player2
    colors decided by a coin toss. """
    coin_toss = random.randint(0, 1)

    if coin_toss == 1:
        game = Board.Board(WIDTH, HEIGHT, Color.Colors.YELLOW, Color.Colors.RED)
    else:
        game = Board.Board(WIDTH, HEIGHT, Color.Colors.RED, Color.Colors.YELLOW)
    return game, game.player1


def ai_against_ai():
    """A main function where an AI player plays against another AI player."""
    clock = pygame.time.Clock()
    run = True
    game, player = generate_game(SCREEN)
    clock.tick(FPS)
    draw_window()
    screenClass = screenUpdate(SCREEN, game)
    game.screen = screenClass
    screenClass.draw_grid()
    ai_1 = AI.AI(game, game.player1)
    ai_2 = AI.AI(game, game.player2)
    while run:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            else:
                ai_1_move = ai_1.get_move()
                game.make_move(ai_1_move[0], ai_1_move[1], game.player1)
                winner = game.check_win()
                if winner != Color.Colors.WHITE:
                    run = False
                    play_again(winner)
                ai_2_move = ai_2.get_move()
                game.make_move(ai_2_move[0], ai_2_move[1], game.player2)
                winner = game.check_win()
                if winner != Color.Colors.WHITE:
                    run = False
                    play_again(winner)
    pygame.quit()


def main_ai():
    """A main function for a single player game against an AI player."""
    clock = pygame.time.Clock()
    run = True
    game, player = generate_game(SCREEN)
    clock.tick(FPS)
    draw_window()
    screenClass = screenUpdate(SCREEN, game)
    game.screen = screenClass
    screenClass.draw_grid()
    ai = AI.AI(game, game.player2)
    while run:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x = event.pos[1]
                mouse_y = event.pos[0]
                clicked_row = int(mouse_x // TILE_SIZE)
                clicked_col = int(mouse_y // TILE_SIZE)
                if game.make_move(clicked_row, clicked_col, player) != False:
                    winner = game.check_win()
                    if winner != Color.Colors.WHITE:
                        run = False
                        play_again(winner)
                        return

                    ai_move = ai.get_move()
                    game.make_move(ai_move[0], ai_move[1], game.player2)
                    winner = game.check_win()
                    if winner != Color.Colors.WHITE:
                        run = False
                        play_again(winner)
    pygame.quit()


def main():
    clock = pygame.time.Clock()
    run = True
    game, player = generate_game(False)
    clock.tick(FPS)
    draw_window()
    screenClass = screenUpdate(SCREEN, game)
    game.screen = screenClass
    screenClass.draw_grid()
    while run:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:

                mouse_x = event.pos[1]
                mouse_y = event.pos[0]
                clicked_row = int(mouse_x // TILE_SIZE)
                clicked_col = int(mouse_y // TILE_SIZE)
                game.make_move(clicked_row, clicked_col, player)
                winner = game.check_win()
                if winner != Color.Colors.WHITE:
                    run = False
                    play_again(winner)
                player = game.whose_move()
    pygame.quit()


def draw_window():
    """Fills the board with the color BLUE."""
    SCREEN.fill(BLUE)


class screenUpdate:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game

    def draw_grid(self):
        """Draws all board game tiles."""
        for i in range(0, 6):
            for j in range(0, 7):
                tile = self.game.board[i][j]
                SCREEN.blit(transform.scale(tile.get_path(), (WIDTH / 7, HEIGHT / 6)), (tile.y, tile.x))
                pygame.display.update()

    def update_tile(self, row, col):
        """Updates a single tile. Used when swapping in the Board class."""
        self.screen.blit(transform.scale(self.game.board[row][col].get_path(), (WIDTH / 7, HEIGHT / 6)),
                         (col * TILE_SIZE, row * TILE_SIZE))
        pygame.display.update()


if __name__ == '__main__':
    main_menu()
