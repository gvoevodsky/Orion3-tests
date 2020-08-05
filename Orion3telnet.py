import telnetlib
import time
import sys
import io_adapter


class TelnetAdapter(io_adapter.IOAdapter):
    DELAY = 1

    def send(self, arg):
        self.io_object.write(bytes(str(arg), encoding='utf-8'))

    def read(self):
        return self.io_object.read_very_eager().decode('utf-8')

    def open_cli(self):
        print("Opening CLI")
        self.send('\n')
        self.send('\r')

    def move(self, *pargs):
        for arg in pargs:
            self.send(arg)
        self.send('\r')
        text = self.read()
        print(text)
        time.sleep(self.DELAY)
        return text

    def reconnect(self):
        self.io_object = telnet_init(sys.argv).io_object


def telnet_init(arguments):
    session = telnetlib.Telnet(host=arguments[1], port=23, timeout=int(arguments[2]))
    return TelnetAdapter(io_object=session)


# def telnet_init(arguments, n):
#    print('.....')
#    parser = argparse.ArgumentParser(description='Orion3 telnet tester.')
#    parser.add_argument('--host', default='192.168.1.10', help='modem ip')
#    parser.add_argument('--port', default=23, help='port for telnet connection')
#    parser.add_argument('--timeout', default=10)
#    parser.add_argument('--delay', default=1, help='delay  ')
#
#    args = parser.parse_known_args(arguments)[0]
#    print(args)
#
#    session = telnetlib.Telnet(args.host[n], args.port, args.timeout)
#
#    return TelnetAdapter(io_object=session)
#

if __name__ == '__main__':
    telnet_adapter = telnet_init(sys.argv)
    telnet_adapter.open_cli()
