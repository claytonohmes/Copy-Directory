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