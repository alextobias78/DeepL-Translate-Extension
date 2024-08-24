from openai import OpenAI
import os
from dotenv import load_dotenv
from ai_pair_programmer import ai_pair_programmer

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client
client = OpenAI()

MANAGER_SYSTEM_PROMPT = """You are a project manager with 15 years of experience in software development. Your role is to interpret user requests, break them down into specific coding tasks, and communicate these tasks to a senior developer (the AI pair programmer).

<responses>
- Analyze the user's request and break it down into specific, actionable coding tasks.
- Prioritize tasks based on their importance and dependencies.
- Communicate each task clearly and concisely to the AI pair programmer.
- Review the AI pair programmer's responses and provide feedback or additional instructions if necessary.
- Summarize the overall progress and next steps for the user.
- Always communicate with the AI pair programmer as if you are the user, using "I" statements.
</responses>"""

def manager_agent(user_input):
    """
    Function to interact with the GPT-4 model as a manager agent.
    It interprets user requests and generates tasks for the AI pair programmer.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": MANAGER_SYSTEM_PROMPT},
                {"role": "user", "content": user_input}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {str(e)}"

def main():
    print("Welcome to the AI Project Manager!")
    print("Type 'exit' to quit the program.")
    
    conversation_history = []
    
    while True:
        user_input = input("\nEnter your project request or question: ")
        if user_input.lower() == 'exit':
            break
        
        print("\nManager Agent processing...")
        manager_response = manager_agent(user_input)
        
        print("\nManager's instructions to AI Pair Programmer:")
        print(manager_response)
        
        conversation_history.append({"role": "user", "content": manager_response})
        
        print("\nAI Pair Programmer response:")
        full_response = ""
        for chunk in ai_pair_programmer(conversation_history):
            if isinstance(chunk, str):  # Error message
                print(chunk)
                break
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                print(content, end="", flush=True)
                full_response += content
        print()  # New line after the complete response
        
        if full_response:
            conversation_history.append({"role": "assistant", "content": full_response})
        
        print("\nManager Agent reviewing...")
        manager_review = manager_agent(f"Review this AI Pair Programmer response and provide feedback or next steps:\n{full_response}")
        print("\nManager's feedback and next steps:")
        print(manager_review)

if __name__ == "__main__":
    main()
