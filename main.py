from knowledge_tree import *
from ingest import *
from tracker import *
from quiz import quiz
from evaluator import *
from scheduler import *



print("Welcome to Studdy Budyy!")
#creted a knowlegetree based on notes
print("generating question...")


#only leafs
def extracting_leafs(tree):
  leafs = []
  for b in tree.branch:
    for l in b.leaf:
       leafs.append(l)
  return leafs

#getting the leafs 
def recording_leafs(leafs:list):
  recorded_leafs = {}
  for l in leafs:
    recorded_leafs[l.name] = new_record(l)

  return recorded_leafs


def lazy_generator(recorded: dict):
  names = list(recorded.keys()) 
  if os.path.exists("index.json") and os.path.exists("index.json") > 0:
     state = read_json("index.json")
     i = state["i"]
  else: 
     i =0   
  while( i < len(recorded) ): 
   card = recorded[names[i]]
   name = card["leaf"]["name"]
   description = card["leaf"]["description"]
   leaf = Leaf(name=name,description=description)
   question = quiz(leaf[i])
   card["question"] = question
   print(question)
   answer  = read_multiline("Please paste your answer here: ")
   print("Calculating...")
   while not answer:
      answer = input("Answer can't be empty. Try again: ").strip()
   score =  evaluator(leaf[i],question , answer)
   new_score = converter(score.score)
   r,e,it = scheduling(new_score,card["repetition"],card["ease_factor"],card["interval"])
   card["repetition"] = r
   card["ease_factor"] = e
   card["interval"] = it
   write_json(recorded,"test.json")
   choice = input("1. Generate next question\n2. Quit\nChoose: ").strip()
   while choice not in ("1", "2"):
    print("Type 1 or 2.")
    choice = input("Choose: ").strip()

   if choice == "1":
     i = i + 1
     continue
   elif choice == "2":
     write_json({"i": i}, "index.json")
     print("Goodbye!")
     return


if os.path.exists("test.json" and os.path.exists("test.json") > 0):
  recorded = read_json("test.json")
else:
  notes = read_multiline(input("Please paste your notes here"))
  new_tree = extract_knowledge_tree(notes)
  list_of_leafs =  extracting_leafs(new_tree)   
  recorded = recording_leafs(list_of_leafs)

lazy_generator(recorded)






