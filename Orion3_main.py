import Orion3com
import argparse
import sys
import cli_tests
import Orion3telnet
import combined_tests

print(sys.argv)

parser = argparse.ArgumentParser(description='Orion3 tester.')
parser.add_argument('--method',
                    choices=["web", "com", "telnet"],
                    help='Selected test method')
parser.add_argument('--device_counter', choices=[1, 2], default=1, help='Number of devices to be used in tests')

args = parser.parse_known_args(sys.argv)[0]

print(sys.argv)

if args.device_counter == 1:
    if args.method == "com":
        io_adapter = Orion3com.com_init(sys.argv)
    elif args.method == 'telnet':
        io_adapter = Orion3telnet.telnet_init(sys.argv)
    elif args.method == 'web':
        pass
    else:
        print('Fail')
else:
    if args.method == "com":
        io_adapter = Orion3com.com_init(sys.argv)
        io_adapter_second = Orion3com.com_init(sys.argv)  # ???
    elif args.method == 'telnet':
        io_adapter = Orion3telnet.telnet_init(sys.argv)
    elif args.method == 'web':
        pass
    else:
        print('Fail')

if __name__ == '__main__':
    print(io_adapter, 'OLOLO')
    cli_tests.open_cli(io_adapter)
    # comb.set_br(io_adapter, 32, 89, 1)
    combined_tests.test_1(io_adapter)
