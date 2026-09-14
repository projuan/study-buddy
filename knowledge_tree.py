from pydantic import BaseModel
import anthropic
from dotenv import load_dotenv
import os

load_dotenv()
class Leaf(BaseModel):
    name: str
    description: str

class Branch(BaseModel):
    name: str
    leaf: list[Leaf]  


class KnowledgeTree(BaseModel):
    subject: str
    branch : list[Branch]


_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
MODEL = "claude-opus-4-8"
def extract_knowledge_tree(notes:str) -> KnowledgeTree:
    response= _client.messages.parse(
        model=MODEL,
        max_tokens=1024,
        messages=[{"role":"user" , "content":f"extract a  trunk/branch/leaf knowledge tree from these notes -> {notes}"}],
        output_format=KnowledgeTree
    )
    return response.parsed_output