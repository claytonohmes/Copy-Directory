import os
import shutil

def copy_directory_contents(source_dir, dest_dir):
    # Ensure the source directory exists
    if not os.path.isdir(source_dir):
        print(f"Source directory '{source_dir}' does not exist.")
        return
    
    # Ensure the destination directory exists; create it if it doesn't
    if not os.path.isdir(dest_dir):
        os.makedirs(dest_dir)
    
    # Walk through the source directory
    for root, dirs, files in os.walk(source_dir):
        # Calculate the relative path from the source directory
        rel_path = os.path.relpath(root, source_dir)
        # Create the corresponding path in the destination directory
        dest_path = os.path.join(dest_dir, rel_path)
        
        # Ensure the destination subdirectories exist
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)
        
        # Copy all files in the current directory
        for file in files:
            src_file = os.path.join(root, file)
            dst_file = os.path.join(dest_path, file)
            shutil.copy2(src_file, dst_file)
            #print(f"Copied '{src_file}' to '{dst_file}'")

if __name__ == "__main__":
    # Get user input for source and destination directories
    source_directory = 'C:\\Scripts\\Atlanta West File Copy\\Server1'
    destination_directory = 'C:\\Scripts\\Atlanta West File Copy\\Server2'
    
    # Copy contents from source to destination
    copy_directory_contents(source_directory, destination_directory)
