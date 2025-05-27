import os
import json
import logging

from core.planner import generate_plan_stream
from core.file_extractor import extract_file_paths
from core.code_generator import generate_code_for_file
from core.file_writer import save_code_to_file

from openai import AsyncOpenAI
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
load_dotenv()



def save_plan_to_file(plan: str):
    """
    Save the given plan string to a Markdown file named 'plan.md' inside the 'logs' directory.

    Args:
        plan (str): The content of the plan to be saved.
    """

    log_dir: str= "logs"
    os.makedirs(log_dir, exist_ok=True)
    with open(os.path.join(log_dir, "plan.md"), "w", encoding="utf-8") as f:
        f.write(plan)

def delete_old_files(base_output_dir: str = "generated"):
    """
    Delete all files and folders inside the specified output directory.

    Args:
        base_output_dir (str): The directory whose contents will be deleted. Defaults to 'generated'.
    """

    os.system(f"rm -rf {base_output_dir}/*")

async def main(prompt: str, base_output_dir: str = "generated", model: str = "gpt-4"):

    client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    delete_old_files(base_output_dir)
    logger.info(f"Delete old files in {base_output_dir}...")

    logger.info("\n🔧 Generating plan...\n")
    os.makedirs(base_output_dir, exist_ok=True)    
    plan = await generate_plan_stream(client=client, prompt=prompt, model=model)

    save_plan_to_file(plan)

    logger.info("\n📁 Extracting file paths...")
    file_json = await extract_file_paths(client, prompt, plan, model=model)
    file_paths = json.loads(file_json)["files"]
    logger.info("📄 Files to generate: %s", file_paths)

    for file_path in file_paths:
        logger.info(f"\n✍️ Generating code for: {file_path}")
        code = await generate_code_for_file(client, prompt, plan, file_path, model=model)

        save_code_to_file(base_output_dir, file_path, code)    
        logger.info(f"✅ Saved: {os.path.join(base_output_dir, file_path)}")

def run_agent_with_prompt(prompt: str, base_output_dir: str = "generated", model: str = "gpt-4"):
    """
    Run the agent with the given prompt and model.
    """
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        # No running loop, safe to create one
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(main(prompt=prompt, base_output_dir=base_output_dir, model=model))
    else:
        # Loop is already running -> create a task inside it
        return asyncio.create_task(main(prompt=prompt, base_output_dir=base_output_dir, model=model))


if __name__ == "__main__":
    import asyncio
    prompt = input("Enter your prompt: ") or None
    if prompt is None:
        prompt = "Create login/register page using HTML, CSS, and JavaScript."
    asyncio.run(main(prompt=prompt))
