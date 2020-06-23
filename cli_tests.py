#def set_br(io_adapter, pam, baserate, channel):
#    io_adapter.send("3\r")
#    io_adapter.send("m\r")
#    io_adapter.send("pam ", pam, ' ', channel, '\r')
#    io_adapter.send('baserate ', baserate, ' ', channel, '\r')
#    io_adapter.send('m\r')
#    io_adapter.send('2\r')
#    io_adapter.send('apply\r')
#    io_adapter.send('m\r')
#    io_adapter.send("m\r")

def set_br(io_adapter, pam, baserate, channel):
    io_adapter.send("3\n")
    io_adapter.send("m\n")
    io_adapter.send("pam ", pam, ' ', channel, '\n')
    io_adapter.send('baserate ', baserate, ' ', channel, '\n')
    io_adapter.send('m\n')
    io_adapter.send('2\n')
    io_adapter.send('apply\n')
    io_adapter.send('m\n')
    io_adapter.send("m\n")


def check_status(io_adapter):
    io_adapter.send('2\r')
    io_adapter.send('m\r')
    io_adapter.send('2\r')
    io_adapter.send('status\r')
    text = io_adapter.send('\r')
    a = text.find('SYNC')
    print(text[a + 33])
    if text[a + 33] == '1':
        print('test passed')
    elif text[a + 33] == '-':
        print('no dsl connection')
    else:
        print('some error')
    io_adapter.send('m\r')

def open_cli(io_adapter):
    io_adapter.open_cli()