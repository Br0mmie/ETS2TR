# COPYRIGHT BR0MZ AKA STIG HAAG BROMMANN!

import win32com.client as wincl
from string import Template
from time import strftime
import requests, time, json, datetime, os, sys

speak = wincl.Dispatch("SAPI.SpVoice")
now = datetime.datetime.now()
#  i =       0      1      2     3
servers = ["sim1","sim2","arc","pm1"]

# Download data from API
# i = changes the server
def download():
    i = 0
    clearLog()
    while i < 4:
        response = requests.get("https://traffic.krashnz.com/api/v2/public/server/ets2/{}/traffic.json".format(servers[i]))
        print(str("https://traffic.krashnz.com/api/v2/public/server/ets2/{}/traffic.json".format(servers[i])))
        currentServer = servers[i]
        data = response.text
        getData(data,i,currentServer)
        i += 1
        print(str(i))
        print(servers[i])
        if i == 3:
            i = 0

# Clear the output.log file by writing an empty character to it
def clearLog():
    log = open("output.log", "w")
    log.write("")
    log.close()

# Work with the JSON/API data
# Fails if no data is return from the API
def getData(data,i,currentServer):
    count = 0
    parsed = json.loads(data)
    for x in range(1,151):
        try:
            severity = parsed["response"]["traffic"][int(x)]["severity"]
            name = parsed["response"]["traffic"][int(x)]["name"].replace("(City)","")
            players = parsed["response"]["traffic"][int(x)]["players"]
            country = parsed["response"]["traffic"][int(x)]["country"]

            if severity == "Heavy" or severity == "Congested":
                count += 1
                if country == "Luxembourg":
                    country = ""

                sayThis = "{} traffic in {} {} with {} players on {}".format(severity,name, country, players,currentServer)
                logThis = "{} traffic in {} {} with {} players on {}".format(severity,name, country, players,currentServer)
                log(logThis)
                say(sayThis)

        except:
            if count != 0:
                continue
            elif count == 0:
                log("No heavy traffic on {}".format(currentServer))
                say("No heavy traffic on {}".format(currentServer))
                download()
                continue

# Write to output.log file
def log(message):
    currentTime = "[{}.{}.{} {}:{}:{}]".format(now.day,now.month,now.year,now.hour,now.minute,now.second)
    log = open("output.log", "a")
    print("[" + strftime("%d/%m/%Y %H:%M:%S") + "] " + message)
    log.write("[" + strftime("%d/%m/%Y %H:%M:%S") + "] " + message + "\n")
    log.close()

# Tell the ai what to say
def say(message):
    speak.Speak(message)

#event()
download()
    
