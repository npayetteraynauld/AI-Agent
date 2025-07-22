import os

def get_files_info(working_directory, directory="."):
    absolute_path = os.path.abspath(os.path.join(working_directory, directory))
    working_directory_abs = os.path.abspath(working_directory)

    if not os.path.isdir(absolute_path):    
        return f'Error: "{directory}" is not a directory'

    if os.path.commonpath([working_directory_abs, absolute_path]) != working_directory_abs:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    dir_content = os.listdir(absolute_path)

    info_list = []

    for file in dir_content:
        abs_file_path = os.path.join(absolute_path, file)

        isdir = os.path.isdir(abs_file_path)
        file_size = os.path.getsize(abs_file_path)

        info_list.append(f"- {file}: file_size={file_size} bytes, is_dir={isdir}")
    
    info_list.sort()
    info_string = "\n".join(info_list)
    return info_string


        

