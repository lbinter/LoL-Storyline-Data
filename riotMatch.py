import requests, json, argparse, shutil, time, os
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("api", help="your api key from https://developer.riotgames.com/")
parser.add_argument("matchId", help ="riot league of legends match id")
parser.add_argument("workingDir", help ="working directory location")
args = parser.parse_args()

api = args.api
matchId = args.matchId
workingDir = args.workingDir

os.chdir(workingDir)

print('riotMatch.py called with api ['+api+'] matchId ['+matchId+']')

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

p = Path('Results/'+matchId)
if p.exists():
    for child in p.iterdir():
        if child.suffix != '.json': # only allow to delete folders only containing json files
            print("Folder already exists with contents other then json - exiting")
            exit(2)
    shutil.rmtree(p)
p.mkdir()


urlRegion = 'https://europe.api.riotgames.com'
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

jsonFile = open('Results/'+matchId+"/MatchInfo.json", "w")
jsonFile.write(jsonString)
jsonFile.close()
print(" Match " + matchId + " info data fetched!")
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

jsonFile = open('Results/'+matchId+"/Match.json", "w")
jsonFile.write(jsonString)
jsonFile.close()
print("Match " + matchId + " timeline data fetched!")
infoJson["timeline"]["end"] = time.time()

jsonInfoFile = open('Results/'+matchId+'/info.json', 'a')
jsonInfoFile.write(json.dumps(infoJson))
jsonInfoFile.close()