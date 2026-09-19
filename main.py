from knowledge_tree import *
from ingest import *
from tracker import *
from quiz import quiz
from evaluator import *
from scheduler import *
from datetime import datetime, timedelta
import display


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
  while(True): 
   today = datetime.now()
   due_name  , size= next_due(recorded)
   if due_name is  None:
     display.caught_up()
     return
   else:
     name = due_name
     card = recorded[due_name]

   name = card["leaf"]["name"] 
   description = card["leaf"]["description"]
   leaf = Leaf(name=name,description=description)
   display.card_header(name, size)
   display.thinking("generating question...")
   question = quiz(leaf)
   card["question"] = question
   display.show_question(question)
   answer  = read_multiline("Your answer", blanks_needed=1)
   display.thinking("grading...")
   score =  evaluator(leaf,question , answer)
   new_score = converter(score.score)
   r,e,it = scheduling(new_score,card["repetition"],card["ease_factor"],card["interval"])
   card["repetition"] = r
   card["ease_factor"] = e
   card["interval"] = it 
   new_date = today + timedelta(days=it)
   card["due_date"] = new_date.strftime("%Y-%m-%d")
   write_json(recorded,"test.json")
   display.show_grade(score.score, score.feedback)
   display.show_next_review(it, card["due_date"])

   if display.menu() == "next":
    
     continue
   else:
     display.goodbye()
     return



display.banner()

if os.path.exists("test.json") and os.path.getsize("test.json") > 0:
  recorded = read_json("test.json")
else:
  notes = read_multiline("Paste your notes")
  new_tree = extract_knowledge_tree(notes)
  list_of_leafs =  extracting_leafs(new_tree)   
  recorded = recording_leafs(list_of_leafs)


def next_due(dates:dict):
 due = []
 today = datetime.now()
 date = today.strftime("%Y-%m-%d")
 for name in dates:
   if dates[name]["due_date"]<= date:
     due.append(name)  
 if due == []:
   return None , 0
 else:
   return  min(due,key=lambda n: dates[n]["due_date"]) , len(due)


next_due(recorded)
lazy_generator(recorded)
