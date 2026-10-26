import os
import glob
import subprocess

def read_file(file_path: str) -> str:
    """Reads the content of a file or glob pattern within the project workspace."""
    try:
        matched_files = glob.glob(file_path, recursive=True)
        if matched_files:
            target = matched_files[0]
            if os.path.isfile(target):
                with open(target, "r") as f:
                    return f"--- Content of {target} ---\n" + f.read()
        
        if os.path.isfile(file_path):
            with open(file_path, "r") as f:
                return f.read()
        
        return f"Error: Path '{file_path}' not found. Note: Do not use a 'workspace/' prefix. Use relative paths from the current directory (e.g., 'agent_code/filename.py')."
    except Exception as e:
        return f"Error reading file: {e}"

def write_code(file_path: str, content: str) -> str:
    """Writes code or text to a specified file path."""
    try:
        dir_name = os.path.dirname(file_path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        with open(file_path, "w") as f:
            f.write(content)
        return f"Successfully wrote to {file_path}"
    except Exception as e:
        return f"Error writing file: {e}"

def run_shell(command: str) -> str:
    """Executes a safe shell command and returns output or error."""
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            return result.stdout
        else:
            return f"Command failed with stderr:\n{result.stderr}"
    except Exception as e:
        return f"Execution error: {e}"

def run_tests() -> str:
    """Runs pytest or project test suite."""
    return run_shell("pytest")
