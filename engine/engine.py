#!/usr/bin/env python

import sys
import os
import subprocess

def run_robot(rName, rIn, rOut):
  print ("Run robot " + rName)
  with open('robots/' + rName + '/run') as runFile:
    runLines = runFile.readlines()
    retCode = subprocess.call(runLines[0].strip() + " \"" + rIn + "\" \"" + rOut + "\"", shell=True, cwd='robots/' + rName)

def readNumbersFromFile(fileName):
  if not os.path.isfile(fileName):
    return []
  result = []
  with open(fileName) as file:
    for val in file.read().split():
      result.append(int(val))
  return result

def trimCoordinate(fieldType, fieldSize, coord):
  if fieldType == 0 and (coord < 0 or coord >= fieldSize):
    return -1
  return coord % fieldSize

def trimPosition(fieldType, fieldSize, position):
  for i in range(len(position)):
    position[i] = trimCoordinate(fieldType, fieldSize, position[i])
    if position[i] == -1:
      return False
  return True

def trimCatcherPositions(fieldType, fieldSize, catcherPositions):
  # Check field bounds
  for i in range(len(catcherPositions)):
    position = catcherPositions[i]
    if not trimPosition(fieldType, fieldSize, position):
      return False
  return True

def isCorrectMotion(dx, dy):
  return -1 <= dx <= 1 and -1 <= dy <= 1 and dx * dy == 0

def isEscapeeCaught(catcherPositions, escapeePosition):
  for position in catcherPositions:
      if position == escapeePosition:
        return True
  return False

def printField(fieldSize, catcherPositions, escapeePosition):
  result = ""
  for y in range(fieldSize):
    for x in range(fieldSize):
      if escapeePosition == [x, y]:
        p = "E"
      else:
        p = "."
        catcherCount = 0
        for cp in catcherPositions:
          if cp == [x, y]:
            catcherCount += 1
        if catcherCount > 0:
          p = str(catcherCount)
      result += p
    result += "\n"
  print result

def writeRobotInputFile(rIn, currentPlayer, fieldType, fieldSize, catcherCount, escapeeSpeed, turnLimit, currentTurn,
                        escapeePosition, catcherPositions):
  with open(rIn, "w") as fi:
    fi.write(str(currentPlayer) + "\n")
    fi.write(str(fieldType) + " " + str(fieldSize) + "\n")
    fi.write(str(catcherCount) + " " + str(escapeeSpeed) + "\n")
    fi.write(str(turnLimit) + " " + str(currentTurn) + "\n")
    fi.write(str(escapeePosition[0]) + " " + str(escapeePosition[1]) + "\n")
    for i in range(catcherCount):
      fi.write(str(catcherPositions[i][0]) + " " + str(catcherPositions[i][1]) + "\n")

