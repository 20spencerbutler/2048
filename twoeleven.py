import random, pygame, sys, math, copy, time
from pygame.locals import *
from myWriter import *

GRIDSIZE = 4
GAMERES = (600, 400)
COLORS = [
    (255, 220, 215),
    (255, 200, 190),
    (255, 185, 165),
    (255, 170, 150),
    (255, 150, 120),
    (255, 130, 100),
    (255, 110, 80),
    (255, 90, 60),
    (255, 70, 40),
    (255, 50, 20),
    (255, 30, 0),
    (230, 25, 0)
]
lastDirect = 0
score = 0
lastScore = 0
movedDirect = 0
lastBoard = []
TILESIZE = int(min(50,min((GAMERES[0] - 100) / GRIDSIZE, (GAMERES[1] - 100) / GRIDSIZE)))
#print(TILESIZE)
FPS = 60
FPSCLOCK = pygame.time.Clock()
ANIMTIME = 10
animticks = 0
moves = 0
board = []
part = []
empty = []
for i in range(GRIDSIZE): part.append([0, [-1, -1], True, True])
for i in range(GRIDSIZE): board.append(copy.deepcopy(part))



disp = pygame.display.set_mode(GAMERES)
pygame.display.set_caption('ey man')
# for i in board:
#     for j in i:
printer = writerMine()
# for x in range(1, 5):
#     for y in range(1, 10):
#         disp.blit(printer.write(x * y, 'hey man'), (x * 10, y * 10))

def updateEmpty():
    global empty
    empty = []
    for x in range(len(board)):
        for y in range(len(board[x])):
            if(board[x][y][0] == 0):
                empty.append((x, y))

def addTile():
    updateEmpty()
    firstRand = random.randint(0, 9)
    #print(len(empty))
    if(len(empty) == 0):
        return
    spot = empty[random.randint(0, len(empty) - 1)]
    board[spot[0]][spot[1]][0] = 2 - min(1, firstRand)

def newGame():
    global board
    board = []
    part = []
    empty = []
    for i in range(GRIDSIZE): part.append([0, [-1, -1], True, True])
    for i in range(GRIDSIZE): board.append(copy.deepcopy(part))
    addTile()
    addTile()

def findDest(x, y, direction):
    global moves
    #print(board[x][y])
    #print(board[x][y][2])
    board[x][y][2] = False
    #print(x, y, board[x][y][2], 'onself')
    #print(direction)
    ret = (-1, -1)
    if direction == 4:
        if(x == 0): ret = (-1, - 1)
        for i in range(x - 1, -1, -1):
            if(ret != (-1, -1)): break
            if not(board[i][y][0] == 0):
                if board[i][y][1] == [-1, -1]:
                    if(board[x][y][0] == board[i][y][0] and not board[i][y][2]):
                        ret = (i, y)
                        board[x][y][2] = True
                    else:
                        ret = (i + 1, y)
                else:
                    if(board[x][y][0] == board[i][y][0] and not board[i][y][2]):
                        ret = (board[i][y][1][0], y)
                        board[x][y][2] = True
                    else: ret = (board[i][y][1][0] + 1, y)
                    #print(ret)
                    #print(board[i][y][0] + 1, y)
                    #print(board[i][y][0])
                    #print(x, y,'t')
            if i == 0 and ret == (-1, -1): ret = (i, y)
    if direction == 3:
        if(x + 1 == len(board)): ret = (-1, - 1)
        for i in range(x + 1, len(board)):
            if(ret != (-1, -1)): break
            if not(board[i][y][0] == 0):
                if board[i][y][1] == [-1, -1]:
                    if(board[x][y][0] == board[i][y][0] and not board[i][y][2]):
                        ret = (i, y)
                        board[x][y][2] = True
                    else:
                        ret = (i - 1, y)
                else:
                    if(board[x][y][0] == board[i][y][0] and not board[i][y][2]):
                        ret = (board[i][y][1][0], y)
                        board[x][y][2] = True
                    else:ret = (board[i][y][1][0] - 1, y)
                    #print(x, y,'t')
            if i + 1 == len(board) and ret == (-1, -1): ret = (i, y)
    if direction == 1:
        if(y == 0): ret = (-1, - 1)
        for i in range(y - 1, -1, -1):
            if(ret != (-1, -1)): break
            if not(board[x][i][0] == 0):
                if board[x][i][1] == [-1, -1]:
                    #print(x, i, board[x][i][2])
                    if board[x][y][0] == board[x][i][0] and not board[x][i][2]:
                        ret = (x, i)
                        board[x][y][2] = True
                    else: ret = (x, i + 1)
                else:
                    if(board[x][y][0] == board[x][i][0] and not board[x][i][2]):
                        ret = (x, board[x][i][1][1])
                        board[x][y][2] = True
                    else: ret = (x, board[x][i][1][1] + 1)
                    #print(x, y,'t')
            if i == 0 and ret == (-1, -1): ret = (x, i)
    if direction == 2:
        if(y + 1 == len(board[x])): ret = (-1, - 1)
        for i in range(y + 1, len(board[x])):
            if(ret != (-1, -1)): break
            if not(board[x][i][0] == 0):
                if board[x][i][1] == [-1, -1] :
                    if(board[x][y][0] == board[x][i][0] and not board[x][i][2]):
                        ret = (x, i)
                        board[x][y][2] = True
                    else: ret = (x, i - 1)
                else:
                    if(board[x][y][0] == board[x][i][0] and not board[x][i][2]):
                        ret = (x, board[x][i][1][1])
                        board[x][y][2] = True
                    else: ret = (x, board[x][i][1][1] - 1)
                    #print(x, y,'t')
            if i + 1 == len(board[i]) and ret == (-1, -1): ret = (x, i)
    #ret = (-1, -1)
    if(ret == (x, y)): ret = (-1, -1)
    if(ret != (-1, -1)):
        moves += 1
    #print(x, y, ret)
    #print(x, y, board[x][y][2])
    return ret

