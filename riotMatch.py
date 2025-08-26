import requests, json, argparse, shutil, time, os
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("regionId", help ="riot api regionId, 1 = americas, 2 = asia, 3 = europe, 4 = sea")
parser.add_argument("matchId", help ="riot league of legends match id")
parser.add_argument("api", help="your api key from https://developer.riotgames.com/")
parser.add_argument("workingDir", help ="working directory location")
args = parser.parse_args()

regionId = args.regionId
matchId = args.matchId
api = args.api
workingDir = args.workingDir

os.chdir(workingDir)

print('riotMatch.py called with regionId ['+regionId+'], matchId ['+matchId+'], api ['+api+']')

infoJson = {
    "match" : {
        "start" : 0,
        "end": 0
    },
    "timeline" : {
        "start" : 0,
        "end": 0
    }
}


p = Path('Results/' + regionId + '/' + matchId)
if p.exists():
    print("Folder for match already exists - exiting with code 2")
    exit(2)

urlRegionAmerica = 'https://americas.api.riotgames.com'
urlRegionAsia = 'https://asia.api.riotgames.com'
urlRegionEurope = 'https://europe.api.riotgames.com'
urlRegionSea = 'https://sea.api.riotgames.com'

urlRegion = ''

if regionId == '1':
    # americas
    urlRegion = urlRegionAmerica
elif regionId == '2':
    # asia
    urlRegion = urlRegionAsia
elif regionId == '3':
    # europe
    urlRegion = urlRegionEurope
elif regionId == '4':
    # sea
    urlRegion = urlRegionSea
else:
    print("Invalid region code " + regionId + " - exiting with code 3")
    exit(3)


urlApi = '/lol/match/v5/matches/'+matchId
urlParamsTimeline = '/timeline?api_key=' + api
urlParamsInfo = '?api_key=' + api

print(urlRegion+urlApi+urlParamsInfo)

infoJson["match"]["start"] = time.time()
respone = requests.get(urlRegion+urlApi+urlParamsInfo)
jsonString = json.dumps(respone.json(), indent=4)

# check if data was fetched or an error code json was received
data = json.loads(jsonString)
if 'metadata' not in data:
    exit(3)
if 'info' not in data:
    exit(3)

# create folder for match 
p.mkdir()

jsonFile = open('Results/'+ regionId + '/' + matchId + "/MatchInfo.json", "w")
jsonFile.write(jsonString)
jsonFile.close()
print("Region "+ regionId + ": Match " + matchId + " info data fetched!")
infoJson["match"]["end"] = time.time()



infoJson["timeline"]["start"] = time.time()
respone2 = requests.get(urlRegion+urlApi+urlParamsTimeline)
jsonString = json.dumps(respone2.json(), indent=4)

# check if data was fetched or an error code json was received
data = json.loads(jsonString)
if 'metadata' not in data:
    exit(3)
if 'info' not in data:
    exit(3)

jsonFile = open('Results/'+ regionId + '/' + matchId + "/Match.json", "w")
jsonFile.write(jsonString)
jsonFile.close()
print("Region "+ regionId + ": Match " + matchId + " timeline data fetched!")
infoJson["timeline"]["end"] = time.time()

jsonInfoFile = open('Results/'+ regionId + '/' + matchId + '/info.json', 'a')
jsonInfoFile.write(json.dumps(infoJson))
jsonInfoFile.close()

print("Region "+ regionId + ": Match " + matchId + " finished")