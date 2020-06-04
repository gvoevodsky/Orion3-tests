import telnetlib
import time

host = "192.168.0.223"
port = 23
timeout = 10
delay = 1
n = 0

session = telnetlib.Telnet(host, port, timeout)

print(session.read_until(b'Clock',timeout = 3).decode('utf-8'))
session.write(b"\n")
time.sleep(delay)

print(session.read_until(b'Clock',timeout = 3).decode('utf-8'))
n=+1
time.sleep(delay)

print(session.read_eager().decode('utf-8'), n)
session.write(b"3\n")
time.sleep(delay)

print(session.read_until(b'Clock').decode('ascii'))
n=+1
time.sleep(delay)

print(session.read_very_eager().decode('utf-8'), n)
n=+1
time.sleep(delay)

session.close()
