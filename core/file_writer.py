import os


def save_code_to_file(base_dir: str, path: str, code: str):
    """
    Saves the given code string to a file at the specified path within the base directory.

    This function ensures that the necessary directories exist before writing the code to the file.
    If the target directories do not exist, they will be created automatically. The written code
    is stripped of any leading or trailing whitespace.

    Args:
        base_dir (str): The root directory where the file should be saved.
        path (str): The relative file path (from base_dir) where the code should be saved.
        code (str): The source code to write into the file.

    Returns:
        None

    Notes:
        - Directories in the provided path are created if they don't exist.
        - The file is written with UTF-8 encoding.
        - The code content is stripped before writing to remove unnecessary whitespace.

    Raises:
        OSError: If there is an error creating directories or writing to the file.
    """
    
    full_path = os.path.join(base_dir, path)
    dir_name = os.path.dirname(full_path)

    if dir_name:
        os.makedirs(dir_name, exist_ok=True)

    with open(full_path, "w", encoding="utf-8") as f:
        f.write(code.strip())
