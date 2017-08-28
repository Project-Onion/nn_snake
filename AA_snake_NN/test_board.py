import numpy as np

# boards=numpy.load('./snake_json_files/trainingDataBoards.npy')

def drawBoard(boards, move, indexArray, num):
	row = 0
	head=(-1,-1)
	for i in boards[num]:
		row = row + 1
		column = 0
		for j in i:
			column = column + 1
			if j == 0:
				print(" "),
			else:
				print(j),
				if j==4:
					head=(column,50 - row)
		print("")
	print("-------------------------------------------------------------")
	print("head: " + str(head))
	print ("move: "+ str(move[num]))
	print ("index: " + str(indexArray[num]))


