swgoh_v2 (Made in Python)
===
🎮 Import data from swgoh.gg
---
* by player or Guild
* all units and abilities
***
💽 Install:
---
* Installing poetry
>https://python-poetry.org/docs/#installation
* Recommendation
> poerty config virtualenvs.in-project true
* Creating a virtual environment and installing dependencies
> poetry install
***
📠 Basic functions:
---
* import by player
    * data
    * units
        * characters
        * ships
* import by the list of players
    * data
    * units
        * characters
        * ships
* import by the Guild
    * data
    * units
        * characters
        * ships
* import all units
    * characters
    * ships
* import all the ability
***
📝 List of functions
---
* get_data_player(ally_code)
> Получение информации по игроку  
> :input ally_code (int):  
> :return массив с данными о игроке (DataFrame):

* get_units_player(ally_code)
> Получение списка персонажей по игроку  
> :input ally_code (int):  
> :return массив с персонажами (DataFrame):

* units_type_chars(units)
> Отбор из юнитов только персонажей  
> :input units (DataFrame):  
> :return массив с персонажами (DataFrame):

* units_type_ships(units)
> Отбор из юнитов только флот  
> :input units (DataFrame):  
> :return массив с флотом (DataFrame):

* units_combat_type(units)
> Разделение юнитов по классам (персонажи и флот)  
> :input units (DataFrame):  
> :return два массива: с персонажами и флотом (DataFrame x2):

* get_ally_list(guild_id)
> Получение списка игроков гильдии  
> :input guild_id (int):  
> :return строка с игроками гильдии (str):

* get_ally_count(guild_id)
> Подсчет количества игроков в гильдии  
> :input guild_id (str):  
> :return количетсво игроков в гильдии (int):

* get_base_units(combat_type)
> Получение списка юнитов: персонажи или флот  
> :input 'characters' or 'ships':  
> :return массив с базой юнитов (DataFrame):

* get_base_abilities()
> :return массив со всеми способностями (DataFrame):

* get_base_units_and_abilities()
> :return два массива со всеми юнитами и способностями (DataFrame x2):

* sync_for_ally_list(ally_list)
> Получение строки со списком кодов игроков  
> :input ally_list (str):  
> :return три массива игроки, персонажи, флот (DataFrame x3):

* sync_for_guild_id(guild_id)
> Получение всех данных по гильдии  
> :input guild_id (int):  
> :return три массива игроки, персонажи, флот (DataFrame x3):
___
I will be happy to receive feedback.
