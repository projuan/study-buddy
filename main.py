from knowledge_tree import *
from ingest import *
from tracker import *
from quiz import quiz
from evaluator import *
from scheduler import *



print("Welcome to Studdy Budyy!")
#creted a knowlegetree based on notes
notes = read_multiline(input("Please paste your notes here"))
print("generating question...")
new_tree = extract_knowledge_tree(notes)

#only leafs
def extracting_leafs():
  leafs = []
  for b in new_tree.branch:
    for l in b.leaf:
       leafs.append(l)
  return leafs

#getting the leafs 
def recording_leafs(leafs:list):
  recorded_leafs = {}
  for l in leafs:
    recorded_leafs[l.name] = new_record(l)

  return recorded_leafs


def lazy_generator(leafs:list , recorded: dict):
  if os.path.exists("index.json") and os.path.exists("progress.json") > 0:
     state = read_json("index.json")
     i = state["i"]
     c = state["c"]
  else: 
     i =0
     c =0   
  while(i < len(leafs)  and c < len(recorded) ): 
   question = quiz(leafs[i])
   names = list(recorded.keys())
   card = recorded[names[i]]
   card["question"] = question
   print(question)
   answer  = read_multiline("Please paste your answer here: ")
   print("Calculating...")
   while not answer:
      answer = input("Answer can't be empty. Try again: ").strip()
   score =  evaluator(leafs[i],question , answer)
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
     continue
   elif choice == "2":
     write_json({"i": i, "c": c}, "index.json")
     print("Goodbye!")
     return

list_of_leafs =  extracting_leafs()   
lazy_generator(list_of_leafs, recording_leafs(list_of_leafs))






