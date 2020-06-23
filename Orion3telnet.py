import telnetlib
import time
import argparse
import sys
import io_adapter


delay = 1

def telnet_init(arguments):
    print('.....')
    parser = argparse.ArgumentParser(description='Orion3 telnet tester.')
    parser.add_argument('--host', default='192.168.0.222', help='modem ip')
    parser.add_argument('--port', default=23, help='port for telnet connection')
    parser.add_argument('--timeout', default=10)

    args = parser.parse_known_args(arguments)[0]
    print(args)

    session = telnetlib.Telnet(args.host, args.port, args.timeout)

    return io_adapter.IOAdapter(io_object=session, io_method=go, open_cli=open_cli)

def go(session, *pargs):
    global delay
    text = session.read_very_eager().decode('utf-8')
    print(text)
    for arg in pargs:
        session.write(bytes(str(arg), encoding='utf-8'))
    time.sleep(delay)
    return text

def open_cli(arguments):
    pass

if __name__ == '__main__':
    go('m\r')  # Войти в модем
    if go('m\r'):
        set_br(pam, baserate, channel)
        print('set br complete')
        time.sleep(connection_expectation)
        check_status()  # problem here!
    else:
        print('no connection?')
    session.close()
