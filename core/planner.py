from .prompts import PROMPT
from openai import AsyncOpenAI


async def generate_plan_stream(client: AsyncOpenAI, prompt: str, model="gpt-4") -> str:
    """
    Asynchronously generates a structured plan for code generation using streaming from the OpenAI API.

    This function sends a system prompt and user prompt to the OpenAI API to request a detailed plan 
    (in GitHub Markdown format) for implementing an application based on the given description. 
    The response includes a YAML section describing files to be generated and their internal structure, 
    such as exported variables, function names, data schemas, and DOM element IDs.

    The plan is streamed token by token, and the response is printed live to the console during streaming.

    Args:
        prompt (str): A natural language description of the application to be built.
        model (str, optional): The OpenAI model to use for generating the plan. Defaults to "gpt-4".

    Returns:
        str: The full streamed response content containing the code generation plan.

    Notes:
        - The function uses the `stream=True` mode of the OpenAI API to receive tokens incrementally.
        - The generated plan begins with a YAML summary of file structure and should follow a specific format.
        - Content is printed to the console in real-time during generation.
        - The final return value is the full concatenated plan string.

    Raises:
        openai.OpenAIError: If the API call fails or the API key is not configured.
    """

    stream = await client.chat.completions.create(
        model=model,
        temperature=0.7,
        stream=True,
        messages=[
            {
                "role": "system", 
                "content": PROMPT['GRAY_PLAN_SYSTEM_PROMPT']
            },
            {
                "role": "user", 
                "content": f"The app prompt is: {prompt}"
            },
        ],
    )

    full_reply = ""
    async for chunk in stream:
        delta = chunk.choices[0].delta
        if delta and delta.content:
            full_reply += delta.content
            print(delta.content, end="", flush=True)

    return full_reply