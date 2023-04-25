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
        self.maxPly = 1
        self.staticEvalFunction = None

    # TODO: return a string containing your UW NETID(s)
    # For students in partnership: UWNETID + " " + UWNETID
    def nickname(self):
        # TODO: return a string representation of your UW netid(s)
        return "rayoh101"

    # Given a ply, it sets a maximum for how far an agent
    # should go down in the search tree. Count the chance nodes
    # as a ply too!
    def setMaxPly(self, maxply=2):
        # TODO: set the max ply
        self.maxPly = maxply

    # If not None, it update the internal static evaluation
    # function to be func
    def useSpecialStaticEval(self, func):
        # TODO: update your staticEval function appropriately
        self.staticEvalFunction = func

    # Given a state and a roll of dice, it returns the best move for
    # the state.whose_move
    # Keep in mind: a player can only pass if the player cannot move any checker with that role
    def move(self, state, die1, die2):
        # TODO: return a move for the current state and for the current player.
        # Hint: you can get the current player with state.whose_move
        return self.expectiminimax(state, self.maxPly, die1, die2)[1]

    # Hint: Look at game_engine/boardState.py for a board state properties you can use.
    def staticEval(self, state):
        # TODO: return a number for the given state

        listW=[]
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

    def get_all_moves_state_pair(self, curr_state, die1, die2):
        """Uses the mover to generate all legal (moves,state) pairs."""
        #generate move for curr_state
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

    def expectiminimax(self, state, plyLeft, die1, die2):
        currPlayer = state.whose_move

        # If plyLeft = 0, returns the static evaluation of the current state
        if plyLeft == 0:
            if self.staticEvalFunction != None:
                return (self.staticEvalFunction(state),"")
            else:
                return (self.staticEval(state),"")

        # bestMove is the current best move and its value
        bestMove = (0,"")

        #Max player's (white) turn
        if currPlayer == 0:
            bestMove = (-math.inf,"")
        #Min player's (red) turn
        else:
            bestMove = (math.inf,"")

        for next_move, next_state in self.get_all_moves_state_pair(state, die1, die2):
            newVal = 0

            for d1 in range(6):
                for d2 in range(6):
                    temp = self.expectiminimax(next_state, plyLeft-1, d1, d2)
                    newVal += temp[0] / 36

            # Update best move if a better move is found
            if (currPlayer == 0) and newVal > bestMove[0]:
                bestMove = (newVal, next_move)

            elif (currPlayer ==1) and newVal < bestMove[0]:
                bestMove = (newVal, next_move)

        return bestMove

