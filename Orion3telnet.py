import telnetlib
import time

host = "192.168.0.222"
port = 23
timeout = 10
delay = 1
n = 0


def go(*pargs):
    global delay
    text = session.read_very_eager().decode('utf-8')
    print(text)
    for arg in pargs:
        session.write(bytes(str(arg), encoding='utf-8'))
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
    session.write(b"\r")
    go('m\r')
    # go('m\r')
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
    session = telnetlib.Telnet(host, port, timeout)
    session.write(b"\r")
    go('m\r')  # Войти в модем
    if go('m\r'):
        set_br(pam, baserate, channel)
        print('set br complete')
        time.sleep(connection_expectation)
        check_status()  # problem here!
    else:
        print('no connection?')
    session.close()
