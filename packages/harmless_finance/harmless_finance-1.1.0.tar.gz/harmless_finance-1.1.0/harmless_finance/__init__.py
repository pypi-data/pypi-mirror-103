import os
from pathlib import Path

def setup():
    # Check current working directory.
    original_working_directory = os.getcwd()
    
    # Define new working directory and downloads folder.
    home_folder = str(Path.home())
    working_directory = os.path.join(home_folder, 'HarmlessFinance')
    downloads_folder = os.path.join(working_directory, 'Downloads') 
    
    # Create new working directory and downloads folder.
    print(f'Setting up directory: {working_directory}')
    print('Proceed (y/n)?')
    proceed = input()
    if proceed.lower() == 'y':
        try:
            os.mkdir(working_directory)
            os.mkdir(downloads_folder)
            print(f'Directory created successfully: {working_directory}')
        except:
            pass       
        # Change the directory.
        os.chdir(working_directory)
    else:
        working_directory = original_working_directory
        downloads_folder = str(os.path.join(home_folder, "Downloads"))
    
    print(f'Original working directory: {original_working_directory}')        
    print(f'Current working directory: {working_directory}')
    print(f'Downloads folder: {downloads_folder}')
    return original_working_directory, working_directory, downloads_folder