import os,configparser,shutil,schedule,time
from CopyDirectoryFunction import copy_directory_contents

#Define the location of the config file and set it to a variable.
ConfigLocation = 'C:\\Scripts\\Atlanta West File Copy\\'
config = configparser.ConfigParser()
config.read(ConfigLocation + 'Config.ini')


#Get the Target and destination folder paths from the config file.
TargetPath1 = config['SERVERS']['TargetPath']
DestinationPath1 = config['SERVERS']['DestPath']

class CustomError(Exception):
    '''
    Custom Error message for error handling
    '''
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

def Get_File_List(Directory):
    '''
    define function returning a list containing all the files in a given directory.
    In the future, you could potentially use tuple unpacking to also walk multiple folders then nested for loops to get multiple file lists
    '''
    for folder, subfolder, filenames in os.walk(Directory):

        if subfolder:
            raise CustomError('Cannot copy files from folders with subfolders.')

        if folder and not subfolder and filenames:
            return filenames
        else:
            return 'No Files Found'

def Target_Vs_Dest_Files(TargetLst,DestinationLst):
    '''
    Define function to compare two lists and output list of missing files at destination
    '''
    DestSet = set(DestinationLst)
    TargSet = set(TargetLst)

    return list(TargSet - DestSet)

def Copy_Missing_Files(TargPath,DestPath,MissingFileList):
    '''
    Function that copies a list of files from one directory to another.
    '''
    Dest = DestPath+'\\'
    for File in MissingFileList:
        Targ = TargPath+'\\'+File
        shutil.copy(Targ,Dest)

def Compare_and_copy(TargetPath,DestinationPath):
    '''
    Compare 2 lists of files created from 2 different directories. Create a new list of the files that are not at the destination.
    Copy those files
    '''
    #variable definition
    FilesAtTarget= []
    FilesAtDest = []
    Missing_Files = []

    #get the files at each location into a list
    FilesAtTarget = Get_File_List(TargetPath)
    FilesAtDest = Get_File_List(DestinationPath)

    #create a list of the missing files
    Missing_Files = Target_Vs_Dest_Files(FilesAtTarget,FilesAtDest)

    #Use the list of missing files, the tagert path, and the destination path to perform the copy operation.
    Copy_Missing_Files(TargetPath,DestinationPath,Missing_Files)

#def execute_notification():
    #print('Executing...')

#time_interval = 30


schedule.every(30).seconds.do(Compare_and_copy,TargetPath1,DestinationPath1)
#schedule.every(30).seconds.do(execute_notification)

while True:
    schedule.run_pending()
    #print('Waiting....')
    time.sleep(10)