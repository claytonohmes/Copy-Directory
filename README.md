# Batch Ticket Copying Script

Owner: clayton ohmes

# Overview:

[Printing HMI Displays to PDF](https://www.notion.so/Printing-HMI-Displays-to-PDF-fff0c37ffdfc805f84bad9a8e5541727?pvs=21) 

This file copy application is designed to automate the process of copying files between specified directories on different Windows servers at a 1-hour interval. It uses a configuration file (`Config.ini`) to specify the source directories (`TargetPath1` and `TargetPath2`) and a destination directory (`DestPath`). The accompanying Python script (`MoveFiles.py`) reads these paths and performs the file transfer operations every hour to synchronize or back up data from the source directories to the destination directory.

## General Flow:

- script walks the target folder, returns a list of all the files in that folder
- Script walks the destination folder, returns a list of all the files in that folder
- compares the two file lists. Creates a new list of files that ARE NOT in the destination but ARE in the target.
- executes this code every 1 hour
- runs as a windows service, configure this service to start on login.

# Python Script

## Config File

### Configuration Section: `[SERVERS]`

This configuration file is designed to specify the paths used for copying files between different directories located on separate Windows servers.

1. **TargetPath1**
    - `TargetPath1` is set to a directory on **Windows Server 1**. For example, this might be configured as:
        
        ```makefile
        TargetPath1=\\Server1\Shared\SourceFiles
        ```
        
    - This path represents the source directory on **Server 1** from which files will be copied.
2. **TargetPath2**
    - `TargetPath2` is set to a directory on **Windows Server 2**. An example configuration might look like:
        
        ```makefile
        TargetPath2=\\Server2\Shared\IntermediateFiles
        ```
        
    - This path could serve as a secondary source or an intermediate location on **Server 2** from which files may also be copied.
3. **DestPath**
    - `DestPath` is set to the destination directory on **Windows Server 3**. For instance, it might be configured as:
        
        ```makefile
        DestPath=\\Server3\Shared\DestinationFiles
        ```
        
    - This is the network directory on **Server 3** where the files from `TargetPath1` (and potentially `TargetPath2`) will be copied to.

### Overall Function

The configuration specifies three network paths:

- **Source Paths**: Two paths (`TargetPath1` on Server 1 and `TargetPath2` on Server 2) which indicate where the files to be copied are located.
- **Destination Path**: A single path (`DestPath` on Server 3) indicating where the files will be copied to.

## Copy Directory Function

```python
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

#used for testing purposed, only executes if this script is directly run.
if __name__ == "__main__":
    # Get user input for source and destination directories
    source_directory = 'C:\\Scripts\\Atlanta West File Copy\\Server1'
    destination_directory = 'C:\\Scripts\\Atlanta West File Copy\\Server2'
    
    # Copy contents from source to destination
    copy_directory_contents(source_directory, destination_directory)
```

### `copy_directory_contents` Function

### Purpose

The `copy_directory_contents` function is designed to recursively copy all files and subdirectories from a specified source directory to a specified destination directory. It preserves the directory structure and file attributes during the copy process.

### Parameters

- **`source_dir`**: A string representing the path of the source directory whose contents need to be copied.
- **`dest_dir`**: A string representing the path of the destination directory where the contents will be copied to.

### Functionality

1. **Check Source Directory**:
    - The function first checks whether the `source_dir` exists and is a directory. If it does not exist, the function prints an error message and returns, terminating further execution.
2. **Create Destination Directory**:
    - If the `dest_dir` does not exist, the function creates it. This is to ensure that the destination directory is available for copying the contents.
3. **Traverse Source Directory**:
    - Using `os.walk()`, the function recursively traverses the `source_dir`. This method yields a tuple for each directory in the tree, including the directory path (`root`), the contained subdirectories (`dirs`), and the contained files (`files`).
4. **Calculate Relative Paths**:
    - For each directory visited, the function calculates its relative path from the `source_dir`. This relative path is then used to determine the corresponding path in the `dest_dir`.
5. **Create Destination Subdirectories**:
    - The function ensures that the corresponding subdirectories exist in the `dest_dir`. If they do not exist, they are created to match the structure of the `source_dir`.
6. **Copy Files**:
    - For each file in the current directory, the function constructs the full paths for both the source file and the destination file. It then copies the file from the `source_dir` to the `dest_dir`, preserving the file’s metadata (e.g., modification time) using `shutil.copy2()`.
7. **Logging**:
    - As files are copied, the function prints messages indicating the source and destination paths of each copied file. This helps in tracking the progress and verifying that files are being copied correctly.

### Example Usage

To use this function, you would call it with the paths of the source and destination directories. For example:

```python
copy_directory_contents('C:\\\\path\\\\to\\\\source', 'D:\\\\path\\\\to\\\\destination')

```

This call would copy all files and subdirectories from `C:\\\\path\\\\to\\\\source` to `D:\\\\path\\\\to\\\\destination`, preserving the original directory structure and file attributes.

### Summary

The `copy_directory_contents` function provides a comprehensive solution for copying an entire directory structure from one location to another. It handles creating necessary directories, copying files while preserving their attributes, and provides feedback during the copying process. This makes it useful for tasks such as backups or data migrations.

## Main Script (MoveFiles.py)

```python
import configparser,schedule,time
from CopyDirectoryFunction import copy_directory_contents

#Define the location of the config file and set it to a variable.
ConfigLocation = 'C:\\Users\\cohmes\\Documents\\GitHub\\Copy-Directory\\'
config = configparser.ConfigParser()
config.read(ConfigLocation + 'Config.ini')

#Get the Target and destination folder paths from the config file.
TargetPath1 = config['SERVERS']['TargetPath1']
TargetPath2 = config['SERVERS']['TargetPath2']
DestinationPath1 = config['SERVERS']['DestPath']

#Copy each target path every 30 seconds.
schedule.every(1).hours.do(copy_directory_contents,TargetPath1,DestinationPath1)
schedule.every(1).hours.do(copy_directory_contents,TargetPath2,DestinationPath1)

while True:
    schedule.run_pending()
    #print('Waiting....')
    time.sleep(60)
```

This script periodically copies the contents of a source directory to a destination directory based on paths specified in a configuration file. The copying process is executed every 30 seconds, and the script continuously runs to ensure the scheduled tasks are carried out. The configuration file must be properly set up with the correct paths for the script to function as intended. The custom error class is available for potential use in error handling, though it's not utilized in the provided code snippet.

- **Configuration Reading**:
    - The script starts by importing necessary modules: `configparser` for reading configuration files, `schedule` for scheduling periodic tasks, and `time` for managing time-related operations.
    - It defines the location of the configuration file (`Config.ini`) and reads this file using the `configparser` module. The configuration file is expected to be located at `'INSERT FILE PATH HERE'`.
- **Extracting Paths**:
    - From the configuration file, the script retrieves two key paths:
        - `TargetPath1`: The path of the source directory whose contents are to be copied.
        - `TargetPath2`: The path of the second source directory whose contents are to be copied (OPTIONAL)
        - `DestinationPath1`: The path of the destination directory where the contents will be copied to.
    - These paths are extracted from the `SERVERS` section of the configuration file.
- **Scheduling the Copy Operation**:
    - The script schedules a periodic task to execute the `copy_directory_contents` function, which is imported from an external module (`CopyDirectoryFunction`). The function is scheduled to run every 30 seconds.
    - The `copy_directory_contents` function will use `TargetPath1` and `DestinationPath1` as arguments to perform the copy operation.
- **Running the Scheduled Task**:
    - The script enters an infinite loop where it continuously checks for any pending scheduled tasks.
    - The `schedule.run_pending()` function is called to run any tasks that are due.
    - The script sleeps for 10 seconds between checks to avoid excessive CPU usage.

# NSSM

## What is NSSM?

NSSM (Non-Sucking Service Manager) is a tool for managing Windows services. Unlike the default Windows Service Manager, NSSM allows you to run any executable, including console programs, as a Windows service. This makes it ideal for keeping applications running continuously in the background, such as servers, scripts, or monitoring tools, ensuring they restart automatically in the event of a crash or reboot.

## Guide to Setting Up a Service with NSSM

Follow these steps to set up a service using NSSM:

1. **Download and Install NSSM:**
    - Visit the NSSM website and download the latest version of NSSM for your system architecture (32-bit or 64-bit).
    - Extract the downloaded ZIP file to a directory of your choice (e.g., `C:\nssm`).
2. **Open Command Prompt as Administrator:**
    - Press `Win + X` and select **Command Prompt (Admin)** or **Windows PowerShell (Admin)** to open a command prompt with administrative privileges.
3. **Navigate to the NSSM Directory:**
    - Change the directory to where you extracted NSSM. For example:
    
    ```bash
    cd C:\nssm\win64
    
    ```
    
4. **Install a New Service:**
    - Use the following command to install a new service:
    
    ```bash
    nssm install <ServiceName>
    ```
    
    Replace `<ServiceName>` with your desired name for the service (e.g., `MyAppService`).
    
5. **Configure the Service:**
    - A GUI window will open for configuring the service. Fill in the following fields:
        - **Path:** The full path to the executable or script you want to run as a service (e.g., `C:\python3\python.exe`).
        - you can find where your python is installed by opening CMD and putting this command in:
        
        ```bash
        python -c "import os, sys; print(os.path.dirname(sys.executable))
        ```
        
        - **Startup directory:** The directory where your executable or script resides.
        - **Startup directory:** The directory where your executable or script resides.
        - **Arguments:** `C:\FullPathToScript\MoveFiles.py`
    - You can also configure other options like the service’s **startup type** (automatic, manual, etc.), **I/O redirection** to log output, and **environment variables**.
6. **Save the Configuration and Start the Service:**
    - Click **Install service** to save your configuration and create the service.
    - Start the service immediately by running:
    
    ```bash
    nssm start <ServiceName>
    ```
    
7. **Verify the Service is Running:**
    - Open the **Services** management console by pressing `Win + R`, typing `services.msc`, and pressing `Enter`.
    - Look for your service (`MyAppService`) in the list and verify that its status is **Running**.
8. **Manage the Service:**
    - To stop, start, or restart the service, use the following commands:
    
    ```bash
    nssm stop <ServiceName>
    nssm start <ServiceName>
    nssm restart <ServiceName>
    
    ```
    
9. **Uninstall the Service:**
    - If you need to remove the service, run:
    
    ```bash
    nssm remove <ServiceName> confirm
    ```
    

# Configure a Windows Service to Restart on Failure

Configuring a Windows service to restart automatically on failure is an effective way to ensure critical applications or services remain available. This guide provides step-by-step instructions on how to configure a Windows service to restart when it fails.

### Method 1: Using the Services Management Console

1. **Open the Services Management Console:**
    - Press `Win + R` to open the Run dialog.
    - Type `services.msc` and press `Enter`.
2. **Locate the Service:**
    - In the Services window, scroll through the list to find the service you want to configure.
    - Right-click on the service and select **Properties**.
3. **Change the Logon Tab:**
    - Use the Pi Vision service account for the site to run the service.
4. **Open the Recovery Tab:**
    - In the **Properties** window, navigate to the **Recovery** tab.
5. **Set Recovery Options:**
    - In the **First failure** dropdown, select **Restart the Service**.
    - In the **Second failure** dropdown, select **Restart the Service**.
    - In the **Subsequent failures** dropdown, select **Restart the Service**.
    - You can also configure the **Reset fail count after** (days) to reset the failure count after a specified number of days.
    - Set the **Restart service after** (minutes) to define how long the system should wait before attempting to restart the service after a failure.
6. **Apply and Save Changes:**
    - Click **Apply** and then **OK** to save your changes.
7. **Verify the Service Configuration:**
    - The service is now configured to restart automatically upon failure. You can test this by manually stopping the service to see if it restarts as configured.