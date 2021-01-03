from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

"""
:param lane = "TOP", "JUNGLE", "MID", "ADC", "SUPPORT"
:returns list of lanes
"""
def get_champions(lane):
    champions = []
    #comment
    URL = "https://na.op.gg/champion/statistics"
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(URL, headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page, 'html.parser')

    champions_list = soup.find(class_="champion-trend-tier-" + lane)
    champions_list = champions_list.find_all('div', class_="champion-index-table__name")
    for champion in champions_list:
        champions.append(str(champion.text))
    return champions

"""
:param profile_link = https://...
:returns player_position [top, jg, mid, bot, supp, fill]
"""
def classify_players(profile_link):
    tops = get_champions("TOP")
    jgs = get_champions("JUNGLE")
    mid = get_champions("MID")
    adc = get_champions("ADC")
    supp = get_champions("SUPPORT")

    roles = {'TOP': 0, 'JG': 0, 'MID': 0, 'ADC': 0, 'SUPP': 0}

    champions = []

    URL = profile_link
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(URL, headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page, 'html.parser')

    mostplayed = soup.find('div', class_="MostChampionContent")
    for champion in mostplayed.find_all("div", class_="ChampionName"):
        champions.append(str(champion.text).strip())

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
    URL = "https://na.op.gg/ranking/ladder/"
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(URL, headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page, 'html.parser')

    top_five = soup.find_all('li', class_='ranking-highest__item')
    ninety_five = soup.find_all('tr', class_='ranking-table__row')

    players = []
    players = add_top_five(top_five, players)
    players = add_rest(ninety_five, players)

    print(len(players))

classify_players("https://na.op.gg/summoner/userName=AnDa")
