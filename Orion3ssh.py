import paramiko
import io_adapter
import socket
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
        self.reconnect()
        logs.logger.info("Opening CLI")
        self.send('\r')

    def move(self, *pargs):
        try:
            for arg in pargs:
                self.send(arg)
            self.send('\r')
            time.sleep(self.DELAY)
            text = self.read()
            logs.logger.info(text)
            if self.socket._closed: # debug if/else
                logs.logger.info('socked closed')
            else:
                logs.logger.info('socket opened')
            return text
        except paramiko.ssh_exception.SSHException:
            logs.logger.critical('SSH socket error!')
            self.reconnect()

    def reconnect(self):
        logs.logger.info('recconecting ssh session\n')
        if self.socket._closed:
            time.sleep(1)
            logs.logger.info('socked was closed, reopening')
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.args[1], 22))
            logs.logger.info(self.socket)
            ts = paramiko.Transport(self.socket)
            ts.start_client(timeout=10)
            ts.auth_interactive(username=self.args[2], handler=handler)
            self.io_object = ts.open_session(timeout=self.args[3])
            self.io_object.invoke_shell()
        else:
            logs.logger.info('socked was open')
            pass

    def socket_close(self):
        self.socket.close()

    def close_session(self):
        self.io_object.close()


def handler():
    pass


def ssh_init(arguments):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((arguments[1], 22))  # arguments[1] = device ip
    logs.logger.info(sock)
    ts = paramiko.Transport(sock)
    ts.start_client(timeout=10)
    ts.auth_interactive(username=arguments[2], handler=handler)  # argument[2] = username
    chan = ts.open_session(timeout=arguments[3])
    chan.invoke_shell()
    return SshAdapter(io_object=chan, args=arguments, socket=sock)


if __name__ == '__main__':
    ssh_adapter = ssh_init(['ssh', '192.168.10.123', 'admin', 10])
    ssh_adapter.open_cli()
    ssh_adapter.move('3')
    ssh_adapter.move('config\r')
    ssh_adapter.close_session()
