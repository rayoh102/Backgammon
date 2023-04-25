'''
Name(s): Ray Oh
UW netid(s): rayoh101
'''

from game_engine import genmoves
import math

class BackgammonPlayer:
    def __init__(self):
        self.GenMoveInstance = genmoves.GenMoves()
        # feel free to create more instance variables as needed.
        self.AlphaBeta = False
        self.staticEvalFunction = None
        self.states = 0
        self.cutoffs = 0
        self.maxPly = 1
        self.die1 = 1
        self.die2 = 6

    # TODO: return a string containing your UW NETID(s)
    # For students in partnership: UWNETID + " " + UWNETID
    def nickname(self):
        # TODO: return a string representation of your UW netid(s)
        return "rayoh101"

    # If prune==True, then your Move method should use Alpha-Beta Pruning
    # otherwise Minimax
    def useAlphaBetaPruning(self, prune=False):
        # TODO: use the prune flag to indiciate what search alg to use
        self.AlphaBeta = prune
        self.states = 0
        self.cutoffs = 0

    # Returns a tuple containing the number explored
    # states as well as the number of cutoffs.
    def statesAndCutoffsCounts(self):
        # TODO: return a tuple containig states and cutoff
        return (self.states, self.cutoffs)

    # Given a ply, it sets a maximum for how far an agent
    # should go down in the search tree. maxply=2 indicates that
    # our search level will go two level deep.
    def setMaxPly(self, maxply=2):
        # TODO: set the max ply
        self.maxPly = maxply

    # If not None, it update the internal static evaluation
    # function to be func
    def useSpecialStaticEval(self, func):
        # TODO: update your staticEval function appropriately
        self.staticEvalFunction = func

    # Given a state and a roll of dice, it returns the best move for
    # the state.whose_move.
    # Keep in mind: a player can only pass if the player cannot move any checker with that role
    def move(self, state, die1=1, die2=6):
        # TODO: return a move for the current state and for the current player.
        # Hint: you can get the current player with state.whose_move
        if self.AlphaBeta:
            return self.alphaBetaPrune(state, 2, -10000000, 10000000, die1, die2)[1]
        else:
            return self.minimax(state, 2, die1, die2)[1]

    # The function takes a board state state as input and returns an evaluation score for the state
    # Hint: Look at game_engine/boardState.py for a board state properties you can use.
    def staticEval(self, state):
        # TODO: return a number for the given state

        listW =[]
        listR=[]

        for i in range(len(state.pointLists)):
            countW = 0
            countR = 0
            homeCountW=0
            homeCountR=0

            for j in range(len(state.pointLists[i])):
                if state.pointLists[i][j]==0:
                    countW += 1
                    if i<=5 and i>=0:
                        homeCountW += 1
                elif state.pointLists[i][j]==1:
                    countR += 1
                    if i>=18 and i<=23:
                        homeCountR+=1

            listW.append(countW)
            listR.append(countR)

        pipCountWhite = 0
        pipCountRed = 0

        for i in range(len(listW)):
            pipCountWhite += listW[i] * (len(listW) -i)

        for i in range(len(listR)):
            pipCountRed += listR[i] * (i+1)

        # Caclulate Evaluation Score
        evalScore = (pipCountRed + 25*state.bar.count(1) + homeCountW + 25*len(state.white_off))
        - (pipCountWhite + 25*state.bar.count(0) + homeCountR + 25*len(state.red_off))

        return evalScore

    def minimax(self, state, plyLeft, die1, die2):
        if plyLeft == 0:
            self.states += 1
            if self.staticEvalFunction != None:
                return (self.staticEvalFunction(state),"")
            else:
                return (self.staticEval(state),"")

        # "bestMove" stores current best move and its value found
        bestMove = (0,"")

        currPlayer = state.whose_move

        #Max player's (white) turn
        if currPlayer == 0:
            bestMove = (-math.inf,"")
        #Min player's (red) turn
        else:
            bestMove = (math.inf,"")

        # Iterate through all possible moves and call "minimax" recursively
        for next_move, next_state in self.get_all_moves_state_pair(state, die1, die2):
            # Resulting value of recursive call is stored in newMove
            newMove = self.minimax(next_state, plyLeft-1, die1, die2)

            # If Max player's turn and newMove's value is higher than current bestMove's value, update bestmove
            if (currPlayer == 0) and newMove[0] > bestMove[0]:
                bestMove = (newMove[0], next_move)

            # If Min player's turn & newMove's value is less than current bestMove's value, update bestmove
            elif (currPlayer ==1) and newMove[0] < bestMove[0]:
                bestMove = (newMove[0], next_move)

        return bestMove

    def alphaBetaPrune(self, state, plyLeft, alpha, beta, die1, die2):
        if plyLeft == 0:
            self.states += 1
            if self.staticEvalFunction != None:
                return (self.staticEvalFunction(state),"")
            else:
                return (self.staticEval(state),"")

        # "bestMove" stores current best move and its value found
        bestMove = (0,"")

        currPlayer = state.whose_move

        #Max player's (white) turn
        if currPlayer == 0:
            bestMove = (-math.inf,"")

            for next_move, next_state in self.get_all_moves_state_pair(state, die1, die2):
                # Calls the alphabetaprune recursively with the next state and updates the alpha and beta values
                newVal = self.alphaBetaPrune(next_state, plyLeft-1, alpha, beta, die1, die2)

                # Update bestmove
                if newVal[0] > bestMove[0]:
                    bestMove = (newVal[0], next_move)

                # Update alpha value and check for beta cutoff
                alpha = max(alpha, bestMove[0])

                if beta <= alpha:
                    self.cutoffs += 1
                    break

            return bestMove

        #Min player's (red) turn
        else:
            bestMove = (math.inf,"")

            for next_move, next_state in self.get_all_moves_state_pair(state, die1, die2):
                newVal = self.alphaBetaPrune(next_state, plyLeft-1, alpha, beta, die1, die2)

                if newVal[0] < bestMove[0]:
                    bestMove = (newVal[0], next_move)

                beta = min(beta, bestMove[0])
                if beta <= alpha:
                    self.cutoffs += 1
                    break

            return bestMove

    #This function takes in a current state of the board (curr_state) and the values of two dice
    # (die1 and die2) and returns a list of all possible moves and their resulting states
    def get_all_moves_state_pair(self, curr_state, die1, die2):
        moveGen = self.GenMoveInstance.gen_moves(curr_state, curr_state.whose_move, die1, die2)
        listOfMoves = []
        finished = False
        legalMoves = False

        # Generate legal moves
        while not finished:
            try:
                move = next(moveGen)
                if move[0] != 'p':
                    legalMoves = True
                    listOfMoves .append(move)

            # Exception raised when no more moves left
            except StopIteration as e:
                finished = True

        # If no legal moves found, then pass
        if not legalMoves:
            listOfMoves.append(('p', curr_state))
        return listOfMoves
