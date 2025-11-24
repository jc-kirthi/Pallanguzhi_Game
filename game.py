# This class contains algorithms of all agent techniques
# Modified version to allow Player 0 = Human and Player 1 = AI

import board
import random

# This is the global variable for defining depth of the tree
depth = 0
stack = []

class game:

   """
        Initialize class variables with pit counts and number of pieces in each board
        Also initialize current score with 0 for each player and current player turn
   """
   def __init__(self, no_of_pits, pieces):
       self.current_game_board = board.board(no_of_pits, pieces)
       self.current_score = [0,0]
       self.current_player = 0

   '''
      This function switch the current player
   '''
   def changePlayerTurn(self):
      self.current_player = (self.current_player + 1) % 2
      
   '''
      This function update the current scores for the current player
   '''
   def updateScore(self, score):
      self.current_score[self.current_player] += score
      
   '''
      This function returns True if game is NOT over
      or it will return False otherwise
   '''
   def checkGameStatus(self):
      return not self.current_game_board.isEmptyBoard()

   '''
      Human move input
   '''
   def humanMove(self):

      print("\nYour Turn (Player 0)")
      valid_moves = self.current_game_board.getCurrentChoices(self.current_player)
      human_vals = [i+1 for i in valid_moves]

      print("Your available pits: ", human_vals)

      pit_choice = None
      while pit_choice not in human_vals:
         try:
            pit_choice = int(input("Choose pit (1–7): "))
            if pit_choice not in human_vals:
               print("Invalid choice, try again.")
         except:
            print("Invalid input. Enter a number.")

      pit = pit_choice - 1
      self.printMove(pit)

      score = self.current_game_board.move(pit, False, self.current_score)
      self.updateScore(score)
      self.changePlayerTurn()
      return pit

   '''
      This function prints move of the current player in the console
   '''
   def printMove(self, value):
      if value > 6:
         value = value - 6
      else:
         value = value + 1
      print("Player {0} chose pit {1}".format(self.current_player, value))
      
   '''
      This is the Naive Agent
   '''
   def naiveAgent(self):         
      pit = random.choice(self.current_game_board.getCurrentChoices(self.current_player))
      self.printMove(pit)
      score = self.current_game_board.move(pit, False, self.current_score)
      self.updateScore(score)
      self.changePlayerTurn()
      return pit

   '''
      Greedy Agent
   '''
   def greedyAgent(self):   
      max_score = float("-inf")
      max_move = 0
      moves = self.current_game_board.getCurrentChoices(self.current_player)

      for move_option in moves:
         new_board = self.current_game_board.clone()
         new_board_score = new_board.move(move_option, True, self.current_score)
         if new_board_score > max_score:
            max_score = new_board_score
            max_move = move_option

      pit = max_move
      self.printMove(pit)
      score = self.current_game_board.move(pit, False, self.current_score)
      self.updateScore(score)
      self.changePlayerTurn()
      return pit

   '''
      Minimax implementation helpers
   '''
   def miniMaxValue(self, board_inst, limit, player, checker=0):
      global depth
      depth += 1

      if board_inst.isEmptyBoard():
         return 0

      max_score = float("-inf")
      max_move = 0
      moves = board_inst.getCurrentChoices(player)

      if ((depth == (limit - 1)) or ((depth == limit) and (limit == 1))):
         for move_option in moves:
            new_board = board_inst.clone()
            new_board_score = new_board.move(move_option, True, self.current_score)
            if new_board_score > max_score:
               max_score = new_board_score
               max_move = move_option

      else:
         max_ratio = float("-inf")
         for move_option in moves:
            new_board = board_inst.clone()
            new_player = (player + 1) % 2
            score = new_board.move(move_option, True, self.current_score)
            opponent_score = self.miniMaxValue(new_board, limit, new_player, depth)

            if opponent_score != 0:
               if float(score/opponent_score) > max_ratio:
                  max_score = score
                  max_ratio = float(score/opponent_score)
                  max_move = move_option
            else:
               max_score = score
               max_move = move_option

      if checker == 1:
         return max_move
      else:
         return max_score

   '''
      MinMax agent wrapper
   '''
   def minMaxAgent(self, limit):
      global depth
      pit = self.miniMaxValue(self.current_game_board, limit, self.current_player, 1)
      depth -= 1

      self.printMove(pit)
      score = self.current_game_board.move(pit, False, self.current_score)
      self.updateScore(score)
      self.changePlayerTurn()
      return pit

   '''
      Alpha Beta
   '''
   def GetAlphaBetaScore(self, board_inst, limit, player, alpha, beta, checker=0):
      global depth
      depth += 1

      if board_inst.isEmptyBoard():
         return 0

      max_score = float("-inf")
      max_move = 0
      moves = board_inst.getCurrentChoices(player)

      if ((depth == (limit - 1)) or ((depth == limit) and (limit == 1))):
         for move_option in moves:
            new_board = board_inst.clone()
            new_board_score = new_board.move(move_option, True, self.current_score)
            if new_board_score > max_score:
               max_score = new_board_score
               max_move = move_option

      else:
         max_ratio = float("-inf")
         for move_option in moves:
            new_board = board_inst.clone()
            new_player = (player + 1) % 2
            score = new_board.move(move_option, True, self.current_score)

            if score <= alpha:
               return score
            if score >= beta:
               return score

            opponent_score = self.GetAlphaBetaScore(new_board, limit, new_player,
                                                    alpha + score, beta + score)

            if opponent_score != 0:
               if float(score/opponent_score) > max_ratio:
                  max_score = score
                  max_ratio = float(score/opponent_score)
                  max_move = move_option
            else:
               max_score = score
               max_move = move_option

      if checker == 1:
         return max_move
      else:
         return max_score         

   def AlphaBetaPlay(self, limit):
      global depth
      alpha = -float('inf')
      beta = float('inf')

      pit = self.GetAlphaBetaScore(self.current_game_board, limit,
                                   self.current_player, alpha, beta, 1)

      depth -= 1

      self.printMove(pit)
      score = self.current_game_board.move(pit, False, self.current_score)
      self.updateScore(score)
      self.changePlayerTurn()
      return pit

   '''
      Reinforcement Learning agent (existing)
   '''
   def addtostack(self,x,y,z):
      global stack
      stack.append([x,y,z])

   def rlagent(self, board_state):
      global stack
      moves = self.current_game_board.getCurrentChoices(self.current_player)
      pit = random.choice(moves)

      possibilities = []
      for i in stack:
         if i[0] == tuple(board_state):
            possibilities.append(i)

      for poss in possibilities:
         if poss[2] >= 0:
            for choice in moves:
               if poss[1] == choice:
                  poss[2] += 1
                  pit = poss[1]

      self.printMove(pit)
      score = self.current_game_board.move(pit, False, self.current_score)
      self.updateScore(score)
      self.changePlayerTurn()
      return pit

   '''
      GAME LOOP
   '''
   def Play(self):
      global stack

      # Load RL data
      try:
         file = open("data.txt","r")
         for line in file:
            stack.append(line)
      except:
         pass

      print("PLAYER 0 = HUMAN")
      print("Choose AI for PLAYER 1:")
      print("1 = Naive")
      print("2 = Greedy")
      print("3 = MinMax")
      print("4 = AlphaBeta")
      print("5 = Reinforcement Learning")

      player = [0,0]  # player[0] = human, player[1] = AI

      # Human is fixed
      player[0] = 0

      # Choose AI for P1
      while player[1] not in [1,2,3,4,5]:
         try:
            player[1] = int(input("Enter AI number for Player 1: "))
            if player[1] not in [1,2,3,4,5]:
               print("Please enter valid number.")
         except:
            print("Enter a valid number.")

      print("\n--- Initial Board ---")
      self.current_game_board.printBoard(self.current_score)

      # GAME LOOP
      while self.checkGameStatus():
         if self.current_player == 0:
            pit = self.humanMove()
            self.current_game_board.printBoard(self.current_score)

         else:
            if player[1] == 1:
               pit = self.naiveAgent()
            elif player[1] == 2:
               pit = self.greedyAgent()
            elif player[1] == 3:
               pit = self.minMaxAgent(2)
            elif player[1] == 4:
               pit = self.AlphaBetaPlay(2)
            elif player[1] == 5:
               pit = self.rlagent(self.current_game_board.board)

            self.current_game_board.printBoard(self.current_score)

      # Game over – assign remaining pieces
      self.current_game_board.getAllPiecesElements(self.current_score)

      self.printGame()

   '''
      Print final result
   '''
   def printGame(self):
      print("\n--- Final Board ---")
      self.current_game_board.printBoard(self.current_score)

      if self.current_score[0] > self.current_score[1]:
         print("\nPLAYER 0 (YOU) WON!")
      elif self.current_score[1] > self.current_score[0]:
         print("\nPLAYER 1 (AI) WON!")
      else:
         print("\nIT'S A DRAW!")

   def __main__(self):
      self.Play()


# Run game
if __name__ == "__main__":
    newgame = game(14, 5)
    newgame.__main__()
