import json
import numpy as np

currGlobalIndex = 0
BOARD_WIDTH=50
BOARD_HEIGHT = 50
NUMOFFILES=10
trainMoves = []
testMoves = []
validMoves = []
# allBoards = []
trainBoards = []
testBoards = []
validBoards = []
def findWinner(snakes):
    max = 0;
    maxIndex = 0;
    for snakeNum in range(len(snakes)):
        if int(snakes[snakeNum][0]) > max:
            max=int(snakes[snakeNum][0])
            maxIndex = snakeNum
    return maxIndex

#def drawLine(start, end, isWinner, isInvisible, isHead):
def drawLine(start, end, isWinner, isHead):
    brush = 1
    if isWinner:
        brush = 2
#    elif isInvisible:
#        brush=0

    start = tuple(map(int, start.split(',')))
    end = tuple(map(int, end.split(',')))
    if (start[0]==end[0]):
        if (start[1]<end[1]):
            for i in range(start[1],end[1]+1):
                board[start[0]][i]=brush
        else:
            for i in range(end[1],start[1]+1):
                board[start[0]][i]=brush
    else:
        if (start[0]<end[0]):
            for i in range(start[0],end[0]+1):
                board[i][start[1]]=brush
        else:
            for i in range(end[0],start[0]+1):
                board[i][start[1]]=brush
    if (isHead):
        if (isWinner):
            board[start[0]][start[1]]=4
        else:
            board[start[0]][start[1]] = 3

def drawSnakes(snakes):
    winnerNum=findWinner(snakes)
    for snakeNum in range(len(snakes)):
        if snakes[snakeNum][3]=="invisible":
            break;
#            isInvisible=True
#        else:
#            isInvisible=False

        if winnerNum==snakeNum:
            isWinner=True
        else:
            isWinner=False

        for i in range(len(snakes[snakeNum])-6-1):#-2*isInvisible -1):
            if (i==0):
                isHead=True
            else:
                isHead=False
            drawLine(snakes[snakeNum][6+i],snakes[snakeNum][6+i+1], isWinner, isHead)
#            drawLine(snakes[snakeNum][6+2*isInvisible+i],snakes[snakeNum][6+2*isInvisible+i+1], isWinner, isInvisible, isHead)

def printBoard():
    for i in range(BOARD_WIDTH):
        for j in range(BOARD_HEIGHT):
            print (str(board[j][i]) + " "),
        print ("\n")

def findMove(lastSnakes, currSnakes, lastWinner):
    if lastSnakes[lastWinner][3]== "invisible":
        isLastInvisible=True
    else:
        isLastInvisible = False
    if currSnakes[lastWinner][3]== "invisible":
        isCurrInvisible=True
    else:
        isCurrInvisible = False
    
    lastHead = tuple(map(int, lastSnakes[lastWinner][6+isCurrInvisible].split(',')))
    currHead = tuple(map(int, currSnakes[lastWinner][6+isCurrInvisible].split(',')))

    if lastHead[0]==currHead[0]:
        if lastHead[1] > currHead[1]:   #moved down
            return 1
        else:                           #moved up
            return 0
    else:
        if lastHead[0] > currHead[0]:   #moved left
            return 2
        else:                           #moved right
            return 3

if __name__ == "__main__":
    for fileNumber in range(0,NUMOFFILES):
        with open('./snake_json_files/'+ str(fileNumber) + '.json') as data_file:
            data = json.load(data_file)

        for currState in range(0,len(data["states"])):
            if data["states"][currState]["globalIndex"] > currGlobalIndex:
                board = np.array( [[0 for i in range(BOARD_WIDTH)] for j in range(BOARD_HEIGHT)])
                currGlobalIndex = data["states"][currState]["globalIndex"]
                splitData = data["states"][currState]["state"].split('\n')

                superApple = tuple(map(int, splitData[0].split(' ')))
                if superApple[0] != -1:
                    board[superApple[0]][superApple[1]]=5
                normalApple = tuple(map(int, splitData[1].split(' ')))
                board[normalApple[0]][normalApple[1]] = 6

                snakes = [tuple(splitData[i].split(' ')) for i in range (2,6)]
		
		if (snakes[findWinner(snakes)][3]=='dead'):
			break;
                drawSnakes(snakes)

        if currGlobalIndex%3==0:
            trainBoards.append(board)
            if currState != 0:
                trainMoves.append(findMove(lastSnakes,snakes, lastWinner))
        elif currGlobalIndex % 3 == 1:
            validBoards.append(board)
            if currState != 0:
                validMoves.append(findMove(lastSnakes,snakes, lastWinner))
        elif currGlobalIndex % 3 == 2:
            testBoards.append(board)
            if currState != 0:
                testMoves.append(findMove(lastSnakes,snakes, lastWinner))
            # allBoards.append(board)
            # if currState != 0:
            #     moves.append(findMove(lastSnakes,snakes, lastWinner))
                # board = board.transpose()
                # allBoards.append(board)
                # if currState != 0:
                #     moves.append(findMove(lastSnakes,snakes, lastWinner))


                lastSnakes=snakes
                lastWinner = findWinner(snakes);

    numpyTrainBoard = np.array(trainBoards)
    # np.save('./snake_json_files/'+ str(fileNumber) + '_parsed.npy',board,True,False)
    np.save('./snake_json_files/trainingDataBoards', numpyTrainBoard)

    numpyValidBoard = np.array(validBoards)
    # np.save('./snake_json_files/'+ str(fileNumber) + '_parsed.npy',board,True,False)
    np.save('./snake_json_files/validationDataBoards', numpyValidBoard)

    numpyTestBoard = np.array(testBoards)
    # np.save('./snake_json_files/'+ str(fileNumber) + '_parsed.npy',board,True,False)
    np.save('./snake_json_files/testDataBoards', numpyTestBoard)

    numpyTrainMoves = np.array(moves)
    # np.save('./snake_json_files/'+ str(fileNumber) + '_parsed.npy',board,True,False)
    np.save('./snake_json_files/trainingDataMoves', numpyTrainMoves)

    numpyValidMoves = np.array(moves)
    # np.save('./snake_json_files/'+ str(fileNumber) + '_parsed.npy',board,True,False)
    np.save('./snake_json_files/validationDataMoves', numpyValidMoves)

    numpyTestMoves = np.array(moves)
    # np.save('./snake_json_files/'+ str(fileNumber) + '_parsed.npy',board,True,False)
    np.save('./snake_json_files/testDataMoves', numpyTestMoves)

1
