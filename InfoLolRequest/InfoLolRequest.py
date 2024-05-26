import requests
import pandas as pd
import json

class InfoLolRequest:

    base_url = "https://americas.api.riotgames.com"
    api_key = "RGAPI-f15fc11a-d5ad-4dd1-a18a-734003f29320"
    nombre_jugador = "MachapeTactico13"
    tagLine = "LAN"
    puuid = ""

    def __init__(self, api_key, nombre_jugador):
        self.api_key = api_key
        self.nombre_jugador = nombre_jugador

    def requestMatches(self):
        url = f"{self.base_url}/riot/account/v1/accounts/by-riot-id/{self.nombre_jugador}/{self.tagLine}?api_key={self.api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            cuenta_id = response.json()
            self.puuid = cuenta_id["puuid"]
        else:
            print("Error al obtener la cuenta del jugador:", response.status_code)
        return self.getMatches()
    
    def getMatches(self):
        url = f"{self.base_url}/lol/match/v5/matches/by-puuid/{self.puuid}/ids?api_key={self.api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            ids_partidas = response.json()
        else:
            print("Error al obtener las partidas del jugador:", response.status_code)
        return ids_partidas
    
    def getVectorData(self, idMatch):
        url = f"{self.base_url}/lol/match/v5/matches/{idMatch}?api_key={self.api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            matchDto = response.json()
        else:
            print("Error al obtener las partidas del jugador:", response.status_code)
        return self.getInformation(matchDto)

    def getInformation(self, matchDto):
        infoDataMatch = matchDto["info"]
        participantsMatchInfo = infoDataMatch["participants"]
        blueParticipants, redParticipants = self.getTeamsInfo(participantsMatchInfo)
        matchID = matchDto["metadata"]["matchId"]
        blueTeamControlWardsPlaced ,redTeamControlWardsPlaced = self.getControlWardsInfo(blueParticipants, redParticipants)
        blueTeamWardsPlaced,redTeamWardsPlaced = self.getWardsInfo(blueParticipants, redParticipants)
        blueTeamTotalKills, redTeamTotalKills = self.getKillsInfo(blueParticipants, redParticipants)
        blueTeamDragonKills, redTeamDragonKills = self.getDragonKillsInfo(infoDataMatch)
        blueTeamHeraldKills, redTeamHeraldKills = self.getHeraldKillsInfo(infoDataMatch)
        blueTeamTowersDestroyed, redTeamTowersDestroyed = self.getTowersDestroyedInfo(infoDataMatch)
        blueTeamInhibitorsDestroyed, redTeamInhibitorsDestroyed = self.getInhibitorsDestroyedInfo(infoDataMatch)
        blueTeamTurretPlatesDestroyed, redTeamTurretPlatesDestroyed = self.getTurretPlatesDestroyedInfo(blueParticipants, redParticipants)
        blueTeamFirstBlood, redTeamFirstBlood = self.getFirstBloodInfo(blueParticipants, redParticipants)
        blueTeamMinionsKilled, redTeamMinionsKilled = self.getMinionsKilledInfo(blueParticipants, redParticipants)
        blueTeamJungleMinions, redTeamJungleMinions = self.getJungleMonsterKillsInfo(blueParticipants, redParticipants)
        blueTeamTotalGold, redTeamTotalGold = self.getTotalGoldInfo(blueParticipants, redParticipants)
        blueTeamXp, redTeamXp = self.getTeamXPInfo(blueParticipants, redParticipants)
        blueTeamTotalDamageToChamps, redTeamTotalDamageToChamps = self.getDamageToChamps(blueParticipants, redParticipants)
        for i in infoDataMatch["teams"]:
            if i["teamId"] == 200:
                blueWin = i["win"]
        finalDataq = {"matchID": [matchID], "blueTeamControlWardsPlaced": [blueTeamControlWardsPlaced], "blueTeamWardsPlaced": [blueTeamWardsPlaced], "blueTeamTotalKills": [blueTeamTotalKills], "blueTeamDragonKills": [blueTeamDragonKills], "blueTeamHeraldKills": [blueTeamHeraldKills], "blueTeamTowersDestroyed": [blueTeamTowersDestroyed], "blueTeamInhibitorsDestroyed": [blueTeamInhibitorsDestroyed], "blueTeamTurretPlatesDestroyed": [blueTeamTurretPlatesDestroyed], "blueTeamFirstBlood": [blueTeamFirstBlood], "blueTeamMinionsKilled": [blueTeamMinionsKilled], "blueTeamJungleMinions": [blueTeamJungleMinions], "blueTeamTotalGold": [blueTeamTotalGold], "blueTeamXp": [blueTeamXp], "blueTeamTotalDamageToChamps": [blueTeamTotalDamageToChamps], "redTeamControlWardsPlaced": [redTeamControlWardsPlaced], "redTeamWardsPlaced": [redTeamWardsPlaced], "redTeamTotalKills": [redTeamTotalKills], "redTeamDragonKills": [redTeamDragonKills], "redTeamHeraldKills": [redTeamHeraldKills], "redTeamTowersDestroyed": [redTeamTowersDestroyed], "redTeamInhibitorsDestroyed": [redTeamInhibitorsDestroyed],  "redTeamTurretPlatesDestroyed": [redTeamTurretPlatesDestroyed], "redTeamMinionsKilled": [redTeamMinionsKilled], "redTeamJungleMinions": [redTeamJungleMinions], "redTeamTotalGold": [redTeamTotalGold], "redTeamXp": [redTeamXp], "redTeamTotalDamageToChamps": [redTeamTotalDamageToChamps], "blueWin": [blueWin]}
        return finalDataq
    
    def getTeamsInfo(self, participantsMatchInfo):
        blueParticipants = []
        redParticipants = []
        for participant in participantsMatchInfo:
            if participant["teamId"] == 100:
                redParticipants.append(participant)
            else:
                blueParticipants.append(participant)
        return (blueParticipants, redParticipants)
    
    def getControlWardsInfo(self, blueParticipants,redParticipants):
        blueTeamControlWardsPlaced = 0
        redTeamControlWardsPlaced = 0
        for i,j in zip(blueParticipants,redParticipants):
            blueTeamControlWardsPlaced += i["challenges"]["controlWardsPlaced"]
            redTeamControlWardsPlaced += j["challenges"]["controlWardsPlaced"]
        return (blueTeamControlWardsPlaced, redTeamControlWardsPlaced)
    
    def getWardsInfo(self, blueParticipants,redParticipants):
        blueTeamWardsPlaced = 0
        redTeamWardsPlaced = 0
        for i, j in zip(blueParticipants,redParticipants):
            blueTeamWardsPlaced += i["wardsPlaced"]
            redTeamWardsPlaced += j["wardsPlaced"]
        return (blueTeamWardsPlaced,redTeamWardsPlaced)
    
    def getKillsInfo(self, blueParticipants,redParticipants):
        blueTeamTotalKills =  0
        redTeamTotalKills =  0
        for i,j in zip(blueParticipants, redParticipants):
            blueTeamTotalKills += i["kills"]
            redTeamTotalKills += j["kills"]
        return (blueTeamTotalKills, redTeamTotalKills)
    
    def getDragonKillsInfo(self, dataMatch):
        blueTeamDragonKills = 0
        redTeamDragonKills = 0
        for i in dataMatch["teams"]:
            if i["teamId"] == 100:
                redTeamDragonKills += i["objectives"]["dragon"]["kills"]
            else:
                blueTeamDragonKills += i["objectives"]["dragon"]["kills"]
        return (blueTeamDragonKills, redTeamDragonKills)
    
    def getHeraldKillsInfo(self, dataMatch):
        blueTeamHeraldKills = 0
        redTeamHeraldKills = 0
        for i in dataMatch["teams"]:
            if i["teamId"] == 100:
                redTeamHeraldKills += i["objectives"]["riftHerald"]["kills"]
            else:
                blueTeamHeraldKills += i["objectives"]["riftHerald"]["kills"]
        return (blueTeamHeraldKills, redTeamHeraldKills)
    
    def getTowersDestroyedInfo(self, dataMatch):
        blueTeamTowersDestroyed = 0
        redTeamTowersDestroyed = 0
        for i in dataMatch["teams"]:
            if i["teamId"] == 100:
                redTeamTowersDestroyed += i["objectives"]["tower"]["kills"]
            else:
                blueTeamTowersDestroyed += i["objectives"]["tower"]["kills"]
        return (blueTeamTowersDestroyed, redTeamTowersDestroyed)
    
    def getInhibitorsDestroyedInfo(self, dataMatch):
        blueTeamInhibitorsDestroyed = 0
        redTeamInhibitorsDestroyed = 0
        for i in dataMatch["teams"]:
            if i["teamId"] == 100:
                redTeamInhibitorsDestroyed += i["objectives"]["inhibitor"]["kills"]
            else:
                blueTeamInhibitorsDestroyed += i["objectives"]["inhibitor"]["kills"]
        return (blueTeamInhibitorsDestroyed, redTeamInhibitorsDestroyed)
    
    def getTurretPlatesDestroyedInfo(self, blueParticipants,redParticipants):
        blueTeamTurretPlatesDestroyed = 0
        redTeamTurretPlatesDestroyed = 0
        for i,j in zip(blueParticipants,redParticipants):
            blueTeamTurretPlatesDestroyed += i["challenges"]["turretPlatesTaken"]
            redTeamTurretPlatesDestroyed += j["challenges"]["turretPlatesTaken"]
        return (blueTeamTurretPlatesDestroyed, redTeamTurretPlatesDestroyed)
    
    def getFirstBloodInfo(self, blueParticipants, redParticipants):    
        blueTeamFirstBlood = False
        redTeamFirstBlood = False
        for i, j in zip(blueParticipants, redParticipants):
            if i["firstBloodKill"]:
                blueTeamFirstBlood = True
            if j["firstBloodKill"]:
                redTeamFirstBlood = True
        return (blueTeamFirstBlood, redTeamFirstBlood)
    
    def getMinionsKilledInfo(self, blueParticipants, redParticipants):    
        blueTeamMinionsKilled = 0
        redTeamMinionsKilled = 0
        for i, j in zip(blueParticipants, redParticipants):
            blueTeamMinionsKilled += i["totalMinionsKilled"]
            redTeamMinionsKilled += j["totalMinionsKilled"]
        return (blueTeamMinionsKilled, redTeamMinionsKilled)
    
    def getJungleMonsterKillsInfo(self, blueParticipants, redParticipants):
        blueTeamJungleMinions = 0
        redTeamJungleMinions = 0
        for i, j in zip(blueParticipants, redParticipants):
            blueTeamJungleMinions += i["totalAllyJungleMinionsKilled"]
            redTeamJungleMinions += j["totalAllyJungleMinionsKilled"]
        return (blueTeamJungleMinions, redTeamJungleMinions)

    def getTotalGoldInfo(self, blueParticipants, redParticipants):    
        blueTeamTotalGold = 0
        redTeamTotalGold = 0
        for i, j in zip(blueParticipants, redParticipants):
            blueTeamTotalGold += i["goldEarned"]
            redTeamTotalGold += j["goldEarned"]
        return (blueTeamTotalGold, redTeamTotalGold)
    
    def getTeamXPInfo(self, blueParticipants, redParticipants):    
        blueTeamXp = 0
        redTeamXp = 0
        for i, j in zip(blueParticipants, redParticipants):
            blueTeamXp += i["champExperience"]
            redTeamXp += j["champExperience"]
        return (blueTeamXp, redTeamXp)

    def getDamageToChamps(self, blueParticipants, redParticipants):    
        blueTeamTotalDamageToChamps = 0
        redTeamTotalDamageToChamps = 0
        for i, j in zip(blueParticipants, redParticipants):
            blueTeamTotalDamageToChamps += i["damageDealtToObjectives"]
            redTeamTotalDamageToChamps += j["damageDealtToObjectives"]
        return (blueTeamTotalDamageToChamps, redTeamTotalDamageToChamps)