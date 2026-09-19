from pydantic import BaseModel
import anthropic
import os
from dotenv import load_dotenv
from knowledge_tree import Leaf
from quiz import quiz
load_dotenv()
_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
MODEL = "claude-opus-5"

class Grade(BaseModel):
    score: int
    strengths: str
    improvements: str

def evaluator(leaf:Leaf, question:str, answer:str) -> Grade:
    # the word limit is load-bearing: unbounded feedback used to run past
    # max_tokens and come back as truncated, unparseable JSON
    prompt = (
        f"Grade this answer.\n\n"
        f"Concept: {leaf.name} - {leaf.description}\n"
        f"Question: {question}\n"
        f"Answer: {answer}\n\n"
        "Score it 0-100. In 'strengths', say what the answer got right. In "
        "'improvements', say what it missed or could state more precisely. "
        "Keep each one under 80 words."
    )
    message= _client.messages.parse(
         model=MODEL,
         max_tokens=4096,
         messages=[{"role":"user" , "content":prompt}],
         output_format=Grade
    )    
    return message.parsed_output


