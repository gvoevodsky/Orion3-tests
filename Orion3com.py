import serial
import time
import argparse
import sys
import io_adapter


class ComAdapter(io_adapter.IOAdapter):
    DELAY = 1

    def send(self, arg):
        self.io_object.write(bytes(str(arg), encoding='utf-8'))

    def read(self):
        return self.io_object.readall().decode('utf-8')

    def open_cli(self):
        print("Opening CLI")
        self.send('\r')

    def move(self, *pargs):
        for arg in pargs:
            self.send(arg)
        self.send('\r')
        text = self.read()
        print(text)
        time.sleep(self.DELAY)
        return text

def com_init(arguments):
    print("....")
    parser = argparse.ArgumentParser(description='Orion3 COM-port tester.')
    parser.add_argument('--timeout', default=1, help='Read timeout')
    parser.add_argument('--parity', default=serial.PARITY_NONE,
                        choices=[
                            serial.PARITY_NONE,
                            serial.PARITY_EVEN,
                            serial.PARITY_ODD,
                            serial.PARITY_MARK,
                            serial.PARITY_SPACE
                        ],
                        help='Read timeout')

    args = parser.parse_known_args(arguments)[0]

    ser = serial.Serial(
        port= ('COM' + arguments[1]),
        baudrate= int(arguments[2]),
        parity=args.parity,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=args.timeout
    )

    return ComAdapter(io_object=ser)

if __name__ == '__main__':
    com_adapter = com_init(sys.argv)