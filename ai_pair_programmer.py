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
    Returns a generator that yields streamed responses.
    """
    try:
        stream = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                *conversation_history
            ],
            stream=True,
        )
        for chunk in stream:
            yield chunk
    except Exception as e:
        yield f"An error occurred: {str(e)}"

# The main() function has been removed as it's no longer needed in this file.
# The ai_pair_programmer function will be called from the manager_agent.py file.
