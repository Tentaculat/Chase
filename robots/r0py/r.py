#!/usr/bin/env python

import sys
import os

def readNumbersFromFile(fileName):
  if not os.path.isfile(fileName):
    return []
  result = []
  with open(fileName) as file:
    for val in file.read().split():
      result.append(int(val))
  return result

def main(argv=None):
  print ('R0py')

  if len(sys.argv) < 3:
    sys.stderr.write('Usage: ' + sys.argv[0] + ' input.txt output.txt')
    sys.exit(1)

  if not os.path.exists(sys.argv[1]):
    sys.stderr.write('ERROR: File ' + sys.argv[1] + ' not found!')
    sys.exit(1)

  inputNumbers = readNumbersFromFile(sys.argv[1])

  if len(inputNumbers) < 11:
    sys.stderr.write('ERROR: Incorrect input!')
    sys.exit(1)

  role = inputNumbers[0]
  fieldType = inputNumbers[1]
  fieldSize = inputNumbers[2]
  catcherCount = inputNumbers[3]
  if len(inputNumbers) != 9 + 2 * catcherCount:
    sys.stderr.write('ERROR: Incorrect input!')
    sys.exit(1)
  escapeeSpeed = inputNumbers[4]
  turnLimit = inputNumbers[5]
  currentTurn = inputNumbers[6]
  escapeePosition = [inputNumbers[7], inputNumbers[8]]
  catcherPositions = []
  for i in range(catcherCount):
    catcherPositions.append([inputNumbers[8 + 2 * i], inputNumbers[9 + 2 * i]])

  answer = ""

  if role == 0:
    if currentTurn == 0:
      x = 0
      y = 0
      for i in range(catcherCount):
        answer += str(x) + " " + str(y) + "\n"
        x += 1
        if x >= fieldSize:
          x = 0
          y += 1
    else:
      dx = 0
      dy = 1
      for i in range(catcherCount):
        answer += str(dx) + " " + str(dy) + "\n"
  else:
    if currentTurn == 0:
      x = int(fieldSize / 2)
      y = int(fieldSize / 2)
      answer += str(x) + " " + str(y) + "\n"
    else:
      dx = 0
      dy = 1
      for i in range(escapeeSpeed):
        answer += str(dx) + " " + str(dy) + "\n"

  with open(sys.argv[2], 'w') as fo:
    fo.write(answer)
    fo.close

if __name__ == '__main__':
  main()
