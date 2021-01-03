"""
OP-GG Webscrapper and Player Analizer.
File: ReportFunctions.py
By: Daniel Chung
Date: 1/1/2021
"""


def write_report(players_by_position):
    with open("results.txt", "w", encoding='utf-8') as f:
        f.write("Report of op.gg leaderboards for all regions \n")
        f.write("\n")
        for position in players_by_position:
            if position == "TOP":
                f.write(f"Top lane | Total Players: {len(players_by_position['TOP'])}\n")
            if position == "JG":
                f.write(f"Jungle | Total Players: {len(players_by_position['JG'])}\n")
            if position == "MID":
                f.write(f"Mid lane | Total Players: {len(players_by_position['MID'])}\n")
            if position == "ADC":
                f.write(f"Adc | Total Players: {len(players_by_position['ADC'])}\n")
            if position == "SUPP":
                f.write(f"Support | Total Players: {len(players_by_position['SUPP'])}\n")
            f.write("\n")
            for player in players_by_position[position]:
                f.write("Server: " + player.region + "\n")
                f.write("Summoner Name: " + player.summoner_name + "\n")
                f.write("Player Position: " + player.position + "\n")
                f.write("Player LP: " + player.lp + "\n")
                f.write("Link: " + player.link + "\n")
                f.write("\n")
        f.close()
