import sys
import pygame
import numpy as np
import random
import time
nodes_explored=0
max_depth_reached=0
pygame.init()

WHITE = (255, 255, 255)
RED= (255, 0, 0)
GRAY= (200, 200, 200)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

width=300
height=300
line_width=5
board_rows=3
board_cols=3
square_size=width//board_cols
circle_radius=square_size//3
circle_width=15
cross_width=25

screen=pygame.display.set_mode((width, height))
pygame.display.set_caption('Tic Tac Toe AI')
screen.fill(BLACK)

board=np.zeros((board_rows, board_cols))

def draw_lines(colour=WHITE):
    for i in range(1, board_rows):
        # Horizontal lines
        pygame.draw.line(screen, colour, (0, i * square_size), (width, i * square_size), line_width)
        # Vertical lines
        pygame.draw.line(screen, colour, (i * square_size, 0), (i * square_size, height), line_width)
def draw_figures(colour=WHITE):
    for row in range(board_rows):
        for col in range(board_cols):
            if board[row][col] == 1:
                pygame.draw.circle(screen, GREEN, (int(col * square_size + square_size//2), int(row * square_size + square_size//2)), circle_radius, circle_width)
            elif board[row][col] == 2:
                # Removed start_pos=, end_pos=, and width=
                pygame.draw.line(screen, RED, (col * square_size + cross_width, row * square_size + cross_width), (col * square_size + square_size - cross_width, row * square_size + square_size - cross_width), cross_width)
                pygame.draw.line(screen, RED, (col * square_size + cross_width, row * square_size + square_size - cross_width), (col * square_size + square_size - cross_width, row * square_size + cross_width), cross_width)
def available_square(row, col):
    return board[row][col] == 0
def mark_square(row, col, player):
    board[row][col] = player
def unmark_square(row, col):
    board[row][col] = 0

def is_board_full(check_board=board):
    for row in range(board_rows):
        for col in range(board_cols):
            if check_board[row][col] == 0:
                return False
    return True
def check_win(player, check_board=board):
    for col in range(board_cols):
        if check_board[0][col] == player and check_board[1][col] == player and check_board[2][col] == player:
            return True
    for row in range(board_rows):
        if check_board[row][0] == player and check_board[row][1] == player and check_board[row][2] == player:
            return True
    if check_board[0][0] == player and check_board[1][1] == player and check_board[2][2] == player:
        return True
    if check_board[0][2] == player and check_board[1][1] == player and check_board[2][0] == player:
        return True
    return False

def minimax(minimax_board, depth, is_maximizing):
    global nodes_explored, max_depth_reached
    nodes_explored += 1
    max_depth_reached = max(max_depth_reached, depth)

    if check_win(2, minimax_board): return float('inf')
    if check_win(1, minimax_board): return float('-inf')
    if is_board_full(minimax_board): return 0

    if is_maximizing:
        best_score = float('-inf')
        for row in range(board_rows):
            for col in range(board_cols):
                if available_square(row, col):
                    
                    if depth <= 1:
                        print("  " * depth + f"-> AI tests ({row}, {col})")
                
                        
                    mark_square(row, col, 2)
                    eval = minimax(minimax_board, depth + 1, False)
                    unmark_square(row, col)
                    best_score = max(best_score, eval)
        return best_score
    else:
        min_eval = float('inf')
        for row in range(board_rows):
            for col in range(board_cols):
                if available_square(row, col):
                    if depth <= 1:
                        print("  " * depth + f"-> Player tests ({row}, {col})")
                    mark_square(row, col, 1)
                    eval = minimax(minimax_board, depth + 1, True)
                    unmark_square(row, col)
                    min_eval = min(min_eval, eval)
        return min_eval
    
def  best_move():  
    global max_depth_reached, nodes_explored
    max_depth_reached=0
    nodes_explored=0

    start_time=time.time()
    best_score = float('-inf')
    move = (-1, -1)
    for row in range(board_rows):
        for col in range(board_cols):
            if available_square(row, col):
                mark_square(row, col, 2)
                score = minimax(board, 0, False)
                unmark_square(row, col)
                if score > best_score:
                    best_score = score
                    move = (row, col)
    end_time=time.time()
    time_taken=end_time-start_time
    print("-" * 60)
    print(f"Minimax: Nodes explored = {nodes_explored}, Max depth reached = {max_depth_reached}, Time taken = {time_taken:.4f} seconds")
    print("-" * 60)
    if move != (-1, -1):
        mark_square(move[0], move[1], 2)
        return True
    return False
def random_move():
    start_time=time.time()
    empty_squares = []
    for row in range(board_rows):
        for col in range(board_cols):
            if available_square(row, col):
                empty_squares.append((row, col))
                
    if empty_squares:
        move = random.choice(empty_squares)
        mark_square(move[0], move[1], 2)
        time_taken=time.time()-start_time
        print(f"Random Move: Time taken = {time_taken:.4f} seconds | Nodes explored = 1 | Max depth reached = 1")
        return True
    return False
def make_ai_move(difficulty):
    chance = random.random() 
    
    if difficulty == 'easy':
        if chance <= 0.3:
            return best_move()
        else:
            return random_move()
            
    elif difficulty == 'medium':
        if chance <= 0.6:
            return best_move()
        else:
            return random_move()
            
    elif difficulty == 'impossible':
        return best_move()

def restart_game():
    screen.fill(BLACK)
    draw_lines()
    for row in range(board_rows):
        for col in range(board_cols):
            board[row][col] = 0

def main():
    draw_lines()
    player_turn = True
    game_over = False

    current_difficulty = 'impossible'  # Change to 'easy', 'medium', or 'impossible' as needed

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over and player_turn:
                mouseX = event.pos[0]
                mouseY = event.pos[1]
                clicked_row = mouseY // square_size
                clicked_col = mouseX // square_size
                if available_square(clicked_row, clicked_col):
                    mark_square(clicked_row, clicked_col, 1)
                    draw_figures()
                    if check_win(1):
                        print("Player wins!")
                        game_over = True
                    elif is_board_full():
                        print("It's a tie!")
                        game_over = True
                    else:
                        player_turn = False

        if not player_turn and not game_over:
            if make_ai_move(current_difficulty):
                draw_figures()
                if check_win(2):
                    print("AI wins!")
                    game_over = True
                elif is_board_full():
                    print("It's a tie!")
                    game_over = True
            player_turn = True
        pygame.display.update()

        if game_over:
            pygame.time.wait(1000)
            restart_game()
            player_turn = True
            game_over = False   

main()