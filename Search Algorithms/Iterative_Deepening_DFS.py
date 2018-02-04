''' anirao26_IDDFS.py
 Ierative Deepening Depth-First Search of a problem space.
 Version 0.1, January 25, 2018.
 Anirudh Rao, Univ. of Washington.
'''

import sys

if sys.argv==[''] or len(sys.argv)<2:
#  import EightPuzzle as Problem
  import TowersOfHanoi as Problem
else:
  import importlib
  Problem = importlib.import_module(sys.argv[1])

print("\nWelcome to IDDFS")
COUNT = None
BACKLINKS = {}
DEPTH = 0
node_depth_dict = {}


def runIDDFS():
  initial_state = Problem.CREATE_INITIAL_STATE()
  print("Initial State:")
  print(initial_state)
  global COUNT, BACKLINKS, MAX_OPEN_LENGTH
  COUNT = 0
  BACKLINKS = {}
  MAX_OPEN_LENGTH = 0
  node_depth_dict[initial_state] = DEPTH
  IterativeDFS(initial_state, 0)
  print(str(COUNT)+" states expanded.")
  print('MAX_OPEN_LENGTH = '+str(MAX_OPEN_LENGTH))

    
def IterativeDFS(initial_state, depth):
  print("\nDepth is: ", depth)
  global COUNT, BACKLINKS, MAX_OPEN_LENGTH

  success_flag = False # An indicator to identify when a goal state is reached

# STEP 1. Put the start state on a list OPEN
  OPEN = [initial_state]
  CLOSED = []
  BACKLINKS[initial_state] = None

# STEP 2. If OPEN is empty, output “DONE” and stop.

  while OPEN != []:
    report(OPEN, CLOSED, COUNT)
    if len(OPEN)>MAX_OPEN_LENGTH: MAX_OPEN_LENGTH = len(OPEN)

# STEP 3. Select the first state on OPEN and call it S.
#         Delete S from OPEN.
#         Put S on CLOSED.
#         If S is a goal state, output its description

    S = OPEN.pop(0)
    CLOSED.append(S)

    if Problem.GOAL_TEST(S):
      print(Problem.GOAL_MESSAGE_FUNCTION(S))
      path = backtrace(S)
      print('Length of solution path found: '+str(len(path)-1)+' edges')
      success_flag = True
      break
    COUNT += 1

# STEP 4. Generate the list L of successors of S and delete 
#         from L those states already appearing on CLOSED.

# STEP 5. Delete from OPEN any members of OPEN that occur on L.
#         Insert all members of L at the front of OPEN.

    L = []
    if(node_depth_dict[S] + 1 <= depth):
      for op in Problem.OPERATORS:
        if op.precond(S):
          new_state = op.state_transf(S)
          if not (new_state in CLOSED):
            L.append(new_state)
            if new_state not in BACKLINKS:
              BACKLINKS[new_state] = S
            node_depth_dict[new_state] = node_depth_dict[S] + 1

      for s2 in L:
        for i in range(len(OPEN)):
          if (s2 == OPEN[i]):
            del OPEN[i]; break
    
    OPEN = L + OPEN
    print_state_list("OPEN", OPEN)

# STEP 6. Go to Step 2.
  if(success_flag):
    return # If goal found return to the main program
  else:
    IterativeDFS(initial_state, depth + 1) # Recursion call


def print_state_list(name, lst):
  print(name+" is now: ",end='')
  for s in lst[:-1]:
    print("\n", str(s),end=', ')
    

def backtrace(S):
  global BACKLINKS
  path = []
  while S:
    path.append(S)
    S = BACKLINKS[S]
  path.reverse()
  print("Solution path: ")
  for s in path:
    print(s)
  print("\n")
  return path 
  
def report(open, closed, count):
  print("len(OPEN)="+str(len(open)), end='; ')
  print("len(CLOSED)="+str(len(closed)), end='; ')
  print("COUNT = "+str(count))

if __name__=='__main__':
  runIDDFS()
