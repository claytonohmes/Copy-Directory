import configparser,schedule,time
from CopyDirectoryFunction import copy_directory_contents

#Define the location of the config file and set it to a variable.
ConfigLocation = 'C:\\Users\\cohmes\\Documents\\GitHub\\Copy-Directory\\'
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

schedule.every(30).seconds.do(copy_directory_contents,TargetPath1,DestinationPath1)

while True:
    schedule.run_pending()
    #print('Waiting....')
    time.sleep(10)