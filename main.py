from knowledge_tree import *
from ingest import note_info
from tracker import *

#creted a knowlegetree based on notes
answer = note_info()
new_tree = extract_knowledge_tree(answer)


#getting the leafs 
leafs = {}
def extracting_leafs():
 for b in new_tree.branch:
   for l in b.leaf:
     leafs[l.name] = l.description


# creating an assigning a question for every leaf
def question_assignment(l:dict) -> dict    
extracting_leafs()
print(leafs)




