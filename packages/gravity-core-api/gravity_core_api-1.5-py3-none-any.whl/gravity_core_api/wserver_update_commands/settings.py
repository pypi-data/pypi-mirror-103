from gravity_core_api.wserver_update_commands.functions import *


all_keys = {'trash_cats': {'execute_function': trash_cat_execute},
            'trash_types': {'execute_function': trash_type_execute},
            'auto': {'execute_function': auto_execute},
            'companies': {'execute_function': clients_execute}}


# Данные локальной базы данных (WDB)
trash_cats_tablename = 'trash_cats'
trash_types_tablename = 'trash_types'
auto_tablename = 'auto'
clients_tablename = 'clients'

