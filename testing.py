"""
PLEASE READ THE COMMENTS BELOW AND THE HOMEWORK DESCRIPTION VERY CAREFULLY BEFORE YOU START CODING

 The file where you will need to create the GUI which should include (i) drawing the grid, (ii) call your Minimax/Negamax functions
 at each step of the game, (iii) allowing the controls on the GUI to be managed (e.g., setting board size, using 
                                                                                 Minimax or Negamax, and other options)
 In the example below, grid creation is supported using pygame which you can use. You are free to use any other 
 library to create better looking GUI with more control. In the __init__ function, GRID_SIZE (Line number 36) is the variable that
 sets the size of the grid. Once you have the Minimax code written in multiAgents.py file, it is recommended to test
 your algorithm (with alpha-beta pruning) on a 3x3 GRID_SIZE to see if the computer always tries for a draw and does 
 not let you win the game. Here is a video tutorial for using pygame to create grids http://youtu.be/mdTeqiWyFnc
 
 
 PLEASE CAREFULLY SEE THE PORTIONS OF THE CODE/FUNCTIONS WHERE IT INDICATES "YOUR CODE BELOW" TO COMPLETE THE SECTIONS
 
"""
#import PySimpleGUI as sg
import pygame
import numpy as np
from GameStatus_5120 import GameStatus
from multiAgents import minimax, negamax
import sys, random

mode = "player_vs_ai" # default mode for playing the game (player vs AI)

width, height = 1000, 1000
# screen = pygame.display.set_mode((width, height))

COLOR_INACTIVE = (100, 80, 255)
COLOR_ACTIVE = (100, 200, 255)
COLOR_LIST_INACTIVE = (255, 100, 100)
COLOR_LIST_ACTIVE = (255, 150, 150)

class Button:
    def __init__(self, text, position, size, bg_color, text_color, action=None):
        self.text = text
        self.position = position
        self.size = size
        self.bg_color = bg_color
        self.text_color = text_color
        self.action = action

    def draw(self, screen):
        font = pygame.font.Font(None, 32)
        pygame.draw.rect(screen, self.bg_color, (self.position, self.size))
        text_surface = font.render(self.text, True, self.text_color)
        text_pos = (self.position[0] + self.size[0] / 2, self.position[1] + self.size[1] / 2)
        # text_rect = text_surface.get_rect(center=self.position)
        text_rect = text_surface.get_rect(center=text_pos)
        screen.blit(text_surface, text_rect)

    def is_mouse_over(self, pos):
        x, y = pos
        return (self.position[0] <= x <= self.position[0] + self.size[0] and
                self.position[1] <= y <= self.position[1] + self.size[1])

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_mouse_over(event.pos):
                if self.action:
                    self.action()
    
