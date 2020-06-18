import serial
import time
import argparse

parser = argparse.ArgumentParser(description='Orion3 COM-port tester.')
parser.add_argument('--port', default='COM3', help='Selected communication port')
parser.add_argument('--baudrate', default=9600, type=int, help='Port speed')
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

args = parser.parse_args()

ser = serial.Serial(
    port=args.port,
    baudrate=args.baudrate,
    parity=args.parity,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=args.timeout
)

print(args)
delay = 0.5


def go(*pargs):
    global delay
    text = ser.readall().decode('utf-8')
    print(text)
    for arg in pargs:
        ser.write(bytes(str(arg), encoding='utf-8'))
    time.sleep(delay)
    return text


def set_br(PAM, baserate, channel):
    go('m\r')
    go('3\r')
    go('pam ', PAM, ' ', channel, '\r')
    go('baserate ', baserate, ' ', channel, '\r')
    go('m\r')
    go('2\r')
    go('apply\r')
    go('m\r')


def check_status():
    go('m\r')
    go('2\r')
    go('status\r')
    text = go('\r')
    print('!!!', text)
    a = text.find('SYNC')
    print(text[a + 33])
    if text[a + 33] == '1':
        print('test passed')
    elif text[a + 33] == '-':
        print('no dsl connection')
    else:
        print('some error')
    go('m\r')


baserate = 88
pam = 32
channel = 1
connection_expectation = 30

if __name__ == '__main__':
    ser.write(b'\r')  # Войти в модем
    if go('m\r'):
        set_br(pam, baserate, channel)
        print('set br complete')
        time.sleep(connection_expectation)
        check_status()
    else:
        print('no connection?')

ser.close()
