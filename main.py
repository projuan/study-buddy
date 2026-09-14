from knowledge_tree import *
from ingest import note_info
from tracker import *
from quiz import quiz

#creted a knowlegetree based on notes
answer = note_info()
new_tree = extract_knowledge_tree(answer)


#getting the leafs 

def extracting_leafs():
  recorded_leafs = {}
  for b in new_tree.branch:
   for l in b.leaf:
     recorded = new_record(l)
     recorded_leafs[l.name] = recorded
  return recorded_leafs
 
     




 #creating an assigning a question for every leaf
#def question_assignment(l:dict) -> dict:
  #for o in l:
   # question = quiz(l)



data = extracting_leafs()
print(data)




