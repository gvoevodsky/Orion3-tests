
def set_br(io_adapter, pam, baserate, channel):
    io_adapter.move("m")
    io_adapter.move("m")
    io_adapter.move("3")
    io_adapter.move("pam ", pam, ' ', channel, '\r')
    io_adapter.move('baserate ', baserate, ' ', channel, '\r')
    io_adapter.move('m')
    io_adapter.move('2')
    io_adapter.move('apply')
    io_adapter.move('m')
    io_adapter.move("m")

def check_status(io_adapter):
    io_adapter.move('2')
    io_adapter.move('m')
    io_adapter.move('2')
    io_adapter.move('status')
    text = io_adapter.move('')
    a = text.find('SYNC')
    print(text[a + 33])
    if text[a + 33] == '1':
        print('test passed')
    elif text[a + 33] == '-':
        print('no dsl connection')
    else:
        print('some error')
    io_adapter.move('m')

def open_cli(io_adapter):
    io_adapter.open_cli()

def test_1():


'''
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
        
    io_data = com_init(sys.argv)
    # test_1(io_data, pam, baserate, channel)
    set_br(io_data, 32, 64, 1)
    io_data["parameter"].close()
'''