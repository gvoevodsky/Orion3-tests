import serial
import time
import argparse
import sys
import io_adapter

def com_init(arguments):
    print("....")
    parser = argparse.ArgumentParser(description='Orion3 COM-port tester.')
    parser.add_argument('--port', default='COM3', help='Selected communication port')
    parser.add_argument('--baudrate', default=9600, type=int, help='Port speed')
    parser.add_argument('--timeout', default=5, help='Read timeout')

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
        port=args.port,
        baudrate=args.baudrate,
        parity=args.parity,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=args.timeout
    )

    print(args)
    return io_adapter.IOAdapter(io_object=ser, io_method=go, open_cli=open_cli)


def go(ser, *pargs):
    for arg in pargs:
        print('sending - ', arg)
        ser.write(bytes(str(arg), encoding='utf-8'))
    time.sleep(1)

    for line in ser:
        print(line)
    #text = ser.readall().decode('utf-8')
    #print(text)
    return "---"

def open_cli(ser):
    print("Opening CLI")
    ser.write(b'\n')




baserate = 88
pam = 32
channel = 1
connection_expectation = 30


def test_1(ser, pam, baserate, channel):
    ser.write(b'\r')  # Войти в модем
    if go('m\r'):
        set_br(pam, baserate, channel)
        print('set br complete')
        time.sleep(connection_expectation)
        check_status()
    else:
        print('no connection?')
    ser.close()


if __name__ == '__main__':
    io_data = com_init(sys.argv)
    # test_1(io_data, pam, baserate, channel)
    set_br(io_data, 32, 64, 1)
    io_data["parameter"].close()
