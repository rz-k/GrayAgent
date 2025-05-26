import os
import json

from core.planner import generate_plan_stream
from core.file_extractor import extract_file_paths
from core.code_generator import generate_code_for_file
from core.file_writer import save_code_to_file
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


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
    
    delete_old_files(base_output_dir)
    logger.info(f"Delete old files in {base_output_dir}...")

    logger.info("\n🔧 Generating plan...\n")
    os.makedirs(base_output_dir, exist_ok=True)    
    plan = await generate_plan_stream(prompt, model=model)

    save_plan_to_file(plan)

    logger.info("\n📁 Extracting file paths...")
    file_json = await extract_file_paths(prompt, plan, model=model)
    file_paths = json.loads(file_json)["files"]
    logger.info("📄 Files to generate: %s", file_paths)

    for file_path in file_paths:
        logger.info(f"\n✍️ Generating code for: {file_path}")
        code = await generate_code_for_file(prompt, plan, file_path, model=model)

        save_code_to_file(base_output_dir, file_path, code)    
        logger.info(f"✅ Saved: {os.path.join(base_output_dir, file_path)}")

prompt = "Create login/register page using HTML, CSS, and JavaScript."

if __name__ == "__main__":
    import asyncio
    asyncio.run(main(prompt=prompt))
