 
import os
import difflib

def create_file(file_path, content):
    """
    Create a new file with the given content.
    
    :param file_path: The path where the file should be created
    :param content: The content to write in the file
    :return: True if successful, False otherwise
    """
    try:
        with open(file_path, 'w') as file:
            file.write(content)
        return True
    except Exception as e:
        print(f"Error creating file: {e}")
        return False

def read_file(file_path):
    """
    Read the content of a file.
    
    :param file_path: The path of the file to read
    :return: The content of the file as a string, or None if an error occurs
    """
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def edit_file(file_path, new_content):
    """
    Edit a file and return the diff.
    
    :param file_path: The path of the file to edit
    :param new_content: The new content to write in the file
    :return: A tuple (success, diff) where success is a boolean and diff is a string
    """
    try:
        # Read the original content
        with open(file_path, 'r') as file:
            original_content = file.read()

        # Write the new content
        with open(file_path, 'w') as file:
            file.write(new_content)

        # Generate the diff
        diff = difflib.unified_diff(
            original_content.splitlines(keepends=True),
            new_content.splitlines(keepends=True),
            fromfile=file_path,
            tofile=f"{file_path} (edited)",
            lineterm=''
        )

        return True, ''.join(diff)
    except Exception as e:
        print(f"Error editing file: {e}")
        return False, str(e)
