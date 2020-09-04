import Orion3com
import argparse
import sys
import Orion3telnet
import Orion3web
import importlib
import Orion3ssh

parser = argparse.ArgumentParser(description='Orion3 tester.')

parser.add_argument('--device', nargs='+', help='Device configuration')
parser.add_argument('--test', help='tests to run')
args = parser.parse_known_args(sys.argv)[0]

print(args)
print(sys.argv)

list_of_connections = []
for device in args.device:
    '''
    Creating adapters from args
    
    --device telnet:192.168.1.1:10
    --device com:1:9600
    --device web:https://192.168.1.1:80:Chrome
    --device web:http://192.168.1.1:80:Firefox
    --device ssh:192.168.1.1:admin:10
    
    '''
    device_parameters = device.split(':')
    method = device_parameters[0]
    if method == 'com':
        io_adapter = Orion3com.com_init(device_parameters)  # !!!
        list_of_connections.append(io_adapter)
    elif method == 'telnet':
        io_adapter = Orion3telnet.telnet_init(device_parameters)
        list_of_connections.append(io_adapter)
    elif method == 'ssh':
        io_adapter = Orion3ssh.ssh_init(device_parameters)
        list_of_connections.append(io_adapter)
    elif method == 'web':
        io_adapter = Orion3web.WebAdapter(device_parameters)
        list_of_connections.append(io_adapter)
    else:
        print('Wrong method')

    if len(list_of_connections) > 2:
        print('Too many connections!')

print(list_of_connections)  # must be less than 2
print(args)

if __name__ == '__main__':
    test_to_run = args.test
    iter_tools = importlib.import_module(('.' + args.test), '.tests')
    iter_tools.test_main(list_of_connections)
