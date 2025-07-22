import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    dir_abs = os.path.abspath(working_directory)
    file_abs = os.path.abspath(os.path.join(working_directory,file_path))

    if not file_abs.startswith(dir_abs):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(file_abs):
        return f'Error: File "{file_path}" not found.'

    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        result = subprocess.run(['python', file_path, *args], timeout=30, capture_output=True, cwd=dir_abs, text=True)

    except Exception as e:
        return f'Error: executing Python file: {e}'

    if result.returncode == 0 and result.stdout == "" and result.stderr == "":
        return "No output produced"

    result_list = []
    
    if result.stdout != "":
        result_list.append(f"STDOUT: {result.stdout.strip()}")

    if result.stderr != "":
        result_list.append(f"STDERR: {result.stderr.strip()}")
    
    if result.returncode != 0:
        result_list.append(f"Process exited with code {result.returncode}")
        
    return "\n".join(result_list)
        


