"""
Импорт данных с swgoh.gg через API
с использованием библиотеки pandas
"""

import requests
import pandas as pd


def get_units_player(ally_code):
    """
    Получение списка персонажей по игроку

    :Ввод ally_code:
    :return массив с персонажами:
    """
    link = f'https://swgoh.gg/api/player/{ally_code}/'
    units = pd.json_normalize(requests.get(link).json(), 'units', [['data', 'name'], ['data', 'ally_code']],
                              record_prefix='unit.', max_level=2,)
    units = pd.DataFrame(
        units, index=None, columns=['data.ally_code', 'data.name', 'unit.data.base_id', 'unit.data.name',
                                    'unit.data.rarity', 'unit.data.gear_level', 'unit.data.relic_tier',
                                    'unit.data.power', 'unit.data.stats.1', 'unit.data.stats.28', 'unit.data.stats.5',
                                    'unit.data.stats.6', 'unit.data.stats.16', 'unit.data.stats.14',
                                    'unit.data.stats.17', 'unit.data.stats.18', 'unit.data.combat_type'])
    units.loc[:, 'unit.data.rarity':'unit.data.relic_tier'] = \
        units.loc[:, 'unit.data.rarity':'unit.data.relic_tier'].astype('int8')
    units.loc[:, 'unit.data.power':'unit.data.stats.28'] = \
        units.loc[:, 'unit.data.power':'unit.data.stats.28'].astype('int32')
    units.loc[:, 'unit.data.stats.5':'unit.data.stats.6'] = \
        units.loc[:, 'unit.data.stats.5':'unit.data.stats.6'].astype('int16')
    units.loc[:, 'unit.data.stats.16':'unit.data.stats.18'] = \
        units.loc[:, 'unit.data.stats.16':'unit.data.stats.18'].astype('float16')
    units.loc[:, 'unit.data.combat_type'] = units.loc[:, 'unit.data.combat_type'].astype('int8')
    units.set_axis(
        ['ally_code', 'player_name', 'unit_id', 'unit_name', 'rarity', 'gear_level', 'relic_tier ', 'power',
         'health', 'protection', 'speed', 'physical_damage', 'critical_damage', 'critical_chance',
         'potency', 'tenacity', 'combat_type'], axis='columns', inplace=True)
    return units


def units_combat_type(units):
    """
    Разделение юнитов по классам

    :Ввод units:
    :return два массива: с персонажами и флотом:
    """
    characters = units[units['combat_type'] == 1]
    ships = units[units['combat_type'] == 2]
    del characters['combat_type']
    ships = ships.loc[:, ['ally_code', 'player_name', 'unit_id', 'unit_name', 'rarity', 'power']]
    return characters, ships


def get_data_player(ally_code):
    """
    Получение информации по игроку

    :Ввод ally_code:
    :return массив с данными о игроке:
    """
    link = f'https://swgoh.gg/api/player/{ally_code}/'
    data = pd.json_normalize(requests.get(link).json()['data'])
    return data


def get_ally_list(guild_id):
    """
    Получение списка игроков гильдии

    :Ввод guild_id:
    :return массив с игроками гильдии:
    """
    link = f'https://swgoh.gg/api/guild/{guild_id}/'
    ally_list = pd.json_normalize(
        requests.get(link).json()['players']).loc[:, 'data.ally_code']
    return list(ally_list)


def get_units_guild(ally_list):
    """
    Получение списка персонажей по игрокам гильдии

    :Ввод ally_list:
    :return массив с персонажами гильдии:
    """
    units = pd.DataFrame(
        data=None, index=None)
    for player in ally_list:
        units = pd.concat([units, get_units_player(player)])
    return units
