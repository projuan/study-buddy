from claude_client import ask_claude
from knowledge_tree import Leaf

def quiz(leaf:Leaf):
    prompt = f"Generate a quiz question that is open-ended only based on this: {leaf.name}: {leaf.description}"
    response = ask_claude(prompt, system="you are a quiz generator assistant")
    return response




