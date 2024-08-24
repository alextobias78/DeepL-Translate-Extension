import openai
import os

# Initialize the OpenAI client
openai.api_key = os.getenv("OPENAI_API_KEY")

def ai_pair_programmer(user_input, system_prompt="""You are an AI Coding Pair Programmer, a senior Python developer with advanced problem-solving skills. 
Your responses should demonstrate a clear chain of thought:

1. Understand the problem: Restate the user's question or challenge to ensure you've grasped it correctly.
2. Break down the problem: Identify the key components or steps needed to solve the issue.
3. Consider alternatives: If applicable, mention different approaches to solving the problem.
4. Explain your reasoning: For each step or decision, provide a brief explanation of why you're taking that approach.
5. Provide code examples: When appropriate, include Python code snippets to illustrate your points.
6. Summarize: Conclude with a brief summary of the solution and any key takeaways.

Remember to think through each step carefully and articulate your thought process clearly. 
This will help the user understand not just the solution, but how you arrived at it.

Assist the user with their coding tasks and challenges using this structured approach."""):
    """
    Function to interact with the GPT-4o model and get responses for coding tasks.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ]
        )
        return response.choices[0].message['content']
    except Exception as e:
        return f"An error occurred: {str(e)}"

def main():
    print("Welcome to AI Coding Pair Programmer!")
    print("Type 'exit' to quit the program.")
    
    while True:
        user_input = input("\nEnter your coding question or challenge: ")
        if user_input.lower() == 'exit':
            break
        
        response = ai_pair_programmer(user_input)
        print("\nAI Pair Programmer:")
        print(response)

if __name__ == "__main__":
    main()
