import serial
import time

# ser = serial.Serial('COM3', 9600, timeout = 1)
ser = serial.Serial(
    port='COM3',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

delay = 1


def go(*pargs):
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
