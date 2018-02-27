"""
Simple helper functions for File Operations
"""

WRITE_FILE_MODE = 'w'

def save_file(file_name, data):
    """
    Function to save data to a file, overwriting the file if it exists
    """
    file = open(file_name, WRITE_FILE_MODE)
    file.write(data)
    file.close()
