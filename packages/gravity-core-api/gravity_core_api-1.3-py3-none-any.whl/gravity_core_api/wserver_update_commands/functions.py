""" Содержит функции-обработчики команд и их вспомогательные функции """
from gravity_core_api.wserver_update_commands import settings


def trash_cat_execute(sqlshell, data, *args, **kwargs):
    """ Выполнить данные по созданию/обновлению записи о категории груза"""
    cat_name = data['cat_name']
    wserver_id = data['wserver_id']
    active = data['active']
    command = "INSERT INTO {} (cat_name, wserver_id, active) values ('{}', {}, {}) " \
              "ON CONFLICT (wserver_id) " \
              "DO UPDATE SET cat_name='{}', active={}"
    command = command.format(settings.trash_cats_tablename, cat_name, wserver_id, active,
                             cat_name, active)
    response = sqlshell.try_execute(command)
    return response


def trash_type_execute(sqlshell, data, *args, **kwargs):
    """ Выполнить данные по созданию/обновлению записи о категории груза"""
    type_name = data['name']
    wserver_id = data['wserver_id']
    active = data['active']
    wserver_category = data['category']
    command = "INSERT INTO {} (name, wserver_id, active, category) values ('{}', {}, " \
              "{}, (SELECT id FROM {} WHERE wserver_id={})) " \
              "ON CONFLICT (wserver_id) " \
              "DO UPDATE SET name='{}', active={}, category=(SELECT id FROM {} WHERE wserver_id={})"
    command = command.format(settings.trash_types_tablename, type_name, wserver_id,
                             active, settings.trash_cats_tablename, wserver_category,
                             type_name, active, settings.trash_cats_tablename, wserver_category)
    response = sqlshell.try_execute(command)
    return response
