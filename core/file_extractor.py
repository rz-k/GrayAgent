
from openai import AsyncOpenAI


FILE_PATH_SCHEMA = {
    "name": "file_paths",
    "description": "Extract list of file paths that should be generated for the application.",
    "parameters": {
        "type": "object",
        "properties": {
            "files": {
                "type": "array",
                "description": "List of file paths the app will need.",
                "items": {"type": "string"},
            },
        },
        "required": ["files"],
    },
}

async def extract_file_paths(client: AsyncOpenAI ,prompt: str, plan: str, model="gpt-4"):
    """
    Asynchronously extracts a minimal list of required file paths for the app based on the prompt and plan.

    This function sends a request to the OpenAI API with function calling enabled, using a structured plan and 
    prompt to request the most essential files for the application. The model is expected to respond with a 
    structured list of file paths that are necessary to implement the described application.

    Args:
        prompt (str): A high-level description of the application to be built.
        plan (str): A breakdown of the application's structure and architecture.
        model (str, optional): The OpenAI model to use for extracting file paths. Defaults to "gpt-4".

    Returns:
        str: A JSON string containing the structured arguments returned by the model's function call,
             typically representing a minimal list of file paths.

    Notes:
        - The function uses OpenAI's function calling feature, targeting the `file_paths` function schema.
        - It ensures unnecessary files are excluded from the output.
        - You may need to parse the returned JSON string (`response.choices[0].message.function_call.arguments`) 
          into a Python object using `json.loads()` if needed for further processing.

    Raises:
        openai.OpenAIError: If the OpenAI API request fails or the API key is not configured.
    """
    
    response = await client.chat.completions.create(
        model=model,
        temperature=0,
        functions=[FILE_PATH_SCHEMA],
        function_call={"name": "file_paths"},
        messages=[
            {
                "role": "system",
                "content": "You extract a minimal and necessary list of files based on the app prompt and the architecture plan. Avoid unnecessary files."
            },
            {
                "role": "user", 
                "content": f"Prompt:\n{prompt}"
            },
            {
                "role": "user", 
                "content": f"Plan:\n{plan}"
            }
        ]
    )

    return response.choices[0].message.function_call.arguments
