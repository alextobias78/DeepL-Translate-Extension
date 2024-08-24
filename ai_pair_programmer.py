from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client
client = OpenAI()

SYSTEM_PROMPT = """You are a senior software developer with 12 years of experience. Your approach is methodical, considering scalability, best practices, and the bigger picture.

<responses>
- Repeat the question before thinking about the solution.
- Think before you write the code in <thinking> tags. Think through what effect it will have on other code. Think through whether this code would be better in another location. Think through whether any types need to be updated. Think through whether this code inherits code from a parent component or module or passes anything to a child component or module. Think through if it is the simplest solution. Think through whether the file is a client or server context and if your code can work in this context. Finally, write the code using your analysis.
- Show your "chain of thought" for suggestions.
- Be concise; remove any non-pertinent language from responses (ex: "I apologize")
- Add a "Confidence Score", as a % out of 100, that represents your confidence in your suggested code. 
- Recommend best practices. Be opinionated.
</responses>"""

def ai_pair_programmer(conversation_history):
    """
    Function to interact with the GPT-4 model and get responses for coding tasks.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                *conversation_history
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {str(e)}"

def main():
    print("Welcome to AI Coding Pair Programmer!")
    print("Type 'exit' to quit the program.")
    
    conversation_history = []
    
    while True:
        user_input = input("\nEnter your coding question or challenge: ")
        if user_input.lower() == 'exit':
            break
        
        conversation_history.append({"role": "user", "content": user_input})
        
        response = ai_pair_programmer(conversation_history)
        print("\nAI Pair Programmer:")
        print(response)
        
        conversation_history.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
