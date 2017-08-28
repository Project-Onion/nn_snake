import json
import numpy as np

currGlobalIndex = 0
BOARD_WIDTH=50
BOARD_HEIGHT = 50
NUMOFFILES=10
trainMoves = []
testMoves = []
validMoves = []
allBoards = []
allMoves = []
# trainBoards = []
# testBoards = []
# validBoards = []

brushSuperApple = 6
brushNormalApple = 5
brushEnemyHead = 2
brushEnemyBody = 1
brushWinnerHead = 4
brushWinnerBody = brushEnemyBody

indexArray = []

def findWinner(snakes):
    max = 0
    maxIndex = 0
    for snakeNum in range(len(snakes)):
        if int(snakes[snakeNum][0]) > max:
            max=int(snakes[snakeNum][0])
            maxIndex = snakeNum
    return maxIndex

# def drawLine(start, end, isWinner, isInvisible, isHead):
def drawLine(start, end, isWinner, isHead):
    brush = brushEnemyBody
    if isWinner:
        brush = brushWinnerBody
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
            board[start[0]][start[1]] = brushWinnerHead
        else:
            board[start[0]][start[1]] = brushEnemyHead

def drawSnakes(snakes):
    winnerNum=findWinner(snakes)
    for snakeNum in range(len(snakes)):
        if snakes[snakeNum][3]=="invisible":
            if snakeNum!=findWinner(snakes):
                continue
            isInvisible=True
        else:
            isInvisible=False

        if winnerNum==snakeNum:
            isWinner=True
        else:
            isWinner=False

        for i in range(len(snakes[snakeNum])-6-1-2*isInvisible): #notice, first coordinate is hwere snake took apple
            if (i==0):
                isHead=True
            else:
                isHead=False
            # drawLine(snakes[snakeNum][6+i],snakes[snakeNum][6+i+1], isWinner, isHead)
            drawLine(snakes[snakeNum][6+2*isInvisible+i],snakes[snakeNum][6+2*isInvisible+i+1], isWinner, isHead)

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
    
    lastHead = tuple(map(int, lastSnakes[lastWinner][6+2*isLastInvisible].split(',')))
    currHead = tuple(map(int, currSnakes[lastWinner][6+2*isCurrInvisible].split(',')))

    newLastHead = (lastHead[1], BOARD_HEIGHT - 1 - lastHead[0])
    newCurrHead = (currHead[1], BOARD_HEIGHT - 1 - currHead[0])

    firstKink = tuple(map(int, lastSnakes[lastWinner][7 + 2 * isLastInvisible].split(',')))
    newfirstKink = (firstKink[1], BOARD_HEIGHT - 1 - firstKink[0])
    if (newLastHead[0] < newfirstKink[0]):  # dir=left
        if newLastHead[0] == newCurrHead[0]:    #is there no a x dimension turn
            if newLastHead[1] > newCurrHead[1]:  # moved left
                return 2
            else:  # moved right
                return 3
        else:   #moved straight (continue in current x dimension)
            return 1
    elif (newLastHead[0] > newfirstKink[0]):  # dir=right
        if newLastHead[0] == newCurrHead[0]:    #is there no a x dimension turn
            if newLastHead[1] > newCurrHead[1]:  # moved right
                return 3
            else:  # moved left
                return 2
        else:   #moved straight (continue in current x dimension)
            return 1

    elif (newLastHead[1] < newfirstKink[1]):  # dir=down
        if newLastHead[1] == newCurrHead[1]:    #is there no y dimension turn
            if newLastHead[0] > newCurrHead[0]:  # moved right
                return 3
            else:  # moved left
                return 2
        else:   #moved straight (continue in current y dimension)
            return 1
    else:                                      # dir=up
        if newLastHead[1] == newCurrHead[1]:    #is there no y dimension turn
            if newLastHead[0] > newCurrHead[0]:  # moved left
                return 2
            else:  # moved right
                return 3
        else:   #moved straight (continue in current y dimension)
            return 1


    # if newLastHead[0]==newCurrHead[0]:
    #     if newLastHead[1] > newCurrHead[1]:   #moved down
    #         return 1
    #     else:                           #moved up
    #         return 0
    # else:
    #     if newLastHead[0] > newCurrHead[0]:   #moved left
    #         return 2
    #     else:                           #moved right
    #         return 3