class RadioButton(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, font, text, action=None):
        super().__init__() 
        text_surf = font.render(text, True, (0, 0, 0))
        self.button_image = pygame.Surface((w, h))
        self.button_image.fill((96, 96, 96))
        self.button_image.blit(text_surf, text_surf.get_rect(center = (w // 2, h // 2)))
        self.hover_image = pygame.Surface((w, h))
        self.hover_image.fill((96, 96, 96))
        self.hover_image.blit(text_surf, text_surf.get_rect(center = (w // 2, h // 2)))
        pygame.draw.rect(self.hover_image, (96, 196, 96), self.hover_image.get_rect(), 3)
        self.clicked_image = pygame.Surface((w, h))
        self.clicked_image.fill((96, 196, 96))
        self.clicked_image.blit(text_surf, text_surf.get_rect(center = (w // 2, h // 2)))
        self.image = self.button_image
        self.rect = pygame.Rect(x, y, w, h)
        self.clicked = False
        self.buttons = None
        self.action = action

    def setRadioButtons(self, buttons):
        self.buttons = buttons

    def update(self, event_list):
        hover = self.rect.collidepoint(pygame.mouse.get_pos())
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if hover and event.button == 1:
                    for rb in self.buttons:
                        rb.clicked = False
                    self.clicked = True
        
        self.image = self.button_image
        if self.clicked:
            self.image = self.clicked_image
            if self.action:
                self.action()
        elif hover:
            self.image = self.hover_image

class RandomBoardTicTacToe:
    def __init__(self, size = (500, 700)):

        self.size = size
        self.uiOffset = 200 # to make room for ui
        self.width, self.height = size[0], size[1] - self.uiOffset
        # self.size = self.width, self.height = size
        # Define some colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)

        # Grid Size
        self.GRID_SIZE = 5
        self. OFFSET = 5

        self.CIRCLE_COLOR = (140, 146, 172)
        self.CROSS_COLOR = (140, 146, 172)

        # This sets the WIDTH and HEIGHT of each grid location
        # self.WIDTH = self.size[0]/self.GRID_SIZE - self.OFFSET
        # self.HEIGHT = self.size[1]/self.GRID_SIZE - self.OFFSET
        self.WIDTH = self.width/self.GRID_SIZE - self.OFFSET
        self.HEIGHT = self.height/self.GRID_SIZE - self.OFFSET

        # This sets the margin between each cell
        self.MARGIN = 5

        self.playerXO = "X"
        self.score = 0
        self.game_state = GameStatus(np.zeros((self.GRID_SIZE, self.GRID_SIZE)), False)

        # Initialize pygame
        pygame.init()
        font50 = pygame.font.SysFont(None, 50)

        self.button = Button("Restart game", (300, 100), (200, 50), (0, 255, 0), (255, 255, 255), action=lambda: self.game_reset())
        self.radioButtons = [
            RadioButton(50, 40, 50, 40, font50, "X", action=lambda: self.set_player_side("X")),
            RadioButton(50, 80, 50, 40, font50, "O", action=lambda: self.set_player_side("O")),
        ]
        for rb in self.radioButtons:
            rb.setRadioButtons(self.radioButtons)
        self.radioButtons[0].clicked = True
        self.group = pygame.sprite.Group(self.radioButtons)

        self.boardSelector = [
            RadioButton(120, 40, 100, 40, font50, "3x3", action=lambda: self.set_grid_size(3)),
            RadioButton(120, 80, 100, 40, font50, "4x4", action=lambda: self.set_grid_size(4)),
            RadioButton(120, 120, 100, 40, font50, "5x5", action=lambda: self.set_grid_size(5)),
        ]
        for rb in self.boardSelector:
            rb.setRadioButtons(self.boardSelector)
        self.boardSelector[0].clicked = True
        self.boardGroup = pygame.sprite.Group(self.boardSelector)

        self.game_reset()
        
    def set_player_side(self, choice):
        if choice != self.playerXO:
            self.playerXO = choice
            self.game_state = GameStatus(np.zeros((self.GRID_SIZE, self.GRID_SIZE)), self.playerXO == "O")
            self.game_reset()

    def set_grid_size(self, size):
        if(size != self.GRID_SIZE):
            self.GRID_SIZE = size
            self.game_state = GameStatus(np.zeros((self.GRID_SIZE, self.GRID_SIZE)), self.playerXO == "O")
            self.game_reset()

    def draw_game(self):
        # Create a 2 dimensional array using the column and row variables
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Tic Tac Toe Random Grid")
        self.screen.fill(self.BLACK)
        # Draw the grid
        
        """
        YOUR CODE HERE TO DRAW THE GRID OTHER CONTROLS AS PART OF THE GUI
        """
        self.button.draw(self.screen)
        # self.playerSelection.draw(self.screen)
        text_surface = pygame.font.Font(None, 32).render("Score: " + str(self.score), True, (0, 255, 0))
        text_pos = (400, 40)
        text_rect = text_surface.get_rect(center=text_pos)
        self.screen.blit(text_surface, text_rect)

        for row in range(self.GRID_SIZE):
            for column in range(self.GRID_SIZE):
                pygame.draw.rect(self.screen, self.WHITE,
                                 [(self.MARGIN + self.WIDTH) * column + self.MARGIN,
                                  (self.MARGIN + self.HEIGHT) * row + self.MARGIN + self.uiOffset,
                                  self.WIDTH, self.HEIGHT])
        
        pygame.display.update()
        self.play_game()

    def change_turn(self):

        if(self.game_state.turn_O):
            pygame.display.set_caption("Tic Tac Toe - O's turn")
        else:
            pygame.display.set_caption("Tic Tac Toe - X's turn")


    def draw_circle(self, x, y):
        """
        YOUR CODE HERE TO DRAW THE CIRCLE FOR THE NOUGHTS PLAYER
        
        """
        color = (255, 0, 128)
        center = (x, y)
        radius = (self.WIDTH / 2)

        pygame.draw.circle(self.screen, color, center, radius)
        # screen, color, center, radius
        

    def draw_cross(self, x, y, column, row):
        """
        YOUR CODE HERE TO DRAW THE CROSS FOR THE CROSS PLAYER AT THE CELL THAT IS SELECTED VIA THE gui
        """
        x_pos = (self.MARGIN + self.WIDTH) * column + self.MARGIN
        y_pos = (self.MARGIN + self.HEIGHT) * row + self.MARGIN + self.uiOffset

        pygame.draw.line(self.screen, self.RED, (x_pos, y_pos), (x_pos + self.WIDTH, y_pos + self.HEIGHT), 5)
        pygame.draw.line(self.screen, self.RED, (x_pos, y_pos + self.HEIGHT), (x_pos + self.WIDTH, y_pos), 5)


    def is_game_over(self):

        """
        YOUR CODE HERE TO SEE IF THE GAME HAS TERMINATED AFTER MAKING A MOVE. YOU SHOULD USE THE IS_TERMINAL()
        FUNCTION FROM GAMESTATUS_5120.PY FILE (YOU WILL FIRST NEED TO COMPLETE IS_TERMINAL() FUNCTION)
        
        YOUR RETURN VALUE SHOULD BE TRUE OR FALSE TO BE USED IN OTHER PARTS OF THE GAME
        """
        return self.game_state.is_terminal()
    

    def move(self, move):
        self.game_state = self.game_state.get_new_state(move)


    def play_ai(self):
        """
        YOUR CODE HERE TO CALL MINIMAX OR NEGAMAX DEPENDEING ON WHICH ALGORITHM SELECTED FROM THE GUI
        ONCE THE ALGORITHM RETURNS THE BEST MOVE TO BE SELECTED, YOU SHOULD DRAW THE NOUGHT (OR CIRCLE DEPENDING
        ON WHICH SYMBOL YOU SELECTED FOR THE AI PLAYER)
        
        THE RETURN VALUES FROM YOUR MINIMAX/NEGAMAX ALGORITHM SHOULD BE THE SCORE, MOVE WHERE SCORE IS AN INTEGER
        NUMBER AND MOVE IS AN X,Y LOCATION RETURNED BY THE AGENT
        """
        score, move = minimax(self.game_state, 10, True)
        # negamax(GameStatus, 10, 1)
        movex, movey = move
        if self.playerXO == "X":
            self.draw_circle(movex * self.WIDTH, movey * self.HEIGHT + self.uiOffset)
        else:
            self.draw_cross(movex * self.WIDTH, movey * self.HEIGHT, movex, movey)
        
        self.move((movex, movey))
        self.change_turn()
        pygame.display.update()
        terminal = self.game_state.is_terminal()
        self.game_state.get_scores(terminal)
        """ USE self.game_state.get_scores(terminal) HERE TO COMPUTE AND DISPLAY THE FINAL SCORES """



    def game_reset(self):
        self.draw_game()
        """
        YOUR CODE HERE TO RESET THE BOARD TO VALUE 0 FOR ALL CELLS AND CREATE A NEW GAME STATE WITH NEWLY INITIALIZED
        BOARD STATE
        """
        
        pygame.display.update()

    def play_game(self, mode = "player_vs_ai"):
        done = False

        clock = pygame.time.Clock()

        while not done:
            event_list = pygame.event.get()

            for event in event_list:  # User did something
                """
                YOUR CODE HERE TO CHECK IF THE USER CLICKED ON A GRID ITEM. EXIT THE GAME IF THE USER CLICKED EXIT
                """
                # print(event.type)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    print(x, y)
                    # convert screen coords to board coords
                    if y < self.height: # make sure its not doing this with ui elements
                        boardx = x % self.GRID_SIZE
                        boardy = y % self.GRID_SIZE
                        print(boardx, boardy)
                        if (boardx, boardy) in self.game_state.get_moves():
                            if self.playerXO == "X":
                                self.draw_cross(x, y, boardx, boardy)
                            else:
                                self.draw_circle(x, y)
                            self.game_state = self.game_state.get_new_state((boardx, boardy))
                            self.change_turn()
                            self.play_ai()
                """
                YOUR CODE HERE TO HANDLE THE SITUATION IF THE GAME IS OVER. IF THE GAME IS OVER THEN DISPLAY THE SCORE,
                THE WINNER, AND POSSIBLY WAIT FOR THE USER TO CLEAR THE BOARD AND START THE GAME AGAIN (OR CLICK EXIT)
                """
                if self.is_game_over():
                    self.score = self.game_state.get_scores()

                """
                YOUR CODE HERE TO NOW CHECK WHAT TO DO IF THE GAME IS NOT OVER AND THE USER SELECTED A NON EMPTY CELL
                IF CLICKED A NON EMPTY CELL, THEN GET THE X,Y POSITION, SET ITS VALUE TO 1 (SELECTED BY HUMAN PLAYER),
                DRAW CROSS (OR NOUGHT DEPENDING ON WHICH SYMBOL YOU CHOSE FOR YOURSELF FROM THE gui) AND CALL YOUR 
                PLAY_AI FUNCTION TO LET THE AGENT PLAY AGAINST YOU
                """
                
                # if event.type == pygame.MOUSEBUTTONUP:
                    # Get the position
                    
                    # Change the x/y screen coordinates to grid coordinates
                    
                    # Check if the game is human vs human or human vs AI player from the GUI. 
                    # If it is human vs human then your opponent should have the value of the selected cell set to -1
                    # Then draw the symbol for your opponent in the selected cell
                    # Within this code portion, continue checking if the game has ended by using is_terminal function
                if event.type == pygame.QUIT:
                    # running = False
                    done = True
                self.button.handle_event(event)
                    
            # Update the screen with what was drawn.
            # selected_option = self.playerSelection.update(event_list)
            # if selected_option >= 0:
            #     self.playerSelection.main = self.playerSelection.options[selected_option]
            # self.playerSelection.draw(self.screen)
            # pygame.display.flip()

            self.group.update(event_list)
            self.group.draw(self.screen)
            self.boardGroup.update(event_list)
            self.boardGroup.draw(self.screen)
            pygame.display.update()

        pygame.quit()

tictactoegame = RandomBoardTicTacToe()
"""
YOUR CODE HERE TO SELECT THE OPTIONS VIA THE GUI CALLED FROM THE ABOVE LINE
AFTER THE ABOVE LINE, THE USER SHOULD SELECT THE OPTIONS AND START THE GAME. 
YOUR FUNCTION PLAY_GAME SHOULD THEN BE CALLED WITH THE RIGHT OPTIONS AS SOON
AS THE USER STARTS THE GAME
"""


                    
#button = Button("Click me", (300, 200), (200, 50), (0, 255, 0), (255, 255, 255), action=lambda: print("Button clicked"))

# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         button.handle_event(event)
