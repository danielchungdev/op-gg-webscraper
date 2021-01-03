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
    for position in players_by_position:
        print(position)
