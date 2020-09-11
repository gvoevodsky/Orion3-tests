import telnetlib
import time
import sys
import io_adapter
import logs

class TelnetAdapter(io_adapter.IOAdapter):
    DELAY = 1

    def __init__(self, io_object, args):
        self.io_object = io_object
        self.args = args

    def send(self, arg):
        self.io_object.write(bytes(str(arg), encoding='utf-8'))

    def read(self):
        return self.io_object.read_very_eager().decode('utf-8')

    def open_cli(self):
        logs.logger.info("Opening CLI")
        self.send('\n')
        self.send('\r')

    def move(self, *pargs):
        for arg in pargs:
            self.send(arg)
        self.send('\r')
        text = self.read()
        logs.logger.info(text)
        time.sleep(self.DELAY)
        return text

    def reconnect(self):
        logs.logger.warning('Reconnecting telnet!!')
        self.disconnect()
        time.sleep(2)
        self.io_object = telnet_init(self.args).io_object # нужно как то взять переменные из main

    def disconnect(self):
        self.io_object.close()


def telnet_init(arguments):
    session = telnetlib.Telnet(host=arguments[1], port=23, timeout=int(arguments[2]))
    return TelnetAdapter(io_object=session, args=arguments)


if __name__ == '__main__':
    telnet_adapter = telnet_init(['telnet', '192.168.1.10', '10'])
    telnet_adapter.open_cli()
    telnet_adapter.move('3')

