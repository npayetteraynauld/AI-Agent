import os

def write_file(working_directory, file_path, content):
    dir_abs = os.path.abspath(working_directory)
    file_abs = os.path.abspath(os.path.join(working_directory,file_path))

    try:
        if not os.path.commonpath([file_abs, dir_abs]) == dir_abs:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        dir_of_file = os.path.dirname(file_abs)
        os.makedirs(dir_of_file, exist_ok=True)

        with open(file_abs, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except Exception as e:
        return f"Error: {str(e)}"