def updateRend():
    global animticks
    global board
    global score
    if animticks > 0:
        print(animticks)
        print(board[0][0])
    if animticks == ANIMTIME and board[0][0][3]:
        print('neu', board[0][0])
        xbounds = range(len(board) - 1, -1, -1) if (lastDirect == 3) else range(len(board))
        ybounds = range(len(board[0]) - 1, -1, -1) if (lastDirect == 2) else range(len(board[0]))
        #print(xbounds, ybounds)
        for i in xbounds:
            for j in ybounds:
                if(board[i][j][1] != [-1, -1]):
                    #print(i, j)
                    #print(board[i][j][1][0])
                    #print(board[i][j][1][1])
                    #print(board[board[i][j][1][0]][board[i][j][1][1]][0])
                    if(board[board[i][j][1][0]][board[i][j][1][1]][0] == 0):
                        board[board[i][j][1][0]][board[i][j][1][1]][0] = board[i][j][0]
                    else:
                        board[board[i][j][1][0]][board[i][j][1][1]][0] = board[i][j][0] + 1
                        score = int(score + math.pow(2, board[board[i][j][1][0]][board[i][j][1][1]][0]))
                        #print('merge:', i, j, board[i][j][1])
                    board[board[i][j][1][0]][board[i][j][1][1]][1] = [-1, -1]
                    #print(i, j, board[i][j][1])
                    #print(board[board[i][j][1][0]][board[i][j][1][1]][0])
                    board[i][j] = [0, [-1, -1], False, True]
                    animticks = 0
        addTile()
    if animticks == ANIMTIME: animticks = 0
    if animticks > 0: animticks += 1
    pygame.draw.rect(disp, (100, 100, 100), (40, 40, TILESIZE * (len(board)) + 20, TILESIZE * (len(board[0])) + 20))
    for i in range(0, len(board)):
        for j in range(0, len(board[i])):
            pygame.draw.rect(disp, (125, 125, 125), ((TILESIZE) * i + 50, (TILESIZE) * j + 50, TILESIZE * .95, TILESIZE * .95))
    for i in range(0, len(board)):
        for j in range(0, len(board[i])):
            if board[i][j][0] != 0:
                #print(board[i][j][0])
                if (board[i][j][1] == [-1, -1]):
                    drawx = (TILESIZE) * i + 50
                elif (board[i][j][3]):
                    drawx = ((TILESIZE) * i + 50) + (TILESIZE * (board[i][j][1][0] - i) * (animticks / ANIMTIME))
                else:
                    print('hey', animticks)
                    drawx = (TILESIZE * board[i][j][1][0] + 50) + (TILESIZE * (i - board[i][j][1][0]) * (animticks / ANIMTIME))
                if (board[i][j][1] == [-1, -1]):
                    drawy = (TILESIZE) * j + 50
                elif (board[i][j][3]):
                    drawy = ((TILESIZE) * j + 50) + (TILESIZE * (board[i][j][1][1] - j) * (animticks / ANIMTIME))
                else:
                    drawy = (TILESIZE * board[i][j][1][1] + 50) + (TILESIZE * (j - board[i][j][1][1]) * (animticks / ANIMTIME))
                #print(board[i][j], drawx, drawy)
                #print(drawx, drawy)
                #print(i, j, board[i][j][1], drawx, drawy)
                pygame.draw.rect(disp, (COLORS[board[i][j][0]]), (drawx, drawy, TILESIZE * .95, TILESIZE * .95))
                disp.blit(printer.write(int(TILESIZE / math.sqrt(math.ceil((math.log(math.pow(2, board[i][j][0]), 10))))),
                                        str(math.trunc(math.pow(2, board[i][j][0])))),
                                        ((drawx + (.1 * TILESIZE)), (TILESIZE) * ( .2) + drawy))

    pygame.display.update()

