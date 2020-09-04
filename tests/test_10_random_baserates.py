import cli_basement_moves
import web_basement_moves
import random
from threading import Thread

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


def test_web(device, pam, baserate, channel='1', mode='Master'):
    print('Starting web test___________________________________________________________')
    web_basement_moves.get_url(device)
    web_basement_moves.configuration_menu(device)
    web_basement_moves.set_params(device, pam, baserate, channel='1', mode='Master')
    web_basement_moves.apply_confirm(device)
    web_basement_moves.close_browser(device)


def test_cli(device, pam, baserate, channel=1, mode='Master'):
    print('Starting cli test___________________________________________________________')
    cli_basement_moves.set_br(device, pam, baserate, 1, mode)

def test_cli_in_configuration_menu(device, pam, baserate, channel=1, mode='Master'):
    device.move("pam ", pam, ' ', channel, '\r')
    device.move('baserate ', baserate, ' ', channel, '\r')
    device.move('apply')


def test_main(devices):
    i = 0
    for pam in pam_pull:
        if devices[0].__class__.__name__ == 'WebAdapter':  # setting br = 20; pam = 32. now u can set any pam.
            web_basement_moves.set_params(devices[0], 32, 20, 1)
        else:
            devices[0].move('m')
            devices[0].move('3')
            devices[0].move('baserate ', 20, ' ', 1, '\r')
            devices[0].move('apply')
        random_baserate_pull = []
        for i in range(10):
            random_baserate_pull.append(random.choice(baserate_pull_to_pam[pam]))
        print(list(set(random_baserate_pull)))
        for random_baserate in list(set(random_baserate_pull)):

            list_of_threads = []
            for device in devices:
                print(device)
                if device.__class__.__name__ == 'WebAdapter':
                    thread = Thread(target=test_web, args=(device, pam, random_baserate, 1, 'Master'))
                    list_of_threads.append(thread)
                elif device.__class__.__name__ == 'ComAdapter' or device.__class__.__name__ == 'TelnetAdapter' or device.__class__.__name__ == 'SshAdapter': #we can do faster by adding device.move methods instead of test_cli()
                    if i == 0:
                        thread = Thread(target=test_cli, args=(device, pam, random_baserate, 1, 'Slave'))
                        list_of_threads.append(thread)
                        i = 1
                    else:
                        thread = Thread(target=test_cli_in_configuration_menu, args=(device, pam, random_baserate, 1, 'Slave'))
                        list_of_threads.append(thread)
                else:
                    print('Error')
                    break

            list_of_threads[0].start()
            list_of_threads[1].start()
            list_of_threads[0].join()
            list_of_threads[1].join()
            print('WAITING FOR DSL CONNECTION_______________________________________________')
            if devices[0].__class__.__name__ == 'WebAdapter':
                web_basement_moves.check_dsl_connection(devices[0])
            elif devices[
                0].__class__.__name__ == 'ComAdapter' or device.__class__.__name__ == 'TelnetAdapter' or device.__class__.__name__ == 'SshAdapter':
                cli_basement_moves.check_status(devices[0])
