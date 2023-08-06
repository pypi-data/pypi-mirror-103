from socket import socket
from gravity_core_api.tests import test_settings as s
import pickle


# ТЕСТ ВИДОВ ГРУЗОВ
#test_data = {'trash_types': {'name': 'TEST123', 'wserver_id': 99, 'category': 12 ,'active': True}}

# ТЕСТ КЛИЕНТОВ
#test_data = {'companies':
#                 {'full_name':
#                      'TEST123', 'wserver_id': 1488, 'inn': 1488 ,'kpp': 1488, 'access':True, 'active': True,
#                  'id_1c': 1488}}

# ТЕСТ КАТЕГОРИЙ ГРУЗОВ
test_data = {'auto': {'car_number': 'test123', 'wserver_id': 1488, 'rfid': 1488, 'active':True, 'rg_weight': 0,
                      'car_protocol': 'rfid', 'auto_model':0}}
command = {}
command['wserver_insert_command'] = test_data

#command = {'wserver_insert_command': {'auto': {'car_number': 'Х079АС102', 'car_protocol': 'rfid', 'rg_weight': 0, 'auto_model': 0, 'wserver_id': 634888, 'active': True, 'rfid': 'FFFF000140'}}}
command = {'wserver_insert_command': {'companies': {'wserver_id': 34197, 'full_name': 'ООО "Вториндустрия"', 'short_name': 'ООО "Вториндустрия"', 'inn': '0268058847', 'kpp': None, 'active': True, 'id_1c': '000000006'}}}
command = pickle.dumps(command)
sock = socket()
sock.connect((s.api_ip, s.api_port))
sock.send(command)
response = sock.recv(1024)
response = pickle.loads(response)
print(response)