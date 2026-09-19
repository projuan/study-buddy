from knowledge_tree import *
from ingest import *
from tracker import *
from quiz import quiz
from evaluator import *
from scheduler import *
from datetime import datetime, timedelta
import display
import os
import time

DATA_FILE = "progress.json"


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


def with_retry(action, what):
  """API calls fail transiently. Give each one a second chance, and never let
  one failure take the whole session down."""
  for attempt in (1, 2):
    try:
      return action()
    except Exception as exc:
      if attempt == 1:
        display.thinking(f"{what} failed, retrying...")
        time.sleep(2)
      else:
        display.error(f"{what} failed: {exc}")
        return None


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
   question = with_retry(lambda: quiz(leaf), "question generation")
   if question is None:
     write_json(recorded, DATA_FILE)
     display.goodbye()
     return
   card["question"] = question
   write_json(recorded, DATA_FILE)
   display.show_question(question)
   answer  = read_multiline("Your answer", blanks_needed=1)
   display.thinking("grading...")
   score = with_retry(lambda: evaluator(leaf, question, answer), "grading")
   if score is None:
     write_json(recorded, DATA_FILE)
     display.goodbye()
     return
   new_score = converter(score.score)
   r,e,it = scheduling(new_score,card["repetition"],card["ease_factor"],card["interval"])
   card["repetition"] = r
   card["ease_factor"] = e
   card["interval"] = it 
   new_date = today + timedelta(days=it)
   card["due_date"] = new_date.strftime("%Y-%m-%d")
   write_json(recorded, DATA_FILE)
   display.show_grade(score.score, score.strengths, score.improvements)
   display.show_next_review(it, card["due_date"])

   if display.menu() == "next":
    
     continue
   else:
     display.goodbye()
     return



display.banner()

if os.path.exists(DATA_FILE) and os.path.getsize(DATA_FILE) > 0:
  recorded = read_json(DATA_FILE)
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
