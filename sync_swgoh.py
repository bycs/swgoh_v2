"""
Импорт данных с swgoh.gg через API
с использованием библиотеки pandas
"""

import requests
import pandas as pd


def get_units_player(ally_code):
    link = f'https://swgoh.gg/api/player/{ally_code}/'
    units = pd.json_normalize(requests.get(link).json(), 'units', [['data', 'name'], ['data', 'ally_code']],
                              record_prefix='unit.', max_level=2,)
    units = pd.DataFrame(
        units, index=None, columns=['data.ally_code', 'data.name', 'unit.data.base_id', 'unit.data.name',
                                    'unit.data.rarity', 'unit.data.gear_level', 'unit.data.relic_tier',
                                    'unit.data.power', 'unit.data.stats.1', 'unit.data.stats.28', 'unit.data.stats.5',
                                    'unit.data.stats.6', 'unit.data.stats.16', 'unit.data.stats.14',
                                    'unit.data.stats.17', 'unit.data.stats.18'])
    units.loc[:, 'unit.data.rarity':'unit.data.relic_tier'] = \
        units.loc[:, 'unit.data.rarity':'unit.data.relic_tier'].astype('int8')
    units.loc[:, 'unit.data.power':'unit.data.stats.28'] = \
        units.loc[:, 'unit.data.power':'unit.data.stats.28'].astype('int32')
    units.loc[:, 'unit.data.stats.5':'unit.data.stats.6'] = \
        units.loc[:, 'unit.data.stats.5':'unit.data.stats.6'].astype('int16')
    units.loc[:, 'unit.data.stats.16':'unit.data.stats.18'] = \
        units.loc[:, 'unit.data.stats.16':'unit.data.stats.18'].astype('float16')
    return units


def get_data_player(ally_code):
    link = f'https://swgoh.gg/api/player/{ally_code}/'
    data = pd.json_normalize(requests.get(link).json()['data'])
    return data


def get_player(ally_code):
    link = f'https://swgoh.gg/api/player/{ally_code}/'
    player = pd.json_normalize(requests.get(link).json())
    return player


def get_ally_list(guild_id):
    link = f'https://swgoh.gg/api/guild/{guild_id}/'
    ally_list = pd.json_normalize(
        requests.get(link).json()['players']).loc[:, 'data.ally_code']
    return list(ally_list)


def get_units_guild(ally_list):
    units = pd.DataFrame(
        data=None, index=None)
    for player in ally_list:
        units = pd.concat([units, get_units_player(player)])
    return units