def undo():
    global score, lastDirect, board, lastScore, lastBoard, animticks
    score = lastScore
    #print(lastBoard)
    board = copy.deepcopy(lastBoard)
    for i in range(len(board)):
        for j in range(len(board[i])):
            board[i][j][3] = False
    #print(board, 'undo')
    lastDirect = movedDirect
    animticks = 1
    animticker = 1
    while(animticks > 0):
        updateRend()
        animticker += 1
        print(animticks, 'in undo')
    for i in range(len(board)):
        for j in range(len(board[i])):
            board[i][j][3] = True


newGame()
updateRend()
while True:
    #global lastBoard
    #print(lastBoard)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit('ey')
        if event.type == MOUSEBUTTONDOWN:
            if 100 < event.pos[0] < 225 and 5 < event.pos[1] < 40:
                newGame()
            if 250 < event.pos[0] < 310 and 5 < event.pos[1] < 40:
                print('undo')
                undo()
        if event.type == KEYDOWN:
            #print(event.key)
            if (272 < event.key < 277):
                if(animticks > 0): animticks = ANIMTIME
                updateRend()
                moves = 0
                direct = event.key - 272
                lastDirect = direct
                if(direct == 2):
                    for i in range(0, len(board)):
                        for j in range(len(board[i]) - 1, -1, -1):
                            #print(i, j)
                            if board[i][j][0] != 0:
                                #print(board[i][j][1])
                                board[i][j][1] = list(findDest(i, j, direct))
                                #print(board[i][j][1])
                if(direct == 1 or 4):
                    for i in range(0, len(board)):
                        for j in range(0, len(board[i])):
                            if board[i][j][0] != 0:
                                #print(board[i][j][1])
                                board[i][j][1] = list(findDest(i, j, direct))
                                #print(board[i][j][1])
                if(direct == 3):
                    for i in range(len(board) -1, -1, -1):
                        for j in range(0, len(board[i])):
                            if board[i][j][0] != 0:
                                #print(board[i][j][1])
                                board[i][j][1] = list(findDest(i, j, direct))
                if(moves > 0):
                    animticks = 1
                    lastScore = score
                    lastBoard = copy.deepcopy(board)
                    #print(lastBoard)
                    movedDirect = direct
                                #print(board[i][j][1])
    FPSCLOCK.tick(FPS)
    updateRend()
    updateEmpty()
    pygame.draw.rect(disp, (0, 0, 0), (0, 0, GAMERES[0], 50))
    disp.blit(printer.write(48, str(score)), (30, 5))
    pygame.draw.rect(disp, (150, 150, 150), (100, 5, 125, 35))
    disp.blit(printer.write(32, 'New game'), (105, 10))
    pygame.draw.rect(disp, (150, 150, 150), (250, 5, 60, 35))
    disp.blit(printer.write(32, 'Undo'), (250, 10))
    if(len(empty) == 0):
        #print('checkin if lost')
        moves = 0
        for i in range(0, len(board)):
            for j in range(len(board[i]) - 1, -1, -1):
                # print(i, j)
                if board[i][j][0] != 0:
                    # print(board[i][j][1])
                    findDest(i, j, 2)
                    # print(board[i][j][1])
        for i in range(0, len(board)):
            for j in range(0, len(board[i])):
                if board[i][j][0] != 0:
                    # print(board[i][j][1])
                    findDest(i, j, 1)
                    findDest(i, j, 4)
                    # print(board[i][j][1])
        for i in range(len(board) - 1, -1, -1):
            for j in range(0, len(board[i])):
                if board[i][j][0] != 0:
                    # print(board[i][j][1])
                    findDest(i, j, 3)

        if(moves == 0):
            print('lost')
            #FPSCLOCK.tick(.2)
            #pygame.quit()
            #sys.exit('ya done goofed')