def runDuel(fieldType, fieldSize, catcherCount, escapeeSpeed, turnLimit, catcherRobot, escapeeRobot, workDir):
  print ("Run duel\n" + 'fieldType = ' + str(fieldType) + ', fieldSize = ' + str(fieldSize)
         + ', catcherCount = ' + str(catcherCount) + ', escapeeSpeed = ' + str(escapeeSpeed)
         + ', turnLimit = ' + str(turnLimit) + ', catcher robot = ' + str(catcherRobot) + ', escapee robot = ' + str(escapeeRobot))

  catcherPositions = []
  for i in range(catcherCount):
    catcherPositions.append([-1, -1])
  escapeePosition = [-1, -1]

  for currentTurn in range(turnLimit):
    print ('Turn: ' + str(currentTurn))

    stepstr = str(currentTurn).zfill(3)

    print ("Catcher's turn")

    currentPlayer = 0

    rName = catcherRobot
    prefix = workDir + stepstr + '_r' + str(currentPlayer) + '_' + rName
    rIn = prefix + 'i.txt'
    rOut = prefix + 'o.txt'

    writeRobotInputFile(rIn, currentPlayer, fieldType, fieldSize, catcherCount, escapeeSpeed, turnLimit, currentTurn,
                        escapeePosition, catcherPositions)

    run_robot(rName, rIn, rOut)

    answerNumbers = readNumbersFromFile(rOut)

    if len(answerNumbers) == 0:
      print ('Player ' + str(currentPlayer) + '(' + rName + ')' + ' returned nothing.')
      return 0

    if len(answerNumbers) != 2 * catcherCount:
      print ('Player ' + str(currentPlayer) + '(' + rName + ')' + ' returned invalid answer.')
      return 0

    if currentTurn == 0:
      for i in range(catcherCount):
        catcherPositions[i][0] = answerNumbers[2 * i]
        catcherPositions[i][1] = answerNumbers[2 * i + 1]
    else:
      for i in range(catcherCount):
        dx = answerNumbers[2 * i]
        dy = answerNumbers[2 * i + 1]
        if not isCorrectMotion(dx, dy):
          print ("Incorrect motion!")
          return 0
        catcherPositions[i][0] += dx
        catcherPositions[i][1] += dy

    isPositionCorrect = trimCatcherPositions(fieldType, fieldSize, catcherPositions)

    printField(fieldSize, catcherPositions, escapeePosition)

    if not isPositionCorrect:
      print ("Incorrect catcher's position!")
      return 0

    if isEscapeeCaught(catcherPositions, escapeePosition):
      print ("Escapee is caught!")
      return turnLimit - currentTurn

    print ("Escapee's turn")

    currentPlayer = 1

    rName = escapeeRobot
    prefix = workDir + stepstr + '_r' + str(currentPlayer) + '_' + rName
    rIn = prefix + 'i.txt'
    rOut = prefix + 'o.txt'

    writeRobotInputFile(rIn, currentPlayer, fieldType, fieldSize, catcherCount, escapeeSpeed, turnLimit, currentTurn,
                        escapeePosition, catcherPositions)

    run_robot(rName, rIn, rOut)

    answerNumbers = readNumbersFromFile(rOut)

    if len(answerNumbers) == 0:
      print ('Player ' + str(currentPlayer) + '(' + rName + ')' + ' returned nothing.')
      return turnLimit - currentTurn

    if currentTurn == 0:
      if len(answerNumbers) != 2:
        print ('Player ' + str(currentPlayer) + '(' + rName + ')' + ' returned invalid answer.')
        return turnLimit - currentTurn
      escapeePosition = answerNumbers
      if not trimPosition(0, fieldSize, escapeePosition):
        return turnLimit - currentTurn
    else:
      if len(answerNumbers) != 2 * escapeeSpeed:
        print ('Player ' + str(currentPlayer) + '(' + rName + ')' + ' returned invalid answer.')
        return turnLimit - currentTurn
      for i in range(escapeeSpeed):
        dx = answerNumbers[2 * i]
        dy = answerNumbers[2 * i + 1]
        if not isCorrectMotion(dx, dy):
          print ("Incorrect motion!")
          return turnLimit - currentTurn
        escapeePosition[0] += dx
        escapeePosition[1] += dy
        isPositionCorrect = trimPosition(fieldType, fieldSize, escapeePosition)
        printField(fieldSize, catcherPositions, escapeePosition)
        if not isPositionCorrect:
          print ("Incorrect escapee's position! Escapee is caught on turn " + str(currentTurn))
          return turnLimit - currentTurn
        if isEscapeeCaught(catcherPositions, escapeePosition):
          print ("Escapee is caught on turn " + str(currentTurn))
          return turnLimit - currentTurn

  print ("Turn limit is exhausted! Escapee wins!")
  return 0

def sim(fieldType, fieldSize, catcherCount, escapeeSpeed, turnLimit, robots, workDir):
  print ("Simulation\n" + 'fieldType = ' + str(fieldType) + ', fieldSize = ' + str(fieldSize)
         + ', catcherCount = ' + str(catcherCount) + ', escapeeSpeed = ' + str(escapeeSpeed)
         + ', turnLimit = ' + str(turnLimit) + ', robots: ' + str(robots))

  robotCount = len(robots)
  robotScores = []
  for i in range(robotCount):
    robotScores.append(0)

  for i in range(robotCount):
    for j in range(i):
      result = runDuel(fieldType, fieldSize, catcherCount, escapeeSpeed, turnLimit, robots[i], robots[j], workDir)
      robotScores[i] += result
      robotScores[j] += turnLimit - result

      result = runDuel(fieldType, fieldSize, catcherCount, escapeeSpeed, turnLimit, robots[j], robots[i], workDir)
      robotScores[j] += result
      robotScores[i] += turnLimit - result

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
