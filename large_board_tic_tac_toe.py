import PySimpleGUI as sg # may need to pip install this, pip install pysimplegui
import pygame
import numpy as np
from GameStatus_5120 import GameStatus
from multiAgents import minimax, negamax
import sys, random

def create_new_board(size):
    return {(row, col): '' for row in range(size) for col in range(size)}

def update_board_display(window, board):
    if isinstance(board, dict):
        for (row, col), value in board.items():
            print(value)
            window[(row, col)].update(value)

def main():
    size = 3

    x_wins = 0
    o_wins = 0
    draws = 0

    player_turn = True
    player = None

    # Pre-game layout for choosing 'X' or 'O'
    pre_game_layout = [
        [sg.Text('Choose your side:')],
        [sg.Button('X'), sg.Button('O')]
    ]

    # Create and display the pre-game window
    pre_game_window = sg.Window('Choose Side', pre_game_layout)
    event, values = pre_game_window.read()
    pre_game_window.close()

    # Initialize player based on choice
    if event in ('X', 'O'):
        player = event
    else:
        return  # Exit if the window is closed or another event occurs
    
    if player is None:  # Check if player has been set
        return  # Exit the function if player wasn't set

    ai_player = 'O' if player == 'X' else 'X'  # 

    # Main game layout
    layout = [
        [sg.Text('Select Board Size')],
        [sg.Button('3x3'), sg.Button('4x4'), sg.Button('5x5')],
        [sg.Column([[sg.Button(size=(3, 1), key=(row, col), pad=(0, 0)) for col in range(3)] for row in range(3)], key='-BOARD-')],
        [sg.Button('Reset'), sg.Button('Exit')]
    ]

    # Create the main game window
    window = sg.Window('Tic-Tac-Toe', layout, use_default_focus=False)

    # Initialize the board
    board = create_new_board(3)
    game_status = GameStatus(np.zeros((3, 3)), player=="O")

    # Event Loop
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Exit':
            break
       # if event == 'Reset':
          #  board = create_new_board(len(board))
            #update_board_display(window, board)
        if event == 'Reset':
            size = int(len(board) ** 0.5)  # Calculate the board size (sqrt of total cells)
            board = create_new_board(size)  # Recreate the board for the calculated size
    
            # Update all buttons on the board to show blank spaces
            for row in range(size):
                for col in range(size):
                    window[(row, col)].update('')
            game_status = GameStatus(np.zeros((size, size)), player=="O")

        elif event in ['3x3', '4x4', '5x5']:
            size = int(event[0])
            board = create_new_board(size)
            game_status = GameStatus(np.zeros((size, size)), player=="O")
            window.close()
            layout = [
                [sg.Text('Select Board Size')],
                [sg.Button('3x3'), sg.Button('4x4'), sg.Button('5x5')],
                [sg.Column([[sg.Button(size=(3, 1), key=(row, col), pad=(0, 0)) for col in range(size)] for row in range(size)], key='-BOARD-')],
                [sg.Button('Reset'), sg.Button('Exit')]
            ]
            window = sg.Window('Tic-Tac-Toe', layout, use_default_focus=False)
        elif event in board:
            if player_turn and board[event] == '':
                board[event] = player
                window[event].update(player)
                player_turn = False
                game_status = game_status.get_new_state(event)
        if not player_turn:
            # AI's turn to make a move
            board, player_turn, move, game_status = ai_player_moves(game_status, board, size, ai_player == 'O')
            # update_board_display(window, board)
            if move: 
                window[move].update(ai_player)
                player_turn = True

    window.close()

def convert_board_to_list(board_dict, size):
    board_list = [[0 for _ in range(size)] for _ in range(size)]
    for (row, col), value in board_dict.items():
        if value == 'X':
            board_list[row][col] = -1  # Assuming 'X' is represented by -1
        elif value == 'O':
            board_list[row][col] = 1  # Assuming 'O' is represented by 1
        # Empty cells are represented by 0, which is already the default
    return board_list

def convert_list_to_dict(board_list):
    board_dict = {}
    size = len(board_list)
    for row in range(size):
        for col in range(size):
            cell_value = board_list[row][col]
            if cell_value == 1:
                board_dict[(row, col)] = 'O'
            elif cell_value == -1:
                board_dict[(row, col)] = 'X'
            else:
                board_dict[(row, col)] = ''  # Empty cell
    return board_dict

def ai_player_moves(game_status, board_dict, size, turn_O):
    current_board_list = convert_board_to_list(board_dict, size)
    # print(current_board_list)
    # game_status = GameStatus(current_board_list, turn_O)
    _, move = minimax(game_status, 5, not turn_O)  # Assuming True for maximizing
    print(move)

    if move:
        # Convert the move to your board dictionary's format and execute
        game_status = game_status.get_new_state(move)
        # Convert new_board_state back to dict format if necessary
        board_dict = convert_list_to_dict(game_status.board_state)  # Implement conversion back to dict
        return board_dict, True, move, game_status  # Return updated board and switch turn back to player

    return board_dict, True, move, game_status


def player_moves(x,y):
    GameStatus.get_new_state(x,y)
    


if __name__ == '__main__':
    main()




def game_over():
    return GameStatus.is_terminal()




