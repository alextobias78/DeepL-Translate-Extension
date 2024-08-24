import openai
import os

# Initialize the OpenAI client
openai.api_key = os.getenv("OPENAI_API_KEY")

def ai_pair_programmer(user_input, system_prompt="You are an AI Coding Pair Programmer. You are a senior Python developer with self-thought and chain of action abilities. Assist the user with their coding tasks and challenges."):
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
