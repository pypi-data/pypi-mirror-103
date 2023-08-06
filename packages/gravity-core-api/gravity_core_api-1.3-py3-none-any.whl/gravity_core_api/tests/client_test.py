from socket import socket
from gravity_core_api.tests import test_settings as s
import pickle


test_data = {'trash_types': {'name': 'TEST123', 'wserver_id': 99, 'category': 12 ,'active': True}}
command = {}
command['wserver_insert_command'] = test_data
command = pickle.dumps(command)
sock = socket()
sock.connect((s.api_ip, s.api_port))
sock.send(command)
response = sock.recv(1024)
response = pickle.loads(response)
print(response)