#
# Script to generate valid puzzles based on the Fickle Sentries scenario
#

#set up the sets used in the puzzle
allTreasures = ['copper','silver', 'gold', 'platinum', 'diamonds','rubies']
guard1_lies = ['copper','silver', 'gold']
guard2_lies = ['platinum', 'diamonds','rubies']
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
    return {'statement': "The treasure is either " + t1 +" or " + t2 + "." , 'items': [t1,t2]}
    
annotatedStatements = []
for t in allTreasures:
    annotatedStatements.append(simpleStatement(t))
    annotatedStatements.append(negativeStatement(t))
    annotatedStatements.append(moreValuableStatement(t))
    annotatedStatements.append(lessValuableStatement(t))
    for s in allTreasures:
        if (s == t):
            continue
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
    puzzle['guard1_items'] = str(g1_statement['items'])
    puzzle['guard1_options'] = str(guard1)
    puzzle['guard2_items'] = str(g2_statement['items'])
    puzzle['guard2']= g2_statement['statement']
    puzzle['guard2_options'] = str(guard2)
    puzzle['solution'] = hiddenTreasure[0]
    puzzle['explanation'] = explain(g1t, g1l, g2t,g2l, hiddenTreasure[0])
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

def explain(g1t, g1l, g2t, g2l, sol):
    exp = ""
    if (len(g1t) != 0):
        exp += "If Guard 1 is telling the truth, then the treasure "
        if (len(g1t) == 1):
            exp += "must be "
        else:
            exp += "can be "
        exp += prettyList(g1t,"or") +"."
    else :
        exp += "Because Guard 1 lies when guarding " + prettyList(guard1_lies,"and")
        exp += ", she cannot be telling the truth."    
    if (len(g1l) != 0):
        exp += " If Guard 1 is lying, then the treasure "
        if (len(g1l) == 1):
            exp += "must be "
        else:
            exp += "can be "
        exp += prettyList(g1l,"or") + "."
     
    if (len(g2t) != 0):
        exp += " If Guard 2 is telling the truth, then the treasure "
        if (len(g2t) == 1):
            exp += "must be "
        else:
            exp += "can be "
        exp += prettyList(g2t,"or") +"."
    else :
        exp += " Because Guard 2 lies when guarding " + prettyList(guard2_lies,"and")
        exp += ", she cannot be telling the truth."    
    if (len(g2l) != 0):
        exp += " If Guard 2 is lying, then the treasure "
        if (len (g2l) == 1):
            exp += "must be "
        else:
            exp += "can be "
        exp += prettyList(g2l,"or") + "."

    exp += " The  only possible option based on the " 
    exp += "statements of both guards is " + sol + "."
    return exp 

def jsonForPuzzle(puzzle):

    json = '{"guard1": "' + puzzle['guard1'] + '", ' 
    json += ' "guard2": "' + puzzle['guard2'] + '", ' 
    json += ' "guard1_options": "' + puzzle['guard1_options'] + '", ' 
    json += ' "guard2_options": "' + puzzle['guard2_options'] + '", ' 
    json += ' "guard1_items": "' + puzzle['guard1_items'] + '", ' 
    json += ' "guard2_items": "' + puzzle['guard2_items'] + '", ' 
    
    json += ' "solution": "' + puzzle['solution'] + '", '
    json += ' "explanation": "' + puzzle['explanation'] + '", '
   
    json += ' "id": "' + str(puzzle['id']) + '"}' + '\n'
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
