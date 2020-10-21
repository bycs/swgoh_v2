"""
Импорт данных с swgoh.gg через API
с использованием библиотеки pandas
"""

import requests
import pandas as pd


def get_data_player(ally_code):
    """
    Получение информации по игроку

    :Ввод ally_code:
    :return массив с данными о игроке:
    """
    link = f'https://swgoh.gg/api/player/{ally_code}/'
    data = pd.json_normalize(requests.get(link).json()['data'])
    data = pd.DataFrame(
        data, index=None, columns=['ally_code', 'name', 'character_galactic_power', 'ship_galactic_power',
                                   'galactic_power'])
    data.set_axis(
        ['ally_code', 'player_name', 'gp_chars', 'gp_ships', 'gp_all'], axis='columns', inplace=True)
    data.loc[:, 'ally_code'] = data.loc[:, 'ally_code'].astype('int32')
    data.loc[:, 'gp_chars':'gp_all'] = data.loc[:, 'gp_chars':'gp_all'].astype('int32')
    return data


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


def units_type_chars(units):
    """
    Отбор из юнитов только персонажей

    :Ввод units:
    :return массивс персонажами:
    """
    characters = units[units['combat_type'] == 1]
    del characters['combat_type']
    return characters


def units_type_ships(units):
    """
    Отбор из юнитов только флот

    :Ввод units:
    :return массив с флотом:
    """
    ships = units[units['combat_type'] == 2]
    ships = ships.loc[:, ['ally_code', 'player_name', 'unit_id', 'unit_name', 'rarity', 'power']]
    return ships


def units_combat_type(units):
    """
    Разделение юнитов по классам (персонажи и флот)

    :Ввод units:
    :return два массива: с персонажами и флотом:
    """
    characters = units_type_chars(units)
    ships = units_type_ships(units)
    return characters, ships


def get_ally_list(guild_id):
    """
    Получение списка игроков гильдии

    :Ввод guild_id:
    :return строка с игроками гильдии:
    """
    link = f'https://swgoh.gg/api/guild/{guild_id}/'
    ally_list = pd.json_normalize(
        requests.get(link).json()['players']).loc[:, 'data.ally_code']
    ally_list = list(ally_list.astype('str'))
    ally_list = (', '.join(ally_list))
    return ally_list


def get_ally_count(guild_id):
    """
    Подсчет количества игроков в гильдии
    """
    ally_list = (get_ally_list(guild_id)).split(', ')
    count = len(ally_list)
    return count


def get_base_units_and_abilities():
    """
    :return три массива с всеми персонажами, флотом и способностями:
    """
    link_chars = f'https://swgoh.gg/api/characters/'
    link_ships = f'https://swgoh.gg/api/ships/'
    link_abilities = f'https://swgoh.gg/api/abilities/'
    chars = pd.json_normalize(requests.get(link_chars).json())
    chars = pd.DataFrame(chars, index=None, columns=['base_id', 'name', 'power', 'image'])
    chars.loc[:, 'power'] = chars.loc[:, 'power'].astype('int32')
    chars.set_axis(['unit_id', 'unit_name', 'max_power', 'url_image'], axis='columns', inplace=True)

    ships = pd.json_normalize(requests.get(link_ships).json())
    ships = pd.DataFrame(ships, index=None, columns=['base_id', 'name', 'power', 'image'])
    ships.loc[:, 'power'] = ships.loc[:, 'power'].astype('int32')
    ships.set_axis(['unit_id', 'unit_name', 'max_power', 'url_image'], axis='columns', inplace=True)

    abilities = pd.json_normalize(requests.get(link_abilities).json())
    abilities = pd.DataFrame(abilities, index=None, columns=['base_id', 'name', 'is_zeta', 'is_omega', 'image'])
    abilities.set_axis(['ability_id', 'ability_name', 'is_zeta', 'is_omega', 'url_image'], axis='columns', inplace=True)
    return chars, ships, abilities


def sync_for_ally_list(ally_list):
    """
    Получение строки со списком игроков

    :Ввод guild_id:
    :return три массива игроки, персонажи, флот:
    """
    ally_list = ally_list.split(', ')
    data = pd.DataFrame(data=None, index=None)
    units = pd.DataFrame(data=None, index=None)
    for player in ally_list:
        data = pd.concat([data, get_data_player(int(player))])
        units = pd.concat([units, get_units_player(int(player))])
    chars, ships = units_combat_type(units)
    return data, chars, ships


def sync_for_guild_id(guild_id):
    """
    Получение всех данных по гильдии

    :Ввод guild_id:
    :return три массива игроки, персонажи, флот:
    """
    ally_list = get_ally_list(guild_id)
    data, chars, ships = sync_for_ally_list(ally_list)
    return data, chars, ships
