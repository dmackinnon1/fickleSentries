#
# Script to generate valid puzzles based on the Fickle Sentries scenario
#

def validPuzzle(statement1, statement2):
    puzzle = {};
    return puzzle

def prettyList(list, conj):
    isFirst = True;
    result = ""
    count = 1
    size = len(list)
    for s in list:
        if not isFirst and size > 2:
            result += ", "
        isFirst  = False
        if count == size and size > 1:
            if (size == 2):
                result += " "
            result += conj + " "
        count = count +1
        result += s
    return result


counter = 0
validPuzzles = []
for s1 in allAnnotated:
    for s2 in allAnnotated:
        puzzle = validPuzzle(s1,s2)        
        if(len(puzzle) > 0):
            counter = counter + 1
            puzzle['id'] = counter
            validPuzzles.append(jsonForPuzzle(puzzle))
result = "["
first = True
for p in validPuzzles:
    if not first:
        result += ", \n"
    else:
        first = False
    result += p
result += "]"

f = open("../data/fickle.json","w")
f.write( result )
f.close()
