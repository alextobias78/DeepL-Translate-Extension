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
    # Define the payload to cache the system prompt
    payload = {
        "model": "claude-3-5-sonnet-20240620",
        "max_tokens": 8000,
        "system": {
            "type": "text",
            "text": system_prompt,
            "cache_control": {"type": "ephemeral"}
        },
        "messages": [{"role": "system", "content": system_prompt}]
    }
    
    # Make the API request to cache the system prompt
    response = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=8000,
        system={
            "type": "text",
            "text": system_prompt,
            "cache_control": {"type": "ephemeral"}
        },
        messages=[{"role": "system", "content": system_prompt}]
    )
    return response.get("cache_id")

def send_request(question, cache_id):
    # Define the payload with the cached system prompt and user question
    payload = {
        "model": "claude-3-5-sonnet-20240620",
        "max_tokens": 8000,
        "cache_id": cache_id,
        "messages": [{"role": "user", "content": question}]
    }
    
    # Make the API request
    response = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=8000,
        cache_id=cache_id,
        messages=[{"role": "user", "content": question}]
    )
    return response

def handle_response(response, payload):
    output = response.get("choices", [])[0].get("text", "")
    confidence_score = extract_confidence_score(output)
    
    if confidence_score < 95:
        # Re-prompt the assistant to think twice
        payload["messages"].append({
            "role": "user",
            "content": "Think twice and provide a more confident solution."
        })
        response = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=8000,
            cache_id=payload["cache_id"],
            messages=payload["messages"]
        )
        output = response.get("choices", [])[0].get("text", "")
    
    return output

def extract_confidence_score(output):
    # Extract the confidence score from the assistant's output
    lines = output.split("\n")
    for line in lines:
        if "Confidence Score" in line:
            return int(line.split(":")[1].strip().replace("%", ""))
    return 0

if __name__ == "__main__":
    # Cache the system prompt and get the cache ID
    cache_id = cache_system_prompt()
    
    question = input("Enter your question: ")
    response = send_request(question, cache_id)
    output = handle_response(response, {"cache_id": cache_id, "messages": [{"role": "user", "content": question}]})
    print(output)