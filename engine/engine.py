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
          coords = map(int, line.split())
          result.append(coords)

    return result

def boundaryCoordinate(fieldType, fieldSize, coord):
    if coord < 0:
      if fieldType == 0:
        return -1
      else:
        return coord + fieldSize
    elif coord >= fieldSize:
      if fieldType == 0:
        return -1
      else:
        return coord - fieldSize

    return coord

def fixPosition(fieldType, fieldSize, position):
    for p in position:
      p = boundaryCoordinate(fieldType, fieldSize, p)
      if p == -1:
        return false
    return true

def fixCatcherPositions(fieldType, fieldSize, catcherPositions):
  # Check field bounds
  for i in range(len(catcherPositions)):
    cp = catcherPositions[i]
    if not fixPosition(fieldType, fieldSize, cp):
      return false

    for j in range(i):
      if catcherPositions[j] == cp:
        return false

    return true





def runDuel(fieldType, fieldSize, catcherCount, escapeeSpeed, turnLimit, catcherRobot, escapeeRobot, workDir):
  print ("Run duel\n" + 'fieldType = ' + str(fieldType) + 'fieldSize = ' + str(fieldSize)
         + 'catcherCount = ' + str(catcherCount) + 'escapeeSpeed = ' + str(escapeeSpeed)
         + 'turnLimit = ' + str(turnLimit) + 'catcher robot: ' + str(catcherRobot) + 'escapee robot: ' + str(escapeeRobot))

  catcherPositions = [[-1, -1] for i in range(catcherCount)]
  escapeePosition = [-1, -1]

  for currentTurn in range(turnLimit):
    print ('Turn: ' + str(currentTurn))

    print ("Catcher's turn")

    currentPlayer = 0

    rName = catcherRobot
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

    answerNumbers = readAnswerNumbers(rOut)

    if len(answerNumbers) == 0:
      prevTurn += 'Player ' + str(currentPlayer) + '(' + rName + ')' + ' returned nothing.'
      return 0;

    if len(answerNumbers) != 2 * catcherCount:
      prevTurn += 'Player ' + str(currentPlayer) + '(' + rName + ')' + ' returned invalid answer.'
      return 0;

    if currentTurn == 0:
      for i in range(catcherCount):
        catcherPositions[i][0] = answerNumbers[2 * i]
        catcherPositions[i][1] = answerNumbers[2 * i + 1]
    else:
      for i in range(catcherCount):
        an1 = answerNumbers[2 * i]
        an2 = answerNumbers[2 * i + 1]
        if an1 < -1 or an1 > 1 or an2 < -1 or an2 > 1 or an1 * an2 != 0:
          return 0;
        catcherPositions[i][0] += an1
        catcherPositions[i][1] += an2

    if not fixCatcherPositions(fieldType, fieldSize, catcherPositions):
      return 0;

    for cp in catcherPositions:
      if cp == escapeePosition:
        print ("Escapee is caught!")
        return turnLimit - currentTurn;

    print ("Escapee's turn")

    currentPlayer = 1

    with open(rIn, "w") as fi:
      fi.write(currentPlayer)
      fi.write(fieldType, fieldSize)
      fi.write(catcherCount, escapeeSpeed)
      fi.write(turnLimit, currentTurn)
      fi.write(escapeePosition)
      fi.write(catcherPositions)

    rName = escapeeRobot
    prefix = workDir + stepstr + '_r' + str(curPlayer) + '_' + rName
    rIn = prefix + 'i.txt'
    rOut = prefix + 'o.txt'

    run_robot(rName, rIn, rOut)

    answerNumbers = readAnswerNumbers(rOut)

    if len(answerNumbers) == 0:
      prevTurn += 'Player ' + str(currentPlayer) + '(' + rName + ')' + ' returned nothing.'
      return turnLimit - currentTurn

    if currentTurn == 0:
      if len(answerNumbers) != 2:
        prevTurn += 'Player ' + str(currentPlayer) + '(' + rName + ')' + ' returned invalid answer.'
        return turnLimit - currentTurn
      escapeePosition = answerNumbers
      if not fixPosition(0, fieldSize, escapeePosition):
        return turnLimit - currentTurn
    else:
      if len(answerNumbers) != 2 * escapeeSpeed:
        prevTurn += 'Player ' + str(currentPlayer) + '(' + rName + ')' + ' returned invalid answer.'
        return turnLimit - currentTurn
      for i in range(escapeeSpeed):
        an1 = answerNumbers[2 * i]
        an2 = answerNumbers[2 * i + 1]
        if an1 < -1 or an1 > 1 or an2 < -1 or an2 > 1 or an1 * an2 != 0:
          return turnLimit - currentTurn
        escapeePosition[0] += an1
        escapeePosition[1] += an2

    if not fixPosition(fieldType, fieldSize, escapeePosition):
        return turnLimit - currentTurn

    for cp in catcherPositions:
      if cp == escapeePosition:
        print ("Escapee is caught!")
        return turnLimit - currentTurn



def sim(fieldType, fieldSize, catcherCount, escapeeSpeed, turnLimit, robots, workDir):
  print ("Simulation\n" + 'fieldType = ' + str(fieldType) + 'fieldSize = ' + str(fieldSize)
         + 'catcherCount = ' + str(catcherCount) + 'escapeeSpeed = ' + str(escapeeSpeed)
         + 'turnLimit = ' + str(turnLimit) + 'robots: ' + str(robots))

  robotCount = len(robots)
  robotScores = [] + robotCount

  for i in range(robotCount):
    for j in range(i):
      r = runDuel(fieldType, fieldSize, catcherCount, escapeeSpeed, turnLimit, robots[i], robots[j], workDir)
      robotScores[i] += r
      robotScores[j] += turnLimit - r

      r = runDuel(fieldType, fieldSize, catcherCount, escapeeSpeed, turnLimit, robots[j], robots[i], workDir)
      robotScores[j] += r
      robotScores[i] += turnLimit - r

  print ("Final score:")

  for i in range(robotCount):
    print ("Robot " + str(i) + ": " + str(robotScores[i]))

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
  for i in range(len(content) - 5):
    robots.append(content[i+5].strip())

  sim(fieldType, fieldSize, catcherCount, escapeeSpeed, turnLimit, robots, workDir)

if __name__ == '__main__':
  main()
