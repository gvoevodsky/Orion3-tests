import time


def set_br(io_adapter, pam, baserate, channel=1, mode='Master'):
    open_cli(io_adapter)
    io_adapter.move("m")
    io_adapter.move("3")
    io_adapter.move("pam ", pam, ' ', channel, '\r')
    io_adapter.move('baserate ', baserate, ' ', channel, '\r')
    if mode == 'Master':
        io_adapter.move('master on ', channel, '\r')
    else:
        io_adapter.move('master off ', channel, '\r')
    io_adapter.move('apply')


def check_status(io_adapter):
    waiting_for_connection_time = 40
    time.sleep(waiting_for_connection_time)
    open_cli(io_adapter)
    io_adapter.move('m')
    io_adapter.move('2')
    text = io_adapter.move('status')
    a = text.find('SYNC')
    status = text[a + 33]
    time.sleep(1)
    io_adapter.move('m')
    return status


def open_cli(io_adapter):
    io_adapter.open_cli()


def reconnect(io_adapter):  # ???
    io_adapter.reconnect()
