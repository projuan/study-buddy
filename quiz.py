from claude_client import ask_claude
from knowledge_tree import Leaf

def quiz(leaf:Leaf):
    prompt = (
        f"Generate one open-ended quiz question based on this concept:\n"
        f"{leaf.name}: {leaf.description}\n\n"
        "Return only the question itself as plain text. No markdown, no "
        "asterisks, no headings, no 'Question:' label, no answer."
    )
    response = ask_claude(prompt, system="you are a quiz generator assistant")
    return response




