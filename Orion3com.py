import serial
import time
import argparse

parser = argparse.ArgumentParser(description='Orion3 COM-port tester.')
parser.add_argument('port', default='COM3', help='Selected communication port');
parser.add_argument('baudrate', default=9600, type=int, help='Port speed');
parser.add_argument('--timeout', default=1, help='Read timeout');
parser.add_argument('--parity', default=serial.PARITY_NONE,
    choices = [
        serial.PARITY_NONE, 
        serial.PARITY_EVEN, 
        serial.PARITY_ODD, 
        serial.PARITY_MARK, 
        serial.PARITY_SPACE
    ], 
    help='Read timeout');

args = parser.parse_args();
print args;

ser = serial.Serial(
    port = args.port,
    baudrate = args.baudrate,
    parity = args.parity,
    stopbits = serial.STOPBITS_ONE,
    bytesize = serial.EIGHTBITS,
    timeout = args.timeout
)

delay = 1


def go(*pargs):
    global delay;

    print(ser.readall().decode('utf-8'))
    for arg in pargs:
        ser.write(bytes(str(arg), encoding='utf-8'))
    time.sleep(delay)


def set_br(PAM, baserate, channel):
    go('\n')
    go('3\n')
    go('pam ', PAM, ' ', channel, b'\n')
    go('baserate ', baserate, ' ', channel, '\n')
    go('m\n')
    go('2\n')
    go('apply\n')
    go('m\n')


print(ser.read_until('Exit', 200).decode('utf-8'))
ser.write(b'\n')
print(ser.readall().decode('utf-8'))
set_br(32, 88, 1)

ser.close()
