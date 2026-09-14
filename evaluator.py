from pydantic import BaseModel
import anthropic
import os
from dotenv import load_dotenv
from knowledge_tree import Leaf
from quiz import quiz
load_dotenv()
_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
MODEL = "claude-opus-4-8"

class Grade(BaseModel):
    score: int
    feedback: str

def evaluator(leaf:Leaf, question:str, answer:str) -> Grade:
    message= _client.messages.parse(
         model=MODEL,
         max_tokens=1024,
         messages=[{"role":"user" , "content":f"Grade the {answer} based on the {leaf} and {question} provide a score and a feedback"}],
         output_format=Grade
    )    
    return message.parsed_output


new_leaf = Leaf(name="loops" , description="A loop is a programming control flow structure that repeatedly executes a specific block of code as long as a specified condition is met. Instead of manually writing the same instructions over and over again, a loop allows you to write the code once and instruct the computer to run it multiple times, keeping your code clean and efficient.")
new_question = quiz(new_leaf)
new_answer = "a loop is the way we can make something repeat itself multiple times"
graded = evaluator(new_leaf,new_question,new_answer)
print(graded)
