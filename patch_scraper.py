#! /opt/anaconda3/bin/python

"""
Scrapes Patch Information for AoE:HD and AoE:DE
Age of Empires has patches that consist of balance changes, bug fixes, new civ additions, etc. Here, we attempt to scrape patch information.
AoE:HD does not have main patches labeled, so we don't have major versions unlike for AoE:DE
"""

# Pre-requisite:
# Download the below websites using a browser
# Unfortunately, it looks like steamdb.info looks for JS to be enabled.
# So instead of scraping a live site, we will download the html locally and scrape that instead to get patch information
# Save to our inputs/ directory
# de_steam_id = 813780
# hd_steam_id = 221380
# de_patch_url = f'https://steamdb.info/app/{de_steam_id}/patchnotes/'
# hd_patch_url = f'https://steamdb.info/app/{hd_steam_id}/patchnotes/'

from bs4 import BeautifulSoup as Soup
import csv
import os

inputs_dir = 'inputs'

# Steam Game App IDs
games = dict()
games[933110] = ['AoE3', None]
games[459220] = ['halo-wars', None]
games[1466860] = ['AoE4', None]
games[1213210] = ['command-and-conquer', None]
games[466560] = ['northguard', None]
games[287450] = ['rise-of-nations', None]
games[594570] = ['total-war-warhammer', None]
games[231430] = ['company-of-heroes', None]
games[40950] = ['stronghold', None]
games[813780] = ['AoE2-DE', None]
games[221380] = ['AoE2-HD', None]


def update_patch_counts(soup: Soup, game_id: int) -> None:
    """
    Counts the number of updates made to a game and stores it in the global games variable
    :param soup: the BeautifulSoup object for the steamdb.info game website at 'https://steamdb.info/app/{game_steam_id}/patchnotes/'
    :param game_id: the Steam App ID for a game
    :return:
    """
    table = soup.find('tbody', attrs={'id': 'js-builds'})
    table_rows = table.find_all('tr')
    games[game_id][1] = len(table_rows)


def get_patches(soup: Soup, game_name: str) -> list:
    """
    Gets the patch notes for a game as a list
    :param game_name: `de` or `hd` for the version of age of empires (DE or HD)
    :param soup: the BeautifulSoup object for the steamdb.info game website at 'https://steamdb.info/app/{game_steam_id}/patchnotes/'
    :return: list of patches made to the game
    """
    from datetime import datetime
    import re

    patches = []
    table = soup.find('tbody', attrs={'id': 'js-builds'})
    table_rows = table.find_all('tr')

    for tr in table_rows:
        td_list = tr.find_all('td')
        date = datetime.strptime(td_list[0].find('a').string, '%d %B %Y')
        title = td_list[3].find('a').string
        has_patch_notes = td_list[5].string is None
        build_id = td_list[6].string
        # Unfortunately the patch notes themselves are not always too descriptive in steamdb
        # But we can get these from ageofempires.com itself!
        # We would like to know what a patch update did for a civ's balance, so let's scrape this info
        patch_info = re.search('(Update|Hotfix) (\d+)', title)
        patch_type = None
        patch_num = None
        patch_changes = None
        if has_patch_notes and patch_info:
            patch_type = patch_info.groups()[0]
            patch_num = int(patch_info.groups()[1])
            # 45185 is actually a hotfix but mislabeled as an update...
            if patch_num == 45185:
                patch_type = 'Hotfix'
        if patch_num is not None and patch_type == 'Update':
            patch_changes = get_patch_notes(patch_num)
        patches.append([game_name, date, title, has_patch_notes, patch_type, patch_num, patch_changes, build_id])

    return patches


def get_patch_notes(patch_num: int = 37650) -> dict({str: list}):
    """
    Returns a dictionary of civilizations and their balance changes given a patch number
    :param patch_num: the patch number
    :return: dict of civ to list of changes
    """
    import requests
    url = f'https://www.ageofempires.com/news/aoe2de-update-{patch_num}/'
    url2 = f'https://www.ageofempires.com/news/aoeii_de_update_{patch_num}/'
    url3 = f'https://www.ageofempires.com/news/aoeiide-update-{patch_num}/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    # try fallback url formats
    if response.status_code != 200:
        response = requests.get(url2, headers=headers)
    if response.status_code != 200:
        response = requests.get(url3, headers=headers)
    if response.status_code != 200:
        raise ConnectionError(f"Connection refused. URL: {url} Status code: {response.status_code}")
    patch_soup = Soup(response.text, 'html.parser')
    civ_changes = dict()

    # https://stackoverflow.com/questions/52842778/find-partial-class-names-in-spans-with-beautiful-soup
    civilization_tags = patch_soup.find_all('h4', attrs={
        'id': lambda e: e.startswith('CIVILIZATION-BALANCE_') if e else False})
    for civ_tag in civilization_tags:
        changes_tags = civ_tag.next_sibling.next_siblings
        changes = list()
        for change_tag in changes_tags:
            change = change_tag.get_text().replace('\xa0', ' ').strip()
            if change != '':
                changes.append(change)
        civ_changes[civ_tag.text] = changes

    return civ_changes


with open('inputs/de_patches.html', 'r') as de:
    de_patches = Soup(de, 'html.parser')
with open('inputs/hd_patches.html', 'r') as hd:
    hd_patches = Soup(hd, 'html.parser')

with open('data/hd_de_patches.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['Game', 'DateTime', 'Title', 'Has Patch Notes', 'Patch Type', 'Patch Number', 'Balance Changes', 'Build ID'])
    writer.writerows(get_patches(hd_patches, 'hd'))
    writer.writerows(get_patches(de_patches, 'de'))

for game_id in games.keys():
    filename = str(game_id) + '.html'
    f = os.path.join(inputs_dir, filename)
    if os.path.isfile(f):
        with open(f, 'r') as steamdb_file:
            soup = Soup(steamdb_file, 'html.parser')
            update_patch_counts(soup, game_id)

with open('data/patch_counts.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['steam_app_id', 'name', 'num_updates'])
    for game_id, lst in games.items():
        writer.writerow([game_id, lst[0], lst[1]])

