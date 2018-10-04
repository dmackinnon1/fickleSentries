#
# Script to generate valid puzzles based on the Fickle Sentries scenario
#

#set up the sets used in the puzzle
allTreasures = ['silver', 'gold', 'platinum', 'diamonds']
guard1_lies = ['silver', 'gold']
guard2_lies = ['platinum', 'diamonds']
# given a list of treasures, what treasures are missing
def complement(listOfTreasure):
    return [treasure for treasure in allTreasures if treasure not in listOfTreasure]

guard1_truths = complement(guard1_lies)
guard2_truths = complement(guard2_lies)

# define other set operations
# return the treasures common to two lists
def intersect(a, b):
    return [item for item in a if item in b]
    
# return the treasures in both lists
def union(a, b):
    return list(a) + [item for item in b if item not in a]

##define an ordering on the set of items - later items are more valuable
def moreValuable (treasure):
    pos = allTreasures.index(treasure)
    if (pos + 1) == len(allTreasures):
        return []
    return allTreasures[(pos +1):len(allTreasures)]

def lessValuable (treasure):
    pos = allTreasures.index(treasure)
    if (pos) == 0:
        return []
    return allTreasures[0:pos]

# statement types

def simpleStatement(treasure):
    return {'statement': "The cave contains " + treasure + ".",'items':[treasure]}

def negativeStatement(treasure):
    return {'statement': "The cave does not contain " + treasure + ".", 'items': complement([treasure])}

def moreValuableStatement(treasure):
    return {'statement': "The treasure is more valuable than " + treasure +".", 'items': moreValuable(treasure)}

def lessValuableStatement(treasure):
    return {'statement': "The treasure is less valuable than " + treasure +".", 'items': lessValuable(treasure)}

def compoundStatement(t1, t2):
    return {'statement': "The treasure is either " + t1 +" or " + t2 + "." , 'items': [[t1,t2]]}
    
annotatedStatements = []
for t in allTreasures:
    annotatedStatements.append(simpleStatement(t))
    annotatedStatements.append(negativeStatement(t))
    annotatedStatements.append(moreValuableStatement(t))
    annotatedStatements.append(lessValuableStatement(t))
    for s in allTreasures:
        annotatedStatements.append(compoundStatement(t,s))

def validPuzzle(g1_statement, g2_statement):
    puzzle = {}
    if len(g1_statement['items']) == 0 or len(g2_statement['items']) == 0:
          return puzzle
    g1t = intersect(g1_statement['items'], guard1_truths) 
    g1l = intersect(complement(g1_statement['items']), guard1_lies)
    guard1 = union(g1t, g1l)
    g2t = intersect(g2_statement['items'], guard2_truths) 
    g2l = intersect(complement(g2_statement['items']), guard2_lies)
    guard2 = union(g2t, g2l)
    hiddenTreasure = intersect(guard1,guard2)
    if (len(hiddenTreasure) != 1):
        return puzzle
    puzzle['guard1']= g1_statement['statement']
    puzzle['guard2']= g2_statement['statement']
    puzzle['solution'] = hiddenTreasure[0]
    return puzzle

def jsonForPuzzle(puzzle):
    json = '{"guard1": "' + puzzle['guard1'] + '",' 
    json += ' "guard2": "' + puzzle['guard2'] + '",' 
    json += ' "solution": "' + puzzle['solution'] + '"}' + '\n'
    return json

counter = 0
validPuzzles = []
for s1 in annotatedStatements:
    for s2 in annotatedStatements:
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
print("There were " + str(counter) + " puzzles generated")

f = open("../data/fickle.json","w")
f.write( result )
f.close()
