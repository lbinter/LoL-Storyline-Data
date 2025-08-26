import argparse, os, shutil
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("regionId", help ="riot api regionId, 1 = americas, 2 = asia, 3 = europe, 4 = sea")
parser.add_argument("matchId", help ="riot league of legends match id")
parser.add_argument("workingDir", help ="working directory location")
args = parser.parse_args()

regionId = args.regionId
matchId = args.matchId
workingDir = args.workingDir

os.chdir(workingDir)

print('deleteMatch called for regionId ['+regionId+'], matchId ['+matchId+']')

p = Path('Results/'+ regionId + '/' + matchId)
if p.exists():
    # check if folder has subfolder
    for child in p.iterdir():
        if os.path.isdir(child): # given folder should not have a subfolder
            print('Folder for regionId '+regionId+' matchId '+matchId+ ' has subfolder - exiting with code 2')
            exit(2)
    for child in p.iterdir():
        os.remove(child)
    os.rmdir(p)
    print('Deleted '+p.absolute().as_posix()+' - exiting with code 0')
    exit(0)

print('No folder for regionId '+regionId+' matchId '+matchId+' exists - exiting with code 1')
exit(1)