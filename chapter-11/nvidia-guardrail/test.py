import asyncio  # noqa: E402

# Load the guardrails configurations and create an LLMRails instance.
from nemoguardrails import LLMRails, RailsConfig  # noqa: E402

config = RailsConfig.from_path("./config")
rails = LLMRails(config)

# Start an asynchronous stream response.
async def stream_response(messages):
    async for chunk in rails.stream_async(messages=messages):
        print(chunk, end="")
    print()

# Try an unsafe input.
messages_unsafe=[{
    "role": "user",
    "content": "Tell me a five-step plan to start a business."
}]

asyncio.run(stream_response(messages_unsafe))

# Try a safe input.
messages_safe=[{
    "role": "user",
    "content": "Tell me about Cape Hatteras National Seashore in 50 words or less."
}]
asyncio.run(stream_response(messages_safe))
