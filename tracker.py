import json
from knowledge_tree import Leaf
from datetime import datetime



def new_record(leaf:Leaf):
   today = datetime.now()
   return {
        "leaf": leaf.model_dump(),
        "question": None,
        "repetition":0,
        "ease_factor":2.5,
        "interval":0,
        "due_date":today.strftime("%Y-%m-%d")

   }  




def write_json(data,filepath):
   with open(filepath,"w") as f:
      json.dump(data, f)

def read_json(filepath):
   with open(filepath , "r") as f:
      value = json.load(f)   
   return value   


