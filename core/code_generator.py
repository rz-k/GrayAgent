import re
from openai import AsyncOpenAI
from .prompts import PROMPT


async def generate_code_for_file(client: AsyncOpenAI, prompt: str, plan: str, file_path: str, model="gpt-4"):
    """
    Asynchronously generates code for a specific file using the OpenAI chat completion API.

    This function sends a structured multi-message prompt to the OpenAI API, instructing it to
    generate valid source code for a specific file (`file_path`) based on an overall app prompt
    and a pre-defined plan. It ensures the model returns only the code (without markdown fences or explanations).

    Args:
        prompt (str): A high-level description of the application to be built.
        plan (str): A breakdown of the application structure, including which files to generate and what they contain.
        file_path (str): The path to the file for which the code should be generated (used to guide the model).
        model (str, optional): The OpenAI model to use for code generation. Defaults to "gpt-4".

    Returns:
        str: The generated code as a plain string, without any markdown formatting or explanations.

    Notes:
        - The function ensures the response only contains valid code for the specified file type.
        - If the response contains code blocks enclosed in markdown (```), they are stripped.
        - If no markdown code block is found, the full message content is returned as-is.

    Raises:
        openai.OpenAIError: If the OpenAI API request fails or the key is not set properly.
    """
    
    response = await client.chat.completions.create(
        model=model,
        temperature=0.7,
        messages=[
            {
                "role": "system",
                "content": PROMPT['GRAY_CODE_GENERATOR_SYSTEM_PROMPT'].format(file_path=file_path)
            },
            {
                "role": "user",
                "content": f""" the plan we have agreed on is: {plan} """,
            },
            {
                "role": "user", 
                "content": f""" the app prompt is: {prompt} """
            },
            {
                "role": "user", 
                "content": PROMPT['GRAY_CODE_GENERATOR_SYSTEM_PROMPT_FILE'].format(file_path=file_path)
            }
        ]
    )
    code = response.choices[0].message.content.strip()
    pattern = r"```[\w\s]*\n([\s\S]*?)```"
    code_blocks = re.findall(pattern, code, re.MULTILINE)
    
    return code_blocks[0] if code_blocks else code
