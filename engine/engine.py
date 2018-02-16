#!/usr/bin/env python

import sys
import os
import subprocess
from random import randint, seed

EMPTY = 0
TOWER = 11
CORNERS = [[-1,-1], [0,0], [0,7], [7,7], [7,0]]

def arena_to_str(A): return ((' \n'.join([''.join(['{:3}'.format(item) for item in row]) for row in A])) + ' \n')
def arena_to_log(A): return arena_to_str(A).replace(' 0 ', '   ')

def run_robot(rName, rIn, rOut):
  print ("Run robot " + rName)
  with open('robots/' + rName + '/run') as runFile:
    runLines = runFile.readlines()
    retCode = subprocess.call(runLines[0].strip() + " \"" + rIn + "\" \"" + rOut + "\"", shell=True, cwd='robots/' + rName)

def isMoveCorrect(a, curPlayer, coord, move):
  newCoord = [coord[0] +  move[0], coord[1] + move[1]]
  if newCoord[0] < 0 or newCoord[0] > 7 or newCoord[1] < 0 or newCoord[1] > 7:
    return False
  if a[newCoord[0]][newCoord[1]] > 4 and abs(move[0]) + abs(move[1]) != 1:
    return False
  if a[newCoord[0]][newCoord[1]] == curPlayer * TOWER:
    return False

  firstHorMove = []
  for i in range(1, abs(move[0])):
    firstHorMove.append([coord[0] + i * move[0] // abs(move[0]), coord[1]])
  for i in range(0, abs(move[1])):
    firstHorMove.append([coord[0] + move[0], coord[1] + i * move[1] // abs(move[1])])
  nbEmpty = 0
  for p in firstHorMove:
    if a[p[0]][p[1]] == EMPTY:
      nbEmpty += 1
  if nbEmpty == len(firstHorMove):
    return True

  firstVerMove = []
  for i in range(1, abs(move[1])):
    firstVerMove.append([coord[0], coord[1] + i * move[1] // abs(move[1])])
  for i in range(0, abs(move[0])):
    firstVerMove.append([coord[0] + i * move[0] // abs(move[0]), coord[1] + move[1]])
  nbEmpty = 0
  for p in firstVerMove:
    if a[p[0]][p[1]] == EMPTY:
      nbEmpty += 1
  if nbEmpty == len(firstVerMove):
    return True

  return False

def isMovePossible(a, curPlayer, rnd):
  rPieces = []
  for i in range(8):
    for j in range(8):
      if a[i][j] == curPlayer or a[i][j] == TOWER*curPlayer:
        rPieces.append([i, j])
  for moveFrom in rPieces:
    for d0 in [-1, 1]:
      for d1 in [-1, 1]:
        for m0 in range(rnd + 1):
          m1 = rnd - m0
          if isMoveCorrect(a, curPlayer, moveFrom, [d0 * m0, d1 * m1]):
            return True
  return False

def oneWinner(a):
  nbPieces = []
  for i in range(5):
    nbPieces.append(0)
  for i in range(8):
    for j in range(8):
      if a[i][j] == EMPTY:
        continue
      if a[i][j] in range(1, 5):
        nbPieces[a[i][j]] +=1
      else:
        if a[i][j] // TOWER in range(1, 5):
          nbPieces[a[i][j] // TOWER] += 2
  nbNotZero = 0
  for i in range(1, 5):
    if nbPieces[i] > 0:
      nbNotZero += 1
  return nbNotZero == 1

def twoWinners(a):
  nbPieces = []
  for i in range(5):
    nbPieces.append(0)
  for i in range(8):
    for j in range(8):
      if a[i][j] == EMPTY:
        continue
      if a[i][j] in range(1, 5):
        nbPieces[a[i][j]] +=1
      else:
        if a[i][j] // TOWER in range(1, 5):
          nbPieces[a[i][j] // TOWER] += 2
  nbNotZero = 0
  notZeroIdx = []
  for i in range(1, 5):
    if nbPieces[i] > 0:
      nbNotZero += 1
      notZeroIdx.append(i)
  return nbNotZero == 2 and notZeroIdx[1] - notZeroIdx[0] == 2

def readAnswerNumbers(rOut):
    if not os.path.isfile(rOut):
      return []

    result = []

    with open(rOut) as fo:
      res = fo.readlines()
      if len(res) > 0:
        for line in res:
          coords = line.split()
          result.append(coords)

    return result

def sim(fieldType, fieldSize, catcherCount, escapeeSpeed, turnLimit, robots, workDir):
  print ("Simulation\n" + 'fieldType = ' + str(fieldType) + 'fieldSize = ' + str(fieldSize)
         + 'catcherCount = ' + str(catcherCount) + 'escapeeSpeed = ' + str(escapeeSpeed)
         + 'turnLimit = ' + str(turnLimit) + 'robots: ' + str(robots))

  escapeePosition = [-1, -1]
  catcherPositions = [[-1, -1] for i in range(catcherCount)]

  for currentTurn in range(turnLimit):
    print ('Turn: ' + str(currentTurn))

    currentPlayer = 0

    rName = robots[curPlayer]
    prefix = workDir + stepstr + '_r' + str(curPlayer) + '_' + rName
    rIn = prefix + 'i.txt'
    rOut = prefix + 'o.txt'

    with open(rIn, "w") as fi:
      fi.write(currentPlayer)
      fi.write(fieldType, fieldSize)
      fi.write(catcherCount, escapeeSpeed)
      fi.write(turnLimit, currentTurn)
      fi.write(escapeePosition)
      fi.write(catcherPositions)

    run_robot(rName, rIn, rOut)

    if not os.path.isfile(rOut):
      prevTurn += 'Player ' + str(curPlayer) + '(' + rName + ')' + ' returned nothing.'
      return currentTurn;
    coords = readAnswerNumbers(rOut)

    if currentPlayer == 0:
      if currentTurn == 0:
        if len(coords) != 2 * catcherCount
          continue

    for player in range(2):
      if a[CORNERS[player][0]][CORNERS[player][1]] == EMPTY or a[CORNERS[player][0]][CORNERS[player][1]] == player * TOWER:
        a[CORNERS[player][0]][CORNERS[player][1]] = player

    curPlayer = curPlayer + 1 if curPlayer < 4 else 1
    stepstr = str(step).zfill(3)
    rnd = randint(1, 6)
    print (arena_to_log(a) + "\n" + prevTurn)
    prevTurn = ''
    print ('Step: ' + str(step) + ', rnd = ' + str(rnd) + ', current player: ' + str(curPlayer))

    if gameType == 0 and oneWinner(a):
      print ('One winner')
      break

    if gameType == 1 and twoWinners(a):
      print ('Two winners')
      break

    if gameType == 1 and not isMovePossible(a, curPlayer, rnd):
      curPlayerBkp = curPlayer;
      curPlayer = curPlayer + 2 if curPlayer < 3 else curPlayer - 2
      print ('Player ' + str(curPlayerBkp) + ' has to skip his move, so ' + str(curPlayer) + ' will move.')

    if gameType == 0 and not isMovePossible(a, curPlayer, rnd):
      print ('Player ' + str(curPlayer) + ' has to skip his move.')
    else:
      rName = robots[curPlayer-1]
      prefix = workDir + stepstr + '_r' + str(curPlayer) + '_' + rName
      rIn  = prefix + 'i.txt'
      rOut = prefix + 'o.txt'
      rInText = str(curPlayer) + ' ' + str(rnd) + "\n" + arena_to_str(a)
      with open(rIn, "w") as fi:
        fi.write(rInText)
      run_robot(rName, rIn, rOut)
      moveFrom = [-1, -1]
      move = [0, 0]
      if not os.path.isfile(rOut):
        prevTurn += 'Player ' + str(curPlayer) + '(' + rName + ')' + ' returned nothing.'
        continue
      with open(rOut) as fo:
        res = fo.readlines()
        if len(res) > 0:
          s = res[0].split()
          if len(s) == 4:
            moveFrom[0] = int(s[0])
            moveFrom[1] = int(s[1])
            move[0] = int(s[2])
            move[1] = int(s[3])
            print ('Move ' + str(moveFrom) + ' ' + str(move))
            if abs(move[0]) + abs(move[1]) != rnd:
              prevTurn += 'Player ' + str(curPlayer) + '(' + rName + ')' + ': wrong length of move.'
              continue
            if a[moveFrom[0]][moveFrom[1]] != curPlayer and a[moveFrom[0]][moveFrom[1]] != TOWER * curPlayer:
              prevTurn += 'Player ' + str(curPlayer) + '(' + rName + ')' + ': move from wrong place.'
              continue
            if not isMoveCorrect(a, curPlayer, moveFrom, move):
              prevTurn += 'Player ' + str(curPlayer) + '(' + rName + ')' + ': incorrect move.'
              continue
            prevTurn += 'Player ' + str(curPlayer) + '(' + rName + ')' + ' moved from ' + str(moveFrom) + ', move: ' + str(move) + '.'

      if moveFrom[0] < 0 or moveFrom[1] < 0:       
        continue

      if a[moveFrom[0]][moveFrom[1]] == curPlayer or a[moveFrom[0]][moveFrom[1]] == curPlayer * TOWER:
        if a[moveFrom[0] + move[0]][moveFrom[1] + move[1]] == curPlayer:
          a[moveFrom[0] + move[0]][moveFrom[1] + move[1]] = curPlayer * TOWER
        else:
          a[moveFrom[0] + move[0]][moveFrom[1] + move[1]] = curPlayer
        if a[moveFrom[0]][moveFrom[1]] == curPlayer:
          a[moveFrom[0]][moveFrom[1]] = EMPTY
        else:
          a[moveFrom[0]][moveFrom[1]] = curPlayer

def main(argv=None):
  if len(sys.argv) < 2:
    sys.stderr.write('Usage: ' + sys.argv[0] + ' replayin.txt')
    sys.exit(1)

  if not os.path.exists(sys.argv[1]):
    sys.stderr.write('ERROR: File ' + sys.argv[1] + ' not found!')
    sys.exit(1)

  workDir = os.path.join(os.getcwd(), "output", "")
  if not os.path.exists(workDir):
    os.makedirs(workDir)

  with open(sys.argv[1]) as fi:
    content = fi.readlines()

  if len(content) < 7:
    sys.stderr.write('ERROR: Not enough lines in the file ' + sys.argv[1] + '!')
    sys.exit(1)

  fieldType = int(content[0])
  fieldSize = int(content[1])
  catcherCount = int(content[2])
  escapeeSpeed = int(content[3])
  turnLimit = int(content[4])

  robots = []
  for i in range(2):
    robots.append(content[i+4].strip())

  sim(fieldType, fieldSize, catcherCount, escapeeSpeed, turnLimit, robots, workDir)

if __name__ == '__main__':
  main()
