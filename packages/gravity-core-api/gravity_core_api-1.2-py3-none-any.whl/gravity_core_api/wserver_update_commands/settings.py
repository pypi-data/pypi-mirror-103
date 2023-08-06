from gravity_core_api.wserver_update_commands.functions import *


all_keys = {'trash_cat': {'execute_function': trash_cat_execute},
            'trash_type': {'execute_function': trash_type_execute}}


# Данные локальной базы данных (WDB)
trash_cats_tablename = 'trash_cats'
trash_types_tablename = 'trash_types'

