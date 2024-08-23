import anthropic
import json

# Define the system prompt
system_prompt = """
<responses>
- Repeat the question before thinking about the solution.
- Think before you write the code in <thinking> tags. Think through what effect it will have on other code. Think through whether this code would be better in another location. Think through whether any types need to be updated. Think through whether this code inherits code from a parent component or module or passes anything to a child component or module. Think through if it is the simplest solution. Think through whether the file is a client or server context and if your code can work in this context. Finally, write the code using your analysis.
- Show your "chain of thought" for suggestions.
- Be concise; remove any non-pertinent language from responses (ex: "I apologize")
- Add a "Confidence Score", as a % out of 100, that represents your confidence in your suggested code. 
- Recommend best practices. Be opinionated.
</responses>
"""

# Initialize the Anthropic client
client = anthropic.Anthropic(api_key="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")

def cache_system_prompt():
    # Make the API request to cache the system prompt
    response = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=8000,
        system=system_prompt,
        messages=[]
    )
    return response.id

def send_request(question, cache_id):
    # Make the API request
    response = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=8000,
        system=system_prompt,
        messages=[{"role": "user", "content": question}]
    )
    return response

def handle_response(response, question):
    output = response.content[0].text
    confidence_score = extract_confidence_score(output)
    
    if confidence_score < 95:
        # Re-prompt the assistant to think twice
        new_response = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=8000,
            system=system_prompt,
            messages=[
                {"role": "user", "content": question},
                {"role": "assistant", "content": output},
                {"role": "user", "content": "Think twice and provide a more confident solution."}
            ]
        )
        output = new_response.content[0].text
    
    return output

def extract_confidence_score(output):
    # Extract the confidence score from the assistant's output
    lines = output.split("\n")
    for line in lines:
        if "Confidence Score" in line:
            return int(line.split(":")[1].strip().replace("%", ""))
    return 0

if __name__ == "__main__":
    question = input("Enter your question: ")
    response = send_request(question, None)  # We don't need cache_id anymore
    output = handle_response(response, question)
    print(output)