def sphere (winningSnake, board):
    if winningSnake[3]== "invisible":
        isInvisible=True
    else:
        isInvisible = False

    head = tuple(map(int, winningSnake[6 + 2*isInvisible].split(',')))
    newHead = (head[1],BOARD_HEIGHT - 1 - head[0])

    if (newHead[1]<(BOARD_HEIGHT+1)/2):
        board = np.roll(board,(newHead[1]+2+(BOARD_HEIGHT+1)/2),axis=0)
    elif (newHead[1]>(BOARD_HEIGHT+1)/2):
        board = np.roll(board, (newHead[1]-(BOARD_HEIGHT+1)/2), axis=0)

    if (newHead[0]<(BOARD_WIDTH+1)/2):
        board = np.roll(board,((BOARD_WIDTH+1)/2-newHead[0]),axis=1)
    elif (newHead[0]>(BOARD_WIDTH+1)/2):
        board = np.roll(board, (BOARD_WIDTH-newHead[0]+2+(BOARD_WIDTH+1)/2), axis=1)

    firstKink = tuple(map(int, winningSnake[7 + 2*isInvisible].split(',')))
    newfirstKink = (firstKink[1], BOARD_HEIGHT - 1 - firstKink[0])
    if (newHead[0] < newfirstKink[0]): #dir=left
        board = np.rot90(board,3)
        board = np.roll(board, -1, axis=1)
        board = np.roll(board, -3, axis=0)
    elif (newHead[0] > newfirstKink[0]): #dir=right
        board =  np.rot90(board, 1)
        board = np.roll(board, -2, axis=0)
    elif (newHead[1] < newfirstKink [1]): #dir=down
        board = np.rot90(board, 2)
        board = np.roll(board, -3, axis=0)
    else:                               #dir=up
        board = np.roll(board, -1, axis=1)
        board = np.roll(board, -2, axis=0)

    return board

