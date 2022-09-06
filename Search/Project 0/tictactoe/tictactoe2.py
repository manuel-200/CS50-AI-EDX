import math
import random
import time
import pygame
import sys
import time
from typing import Match
X = "X"
O = "O"
EMPTY = None

class tictactoe():

    def __init__(self, initial=[[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]):
        """
        Initialize game board.
        Each game board has
            - `piles`: a list of how many elements remain in each pile
            - `player`: 0 or 1 to indicate which player's turn
            - `winner`: None, 0, or 1 to indicate who the winner is
        """
        self.board = initial.copy()
        self.player = X
        self.winner = None

    @classmethod
    def available_actions(cls, board):
        actions = set()
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY: 
                    actions.add((i,j))
        return actions

    @classmethod
    def other_player(cls, player):
        """
        Nim.other_player(player) returns the player that is not
        `player`. Assumes `player` is either 0 or 1.
        """
        return O if player == X else X

    def switch_player(self):
        """
        Switch the current player to the other player.
        """
        self.player = tictactoe.other_player(self.player)

    def move(self, action):
        
        # Check for errors
        if self.winner is not None:
            raise Exception("Game already won")

        # Update pile
        if self.board[action[0]][action[1]] != EMPTY:
            raise ValueError
        else:
            self.board[action[0]][action[1]] = self.player
        self.switch_player()

        # Check for a winner
        for i in self.board:
            if i[0] == i[1] and i[1]== i[2]:
                self.player=self.winner
        for j in range(3):
            if self.board[0][j] == self.board[1][j] and self.board[1][j]== self.board[2][j]:
                self.player=self.winner
            if self.board[0][0] == self.board[1][1] and self.board[1][1]== self.board[2][2]:
                self.player=self.winner
            elif self.board[0][2] == self.board[1][1] and self.board[1][1]== self.board[2][0]:
                self.player=self.winner
            
        if EMPTY in tuple(self.board):
            self.terminal=True
        else:
            self.terminal=False


class ticAI():

    def __init__(self, alpha=0.5, epsilon=0.1):
        """
        Initialize AI with an empty Q-learning dictionary,
        an alpha (learning) rate, and an epsilon rate.

        The Q-learning dictionary maps `(state, action)`
        pairs to a Q-value (a number).
         - `state` is a tuple of remaining piles, e.g. (1, 1, 4, 4)
         - `action` is a tuple `(i, j)` for an action
        """
        self.q = dict()
        self.alpha = alpha
        self.epsilon = epsilon

    def update(self, old_state, action, new_state, reward):
        """
        Update Q-learning model, given an old state, an action taken
        in that state, a new resulting state, and the reward received
        from taking that action.
        """
        old = self.get_q_value(old_state, action)
        best_future = self.best_future_reward(new_state)
        self.update_q_value(old_state, action, old, reward, best_future)

    def get_q_value(self, state, action):
        if (tuple(state),action) in self.q:
            return self.q[tuple(state),action]
        else:
            return 0

    def update_q_value(self, state, action, old_q, reward, future_rewards):
        self.q[tuple(state),action]= old_q + self.alpha*(reward+future_rewards-old_q)

    def best_future_reward(self, state):
        max=-5
        for i in self.q:
            if i[0] == tuple(state) and i[1] is not None:
                if max<self.q[i]:
                    max=self.q[i]
        if max!=5:
            return max
        else:
            return 0

    def choose_action(self, state, epsilon=True):
        actions = list(tictactoe.available_actions(state))
        ran=random.random()
        max=-1000
        act=tuple()
        estate=tuple(state)
        for i in actions:
            if (estate,i) in self.q:
                if max<self.q[estate,i]:
                    max=self.q[estate,i]
                    act=i
            else:
                if max<0:
                    max=0
                    act=i
        if epsilon==False:
            return act
        if ran>=self.epsilon and epsilon==True:
            return act
        elif ran<self.epsilon and epsilon==True:
            return random.choice(actions)

def train(n):
    """
    Train an AI by playing `n` games against itself.
    """

    player = ticAI()

    # Play n games
    for i in range(n):
        print(f"Playing training game {i + 1}")
        game = tictactoe()

        # Keep track of last move made by either player
        last = {
            X: {"state": None, "action": None},
            O: {"state": None, "action": None}
        }

        # Game loop
        while True:

            # Keep track of current state and action
            state = game.board.copy()
            action = player.choose_action(game.board)

            # Keep track of last state and action
            last[game.player]["state"] = state
            last[game.player]["action"] = action

            # Make move
            game.move(action)
            new_state = game.board.copy()

            # When game is over, update Q values with rewards
            if game.winner is not None:
                player.update(state, action, new_state, -1)
                player.update(
                    last[game.player]["state"],
                    last[game.player]["action"],
                    new_state,
                    1
                )
                break

            # If game is continuing, no rewards yet
            elif last[game.player]["state"] is not None or game.terminal==True:
                player.update(
                    last[game.player]["state"],
                    last[game.player]["action"],
                    new_state,
                    0
                )

    print("Done training")

    # Return the trained AI
    return player


def play(ai, human_player=None):
    """
    Play human game against the AI.
    `human_player` can be set to 0 or 1 to specify whether
    human player moves first or second.
    """

    # If no player order set, choose human's order randomly
    if human_player is None:
        human_player = random.randint(0, 1)

    # Create new game
    game = tictactoe()

    import tictactoe as ttt

    pygame.init()
    size = width, height = 600, 400

    # Colors
    black = (0, 0, 0)
    white = (255, 255, 255)

    screen = pygame.display.set_mode(size)

    mediumFont = pygame.font.Font("OpenSans-Regular.ttf", 28)
    largeFont = pygame.font.Font("OpenSans-Regular.ttf", 40)
    moveFont = pygame.font.Font("OpenSans-Regular.ttf", 60)

    user = None
    board = ttt.initial_state()
    ai_turn = False

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill(black)

        # Let user choose a player.
        if user is None:

            # Draw title
            title = largeFont.render("Play Tic-Tac-Toe", True, white)
            titleRect = title.get_rect()
            titleRect.center = ((width / 2), 50)
            screen.blit(title, titleRect)

            # Draw buttons
            playXButton = pygame.Rect((width / 8), (height / 2), width / 4, 50)
            playX = mediumFont.render("Play as X", True, black)
            playXRect = playX.get_rect()
            playXRect.center = playXButton.center
            pygame.draw.rect(screen, white, playXButton)
            screen.blit(playX, playXRect)

            playOButton = pygame.Rect(5 * (width / 8), (height / 2), width / 4, 50)
            playO = mediumFont.render("Play as O", True, black)
            playORect = playO.get_rect()
            playORect.center = playOButton.center
            pygame.draw.rect(screen, white, playOButton)
            screen.blit(playO, playORect)

            # Check if button is clicked
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if playXButton.collidepoint(mouse):
                    time.sleep(0.2)
                    user = ttt.X
                elif playOButton.collidepoint(mouse):
                    time.sleep(0.2)
                    user = ttt.O

        else:

            # Draw game board
            tile_size = 80
            tile_origin = (width / 2 - (1.5 * tile_size),
                        height / 2 - (1.5 * tile_size))
            tiles = []
            for i in range(3):
                row = []
                for j in range(3):
                    rect = pygame.Rect(
                        tile_origin[0] + j * tile_size,
                        tile_origin[1] + i * tile_size,
                        tile_size, tile_size
                    )
                    pygame.draw.rect(screen, white, rect, 3)

                    if board[i][j] != ttt.EMPTY:
                        move = moveFont.render(board[i][j], True, white)
                        moveRect = move.get_rect()
                        moveRect.center = rect.center
                        screen.blit(move, moveRect)
                    row.append(rect)
                tiles.append(row)

            game_over = ttt.terminal(board)
            player = ttt.player(board)

            # Show title
            if game_over:
                winner = ttt.winner(board)
                if winner is None:
                    title = f"Game Over: Tie."
                else:
                    title = f"Game Over: {winner} wins."
            elif user == player:
                title = f"Play as {user}"
            else:
                title = f"Computer thinking..."
            title = largeFont.render(title, True, white)
            titleRect = title.get_rect()
            titleRect.center = ((width / 2), 30)
            screen.blit(title, titleRect)

            # Check for AI move
            if user != player and not game_over:
                if ai_turn:
                    time.sleep(0.5)
                    move = ttt.minimax(board)
                    board = ttt.result(board, move)
                    ai_turn = False
                else:
                    ai_turn = True

            # Check for a user move
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1 and user == player and not game_over:
                mouse = pygame.mouse.get_pos()
                for i in range(3):
                    for j in range(3):
                        if (board[i][j] == ttt.EMPTY and tiles[i][j].collidepoint(mouse)):
                            board = ttt.result(board, (i, j))

            if game_over:
                againButton = pygame.Rect(width / 3, height - 65, width / 3, 50)
                again = mediumFont.render("Play Again", True, black)
                againRect = again.get_rect()
                againRect.center = againButton.center
                pygame.draw.rect(screen, white, againButton)
                screen.blit(again, againRect)
                click, _, _ = pygame.mouse.get_pressed()
                if click == 1:
                    mouse = pygame.mouse.get_pos()
                    if againButton.collidepoint(mouse):
                        time.sleep(0.2)
                        user = None
                        board = ttt.initial_state()
                        ai_turn = False

            pygame.display.flip()
