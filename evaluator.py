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


