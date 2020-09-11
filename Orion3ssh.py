import paramiko
import io_adapter
import socket
import sys
import time
import logs

class SshAdapter(io_adapter.IOAdapter):
    DELAY = 1
    NUMBER_OF_SYMBOLS_TO_RETURN = 3000

    def __init__(self, io_object, args, socket):
        self.io_object = io_object
        self.args = args
        self.socket = socket


    def send(self, arg):
        encoded_string = str(arg).encode(encoding='utf-8')  # is it needed?
        self.io_object.send(encoded_string)

    def read(self):
        return self.io_object.recv(self.NUMBER_OF_SYMBOLS_TO_RETURN).decode(encoding='utf-8')

    def open_cli(self):
        self.io_object.invoke_shell()
        print("Opening CLI")
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
        time.sleep(2)
        if self.socket._closed:
            self.io_object = ssh_init(self.args).io_object
            self.io_object.invoke_shell()
        else:
            pass

        #self.io_object = ssh_init(sys.argv).io_object  # check this
        #self.io_object.invoke_shell()

    def close_session(self):
        self.io_object.close()


def handler():
    pass


def ssh_init(arguments):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((arguments[1], 22))  # arguments[1] = device ip
    ts = paramiko.Transport(sock)
    ts.start_client(timeout=10)
    ts.auth_interactive(username=arguments[2], handler=handler)  # argument[2] = username
    chan = ts.open_session(timeout=arguments[3])
    # chan.invoke_shell()
    return SshAdapter(io_object=chan, args = arguments, socket = sock)


if __name__ == '__main__':
    ssh_adapter = ssh_init(['ssh', '192.168.10.123', 'admin', 10])
    ssh_adapter.open_cli()
    ssh_adapter.move('3')
    ssh_adapter.move('config\r')
    ssh_adapter.close_session()
