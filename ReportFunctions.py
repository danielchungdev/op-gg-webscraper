"""
OP-GG Webscrapper and Player Analizer.
File: ReportFunctions.py
By: Daniel Chung
Date: 1/1/2021
"""

from datetime import datetime

def write_report(players_by_position):
    today = datetime.today()
    date = today.strftime("%b-%d-%Y")+".txt"
    f = open(date, "w+")
    f.write("Report of op.gg leaderboards for all regions \n")
    f.write("Date: " + today.strftime("%b-%d-%Y") + "\n")
    for position in players_by_position:
        if position == "TOP":
            f.write("Top lane\n")
        if position == "JG":
            f.write("Jungle\n")
        if position == "MID":
            f.write("Mid lane\n")
        if position == "ADC":
            f.write("Adc\n")
        if position == "SUPP":
            f.write("Support\n")
        f.write("\n")
        for player in players_by_position[position]:
            f.write("Server: " + player.region)
            f.write("Summoner Name: " + player.summoner_name + "\n")
            f.write("Player Position: " + player.position + "\n")
            f.write("Player LP: " + player.lp + "\n")
            f.write("Link: " + player.link + "\n")
            f.write("\n")
    f.close()