if __name__ == "__main__":
    dataType = 0
    for fileNumber in range(0,NUMOFFILES):

        #if fileNumber<6:
        #    continue

        with open('./snake_json_files/'+ str(fileNumber) + '.json') as data_file:
            data = json.load(data_file)

        reliantOnFlag = False
        for currState in range(0,len(data["states"])):
            if data["states"][currState]["state"].split('\n')[0].split(' ')[0]=="Game":
                continue

            insertStateFlag = True  # fuckedUpFlag
            if ((currState == (len(data["states"])-1)) or ((data["states"][currState]["globalIndex"]+1) != data["states"][currState+1]["globalIndex"])):
                insertStateFlag = False;


            if  int(data["states"][currState]["globalIndex"]) > currGlobalIndex:
                board = np.array( [[0 for i in range(BOARD_WIDTH)] for j in range(BOARD_HEIGHT)])
                currGlobalIndex = data["states"][currState]["globalIndex"]
                splitData = data["states"][currState]["state"].split('\n')

                superApple = tuple(map(int, splitData[0].split(' ')))
                if superApple[0] != -1:
                    board[superApple[0]][superApple[1]]=brushSuperApple
                normalApple = tuple(map(int, splitData[1].split(' ')))
                board[normalApple[0]][normalApple[1]] = brushNormalApple

                snakes = [tuple(splitData[i].split(' ')) for i in range (2,6)]
		
                if (snakes[findWinner(snakes)][3]=='dead'):
                    if reliantOnFlag:
                        del allBoards[-1]
                        del indexArray[-1]
                    reliantOnFlag = False
                    continue


                drawSnakes(snakes)

                # if dataType==0:
                #     if reliantOnFlag: #currState != 0:
                #         testMoves.append(findMove(lastSnakes,snakes, lastWinner))
                #     if insertStateFlag:
                #         board = np.pad(board, 1, 'constant', constant_values=(brushEnemyBody))  # add border to board for sphering
                #         #board = sphere(snakes[findWinner(snakes)],board)
                #         trainBoards.append(board)
                #         reliantOnFlag = True
                #     else:
                #         reliantOnFlag = False
                #     dataType=1
                # elif dataType== 1:
                #     if reliantOnFlag: #currState != 0:
                #         trainMoves.append(findMove(lastSnakes,snakes, lastWinner))
                #     if insertStateFlag:
                #         board = np.pad(board, 1, 'constant', constant_values=(brushEnemyBody))  # add border to board for sphering
                #         # board = sphere(snakes[findWinner(snakes)],board)
                #         validBoards.append(board)
                #         reliantOnFlag = True
                #     else:
                #         reliantOnFlag = False
                #     dataType=2
                # elif dataType== 2:
                #     if reliantOnFlag: #currState != 0:
                #         validMoves.append(findMove(lastSnakes,snakes, lastWinner))
                #     if insertStateFlag:
                #         board = np.pad(board, 1, 'constant', constant_values=(brushEnemyBody))  # add border to board for sphering
                #         # board = sphere(snakes[findWinner(snakes)],board)
                #         testBoards.append(board)
                #         reliantOnFlag = True
                #     else:
                #         reliantOnFlag = False
                #     dataType=0

                # if currState != 0:
                #     allMoves.append(findMove(lastSnakes,snakes, lastWinner))
                # board = np.pad(board, 1, 'constant',constant_values=(brushEnemyBody))  # add border to board for sphering
                # # board = sphere(snakes[findWinner(snakes)], board)
                # allBoards.append(board)

                if reliantOnFlag:  # currState != 0:
                    allMoves.append(findMove(lastSnakes,snakes, lastWinner))
                if insertStateFlag:
                    board = np.pad(board, 1, 'constant', constant_values=(brushEnemyBody))  # add border to board for sphering
                    board = sphere(snakes[findWinner(snakes)],board)
                    allBoards.append(board)
                    reliantOnFlag = True
                    indexArray.append((fileNumber,currGlobalIndex))
                else:
                    reliantOnFlag = False

                    # board = board.transpose()
                    # allBoards.append(board)
                    # if currState != 0:
                    #     allMoves.append(findMove(lastSnakes,snakes, lastWinner))

                lastSnakes=snakes
                lastWinner = findWinner(snakes)

    numpyAllBoard = np.array(allBoards)
    # np.save('./snake_json_files/'+ str(fileNumber) + '_parsed.npy',board,True,False)
    np.save('./snake_json_files/allDataBoards', numpyAllBoard)

    numpyAllMoves = np.array(allMoves)
    # np.save('./snake_json_files/'+ str(fileNumber) + '_parsed.npy',board,True,False)
    np.save('./snake_json_files/allDataMoves', numpyAllMoves)

    numpyIndexArray = np.array(indexArray)
    # np.save('./snake_json_files/'+ str(fileNumber) + '_parsed.npy',board,True,False)
    np.save('./snake_json_files/indexArray', numpyIndexArray)


    # numpyTrainBoard = np.array(trainBoards)
    # # np.save('./snake_json_files/'+ str(fileNumber) + '_parsed.npy',board,True,False)
    # np.save('./snake_json_files/trainingDataBoards', numpyTrainBoard)
    #
    # numpyValidBoard = np.array(validBoards)
    # # np.save('./snake_json_files/'+ str(fileNumber) + '_parsed.npy',board,True,False)
    # np.save('./snake_json_files/validationDataBoards', numpyValidBoard)
    #
    # numpyTestBoard = np.array(testBoards)
    # # np.save('./snake_json_files/'+ str(fileNumber) + '_parsed.npy',board,True,False)
    # np.save('./snake_json_files/testDataBoards', numpyTestBoard)
    #
    # numpyTrainMoves = np.array(trainMoves)
    # # np.save('./snake_json_files/'+ str(fileNumber) + '_parsed.npy',board,True,False)
    # np.save('./snake_json_files/trainingDataMoves', numpyTrainMoves)
    #
    # numpyValidMoves = np.array(validMoves)
    # # np.save('./snake_json_files/'+ str(fileNumber) + '_parsed.npy',board,True,False)
    # np.save('./snake_json_files/validationDataMoves', numpyValidMoves)
    #
    # numpyTestMoves = np.array(testMoves)
    # # np.save('./snake_json_files/'+ str(fileNumber) + '_parsed.npy',board,True,False)
    # np.save('./snake_json_files/testDataMoves', numpyTestMoves)


