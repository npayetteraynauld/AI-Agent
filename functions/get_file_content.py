import os
from functions import config

def get_file_content(working_directory, file_path):
    dir_abs = os.path.abspath(working_directory)
    file_abs = os.path.abspath(os.path.join(working_directory,file_path))

    try:
        if not os.path.commonpath([file_abs, dir_abs]) == dir_abs:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(file_abs):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(file_abs, "r") as f:
            correct_string = f.read(config.MAX_CHARS + 1)

            if len(correct_string) > config.MAX_CHARS:
                correct_string = correct_string[:config.MAX_CHARS] + f'[...File "{file_path}" truncated at 10000 characters]'

            return correct_string    
    
    except Exception as e:
        return f"Error: {str(e)}"

    

