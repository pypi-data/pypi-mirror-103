import requests
import json
import pprint
#import unittest
#import os
#from datetime import datetime

TAN_BASE_URL = "http://open.tan.fr/ewp"

class stations():
    def __init__(self, latitude, longitude):
        self._latitude = latitude
        self._longitude = longitude

    def getStations(self):
        """ Function to obtain stations around a location """
        stations=[]

        url = f"{TAN_BASE_URL}/arrets.json?latitude={self._latitude}&longitude={self._longitude}"
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        res_json = res.json()
        for station in res_json:
            stations.append({
                "name": station['libelle'],
                "codeLieu": station['codeLieu']})
        return stations

    def getWaitings(self, codeLieu):
        """ Function to obtain next arriving at a station """
        waitings=[]

        url = f"{TAN_BASE_URL}/tempsattente.json/{codeLieu}"
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        res_json = res.json()
        for station in res_json:
            waitings.append({
                "ligne": station['ligne']['numLigne'],
                "terminus": station['terminus'],
                "temps": station['temps']
                })
        return waitings

    def getTrafficInfo(self, lines):
        """ Function to obtain Traffic Information """

        infos=[]

        url= f"https://plan-tan.fr/referentiel/infostrafic"
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        res_json = res.json()

        for line in lines:
            for travaux in res_json:
                for info in travaux["lignes"]:
                    if info["shortName"]==line:
                        name = travaux["name"]
                        desc = travaux["description"]
                        infos.append({"line": line, "name": name, "description": desc })
        return infos

    def getLocationForecast(self):
        """ Function to format all Informations regarding a location """
        lines = []
        forecast = []
        for station in self.getStations():
            name = station['name']
            waitings = self.getWaitings(station['codeLieu'])
            forecast.append({"name": name, "passage": waitings })
            # Build unique dict of lines
            for service in waitings:
                if service.get('ligne') not in lines:
                    lines.append(service.get('ligne'))  
        # Get Traffic Information
        traffic=self.getTrafficInfo(lines)
        if len(traffic) > 0:
            for cast in forecast:
                for spot in cast['passage']:
                    if spot['ligne'] in lines:
                        cast['traffic'] = traffic
        return forecast
