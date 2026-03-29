import re
import os
import ollama

class Agent:
    def __init__(self, system=''):   
        self.system=system
        self.messages=[]
        if self.system:
            self.messages.append({'role':'system', 'content':system})

    def __call__(self, message):
        self.messages.append({'role':'user', 'content': message})
        result=self.execute()
        self.messages.append({'role':'assistant', 'content':result})
        return result
    
    def execute(self):
        response = ollama.chat(
            model='qwen2.5:7b',
            messages=self.messages,
        )
        return response['message']['content']
        
prompt="""You are a Socratic quiz agent testing a student on agentic AI concepts.

For every student turn, you must follow this exact sequence:
1. Thought — reason about the quality of their answer out loud
2. Action — call exactly one tool
3. Observe the result
4. Repeat until you decide to speak to the student

Always show your Thought/Action/Observation to the student — this is intentional.
They are learning the ReAct pattern by watching you execute it.

## Tools available
- get_question(concept) — get the next question for a concept
- evaluate_answer(question, user_answer, model_answer) — returns score 0–1 and what was missing
- get_probe(concept) — returns a follow-up if the answer was shallow
- advance() — mark current concept done and move to next

## Concepts to cover (in order)
1. Agent vs chain
2. ReAct pattern
3. Tool calling
4. Why agents fail — infinite loops, hallucinated tool calls, context overflow

## Scoring rules
- Score >= 0.8 → praise briefly, call advance()
- Score 0.5–0.79 → call get_probe(), push for the missing piece
- Score < 0.5 → give a hint in plain language, re-ask the same question

## Hard limits
- Maximum 6 iterations per question. If you hit 6, give the model answer and move on.
  Print "⚠ max iterations reached" so the student sees the guard trip.
- Never skip the Thought step. Reasoning before acting is the whole point.
- Never call a tool that isn't in your tools list. If you're tempted to, output
  "⚠ hallucinated tool call caught" and recover by calling evaluate_answer instead.

## Tone
Socratic, not lecturing. Ask, don't tell. When the student is close, reflect
their answer back with a gap: "You've got X — what about Y?""".strip()
    

def get_question(message:str)->str:
    _system_prompt="You are a helpful assistant for a student learning about agentic AI."
    _user_prompt=f"The student's message:\n{message}"
    response=ollama.chat(
        model='qwen2.5:7b',
        messages=[
            {"role": "system", "content": _system_prompt},
            {"role": "user", "content": _user_prompt}
        ]
    )
    return response['message']['content']

def evaluate_answer(answer: str) -> str:
    _system_prompt = "Evaluate the student's answer and give a score between 0 and 1 with feedback."
    _user_prompt = f"The student's answer:\n{answer}"

    response = ollama.chat(
        model='qwen2.5:7b',
        messages=[
            {"role": "system", "content": _system_prompt},
            {"role": "user", "content": _user_prompt}
        ]
    )

    return response['message']['content'].strip()

def get_probe(question: str) -> str:
    _system_prompt:str=""""Generate a probing follow-up question to push the student to think deeper about what they just answered."""
    _user_prompt:str=f"""The student's question:\n{question}"""
    response = ollama.chat(
        model='qwen2.5:7b',
        messages=[{"role": "system", "content": _system_prompt}, {"role": "user", "content": _user_prompt}],
    )
    return response['message']['content'].strip()

def advance(message: str):
    """Mark the current concept as done and move to the next one."""
    _system_prompt:str="""Move onto the next concept."""
    _user_prompt:str=f"""The student's message:\n{message}"""
    response = ollama.chat(
        messages=[{"role": "system", "content": _system_prompt}, {"role": "user", "content": _user_prompt}],
        )
    return response['message']['content'].strip()

known_actions={
    'get_question': get_question,
    'evaluate_answer': evaluate_answer,
    'get_probe': get_probe,
    'advance': advance
    }

actions_re = re.compile(r'Action:\s*(\w+)\((.*?)\)|Action:\s*(\w+):\s*(.*)')

modi=Agent(prompt)

def run_agent(question):
    next_prompt=question
    iterations=0
    while iterations<=5:
        result=modi(next_prompt)
        print(result)
        iterations+=1
        match=actions_re.search(result)
        if not match:
            break
        action_name=match.group(1) or match.group(3)
        action_input=match.group(2) or match.group(4)
        if action_name not in known_actions:
            print("⚠ hallucinated tool call caught")
            next_prompt=f"Observation: tool '{action_name}' does not exist."
            continue
        observation=known_actions[action_name](action_input)
        print(f"\nObservation: {observation}\n")
        next_prompt=f"Observation: {observation}"
    if iterations==6:
        print("⚠ max iterations reached")

if __name__=="__main__":
    modi=Agent(prompt)
    while True:
        user_input=input("You: ")
        if user_input.lower()=="exit":
            break
        run_agent(user_input)