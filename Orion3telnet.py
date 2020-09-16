import telnetlib
import time
import io_adapter
import logs


class TelnetAdapter(io_adapter.IOAdapter):
    DELAY = 1

    def __init__(self, io_object, args, socket):
        self.io_object = io_object
        self.args = args
        self.socket = socket

    def send(self, arg):
        self.io_object.write(bytes(str(arg), encoding='utf-8'))

    def read(self):
        return self.io_object.read_very_eager().decode('utf-8')

    def open_cli(self):
        self.reconnect()
        logs.logger.info("Opening CLI")
        # self.send('\n')

    def move(self, *pargs):
        for arg in pargs:
            self.send(arg)
        self.send('\r')
        time.sleep(self.DELAY)  # without this delay read_very_eager fails
        text = self.read()
        logs.logger.info(text)
        # time.sleep(self.DELAY)
        return text

    def reconnect(self):
        logs.logger.info('Reconnecting telnet session')
        # logs.logger.warning(self.socket._closed)
        # if self.socket._closed:
        #    logs.logger.info('socked was closed, reopening')
        #    self.io_object = telnetlib.Telnet(host=self.args[1], port=23, timeout=int(self.args[2]))
        #    self.socket = self.io_object.get_socket()
        #    time.sleep(1)
        # else:
        #    logs.logger.info('socked was open')
        #    pass
        self.disconnect()
        self.io_object = telnet_init(self.args).io_object
        time.sleep(1)

    def disconnect(self):
        self.io_object.close()


def telnet_init(arguments):
    session = telnetlib.Telnet(host=arguments[1], port=23, timeout=int(arguments[2]))
    sock = session.get_socket()
    return TelnetAdapter(io_object=session, args=arguments, socket=sock)


if __name__ == '__main__':
    telnet_adapter = telnet_init(['telnet', '192.168.1.10', '10'])
    telnet_adapter.open_cli()
    telnet_adapter.move('3')
