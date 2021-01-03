from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

"""
:param lane = "TOP", "JUNGLE", "MID", "ADC", "SUPPORT"
:returns list of lanes
"""
def get_champions(lane):
    print("Getting " + lane + " champions")
    champions = []
    URL = "https://na.op.gg/champion/statistics"
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(URL, headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page, 'html.parser')

    champions_list = soup.find(class_="champion-trend-tier-" + lane)
    champions_list = champions_list.find_all('div', class_="champion-index-table__name")
    for champion in champions_list:
        champions.append(str(champion.text))
    print("Ending " + lane + " champions")
    return champions

"""
:param profile_link = https://... 
        tops, jgs, mid, adc, supp = list of champions []
:returns player_position [top, jg, mid, bot, supp, fill]
"""
def classify_players(profile_link, tops, jgs, mid, adc, supp):

    roles = {'TOP': 0, 'JG': 0, 'MID': 0, 'ADC': 0, 'SUPP': 0}

    champions = []

    URL = profile_link
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(URL, headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page, 'html.parser')

    mostplayed = soup.find('div', class_="MostChampionContent")

    print("Starting player's most played")
    for champion in mostplayed.find_all("div", class_="ChampionName"):
        champions.append(str(champion.text).strip())
    print("Ending champion most played")

    print("Analizing player's champions")
    for champion in champions:
        if champion in tops:
            roles['TOP'] += 1
        if champion in jgs:
            roles['JG'] += 1
        if champion in mid:
            roles['MID'] += 1
        if champion in adc:
            roles['ADC'] += 1
        if champion in supp:
            roles['SUPP'] += 1
    print("Ending player's analization")

    main_position = max(roles, key=roles.get)
    return main_position

"""
:param top_five = <class 'bs4.element.ResultSet'>
        players = python list[]
:returns Updated players[]
"""
def add_top_five(top_five, players):
    players_updated = players
    for player in top_five:
        player_box = player.find('div', class_='ranking-highest__icon')
        links = player_box.find_all('a', href=True)
        for a in links:
            single_link = a['href']
            single_link = 'https:'+single_link
            players_updated.append(single_link)
    return players_updated

"""
:param ninety_five = <class 'bs4.element.ResultSet'>
        players = python list[]
:returns Updated players[]
"""
def add_rest(ninety_five, players):
    players_updated = players
    for player in ninety_five:
        player_box = player.find('td', class_='select_summoner')
        links = player_box.find_all('a', href=True)
        for a in links:
            single_link = a['href']
            single_link = 'https:' + single_link
            players_updated.append(single_link)
    return players_updated

def main():
    print("Start")
    players = []

    regions = ["na", "lan", "las", "jp", "www", "eune", "oce", "ru", "br", "tr", "euw"]

    tops = get_champions("TOP")
    jgs = get_champions("JUNGLE")
    mid = get_champions("MID")
    adc = get_champions("ADC")
    supp = get_champions("SUPPORT")

    for region in regions:
        URL = "https://" + region + ".op.gg/ranking/ladder/"
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = Request(URL, headers=hdr)
        page = urlopen(req)
        soup = BeautifulSoup(page, 'html.parser')

        top_five = soup.find_all('li', class_='ranking-highest__item')
        ninety_five = soup.find_all('tr', class_='ranking-table__row')

        players = add_top_five(top_five, players)
        players = add_rest(ninety_five, players)

    players_by_position = {"TOP": [], "JG": [], "MID": [], "ADC": [], "SUPP": []}

    for player in players:
        position = classify_players(player, tops, jgs, mid, adc, supp)
        print(player + " position is: " + position)
        if position == "TOP":
            players_by_position["TOP"].append(player)
        if position == "JG":
            players_by_position["JG"].append(player)
        if position == "MID":
            players_by_position["MID"].append(player)
        if position == "ADC":
            players_by_position["ADC"].append(player)
        if position == "SUPP":
            players_by_position["SUPP"].append(player)

    print(players_by_position)
    print(len(players))

main()
