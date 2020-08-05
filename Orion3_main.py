import Orion3com
import argparse
import sys
import cli_tests
import Orion3telnet
import combined_tests
import Orion3web
import web_tests
import Orion3all_CLI



parser = argparse.ArgumentParser(description='Orion3 tester.')

parser.add_argument('--device', nargs='+', help='Device configuration')
parser.add_argument('--test', nargs='+', help='tests to run')
args = parser.parse_known_args(sys.argv)[0]

print(args)
print(sys.argv)

list_of_connections = []
for device in args.device:
    '''
    --device telnet:192.168.1.1:10
    --device com:1:9600
    --device web:https://192.168.1.1:Chrome
    --device web:http://192.168.1.1:Firefox
    --device web:http://192.168.1.1:80:Firefox
    
    '''
    device_parameters = device.split(':')
    method = device_parameters[0]
    if method == 'com':
        io_adapter = Orion3com.com_init(device_parameters) #!!!
        list_of_connections.append(io_adapter)
    elif method == 'telnet':
        io_adapter = Orion3telnet.telnet_init(device_parameters)
        list_of_connections.append(io_adapter)
    elif method == 'ssh':
        io_adapter = Orion3telnet.telnet_init(device_parameters)
        list_of_connections.append(io_adapter)
    elif method == 'web':
        io_adapter = Orion3web.WebAdapter(device_parameters)
        list_of_connections.append(io_adapter)
    else:
        print('Wrong method')

    if len(list_of_connections) > 2:
        print('Too many connections!')


print(list_of_connections) #must no be more than 2
print(args)


if __name__ == '__main__':
    for device in list_of_connections:
        print(device)
        if device.__class__.__name__ == 'WebAdapter':
            web_tests.test_first(device)
        elif device.__class__.__name__ == 'ComAdapter' or device.__class__.__name__ == 'TelnetAdapter' or device.__class__.__name__ == 'SshAdapter':
            combined_tests.test_1(device)
        else:
            print('Error')
            break

#    combined_tests.test_1(list_of_connections[0])
#    combined_tests.test_1(list_of_connections[1])
#    combined_tests.web_test_1(list_of_connections[2])

'''
    cli_tests.open_cli(io_adapter)
    # comb.set_br(io_adapter, 32, 89, 1)
    combined_tests.test_1(io_adapter)
'''