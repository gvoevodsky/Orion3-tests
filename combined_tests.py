from cli_tests import set_br, check_status
import random
import time



pam_pull = [4, 8, 16, 32, 64, 128]
baserate_pull_pam4 = [i for i in range(2, 40)]
baserate_pull_pam8 = [i for i in range(3, 80)]
baserate_pull_pam16 = [i for i in range(1, 120)]
baserate_pull_pam32 = [i for i in range(1, 160)]
baserate_pull_pam64 = [i for i in range(2, 200)]
baserate_pull_pam128 = [i for i in range(4, 239)]
all_baserate_pulls = [baserate_pull_pam4, baserate_pull_pam8, baserate_pull_pam16, baserate_pull_pam32,
                      baserate_pull_pam64, baserate_pull_pam128]

baserate_pull_to_pam = dict(zip(pam_pull, all_baserate_pulls))


#def test_1(io_adapter, io_adapter_slave = None):  # For each pam checking 10 random baserates for set_br -> check_status
#    for pam in pam_pull:
#        random_pam_pull = []
#        for i in range(10):
#            random_pam_pull.append(random.choice(baserate_pull_to_pam[pam]))
#        print(list(set(random_pam_pull)))
#        io_adapter.move('m')
#        io_adapter.move('3')
#        io_adapter.move('baserate ', random.randint(5, 39), ' ', 1, '\r')
#        io_adapter.move('m')
#        for random_pam in list(set(random_pam_pull)):
#            set_br(io_adapter, pam, random_pam, 1)
#            print('Waiting 5 sec______________________________________________________________')
#            time.sleep(5)
#            io_adapter.reconnect()
#            #check_status(io_adapter)

def test_1(devices):  # For each pam checking 10 random baserates for set_br -> check_status
    for pam in pam_pull:
        random_baserate_pull = []
        for i in range(10):
            random_baserate_pull.append(random.choice(baserate_pull_to_pam[pam]))
        print(list(set(random_baserate_pull)))
        #io_adapter.move('m')
        #io_adapter.move('3')
        #io_adapter.move('baserate ', random.randint(5, 39), ' ', 1, '\r')
        #io_adapter.move('m')
        for random_baserate in list(set(random_baserate_pull)):
            for device in devices:
                if device.__class__.__name__ == 'WebAdapter':
                    Web_tests.set_br(device, pam, random_baserate, 1)
                elif device.__class__.__name__ == 'ComAdapter' or device.__class__.__name__ == 'TelnetAdapter' or device.__class__.__name__ == 'SshAdapter':
                    Cli_tests.set_br(device, pam, random_baserate, 1)
                print('Waiting 5 sec______________________________________________________________')
                time.sleep(5)

            if device.__class__.__name__ == 'WebAdapter':
                Web_tests.check_status(devices[0])
            elif device.__class__.__name__ == 'ComAdapter' or device.__class__.__name__ == 'TelnetAdapter' or device.__class__.__name__ == 'SshAdapter':
                Cli_tests.check_status(devices[0])
            # переименовать файлы и имена тестов

            set_br(io_adapter, pam, random_baserate, 1)
            print('Waiting 5 sec______________________________________________________________')
            time.sleep(5)
            io_adapter.reconnect()
            #check_status(io_adapter)