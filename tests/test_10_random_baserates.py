import cli_basement_moves
import web_basement_moves
import random
from threading import Thread
import logs
import time

logs.logger.warning(f'{__name__} started')

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
    logs.logger.info('Starting web test___________________________________________________________')
    web_basement_moves.get_url(device)
    web_basement_moves.configuration_menu(device)
    web_basement_moves.set_params(device, pam, baserate, '1', mode)
    web_basement_moves.apply_confirm(device)
    web_basement_moves.close_browser(device)


def test_cli(device, pam, baserate, channel=1, mode='Master'):
    logs.logger.info('Starting cli test___________________________________________________________')
    device.reconnect()
    cli_basement_moves.set_br(device, pam, baserate, 1, mode)


def test_cli_in_configuration_menu(device, pam, baserate, channel=1):
    device.reconnect()
    device.move('3')
    device.move("pam ", pam, ' ', channel, '\r')
    device.move('baserate ', baserate, ' ', channel, '\r')
    device.move('apply')


def test_main(devices):
    i = 0
    for pam in pam_pull:

        for device in devices:
            if device == devices[0]:
                if device.__class__.__name__ == 'WebAdapter':  # setting br = 20; pam = 32. now u can set any pam.
                    test_web(device, 32, 20, '1', 'Master')
                else:
                    device.open_cli()
                    device.move('m')
                    device.move('3')
                    device.move('baserate ', 20, ' ', 1, '\r')
                    device.move('master on ', 1, '\r')
                    device.move('ext on ', 1, '\r')
                    device.move('apply')
            else:
                if device.__class__.__name__ == 'WebAdapter':  # setting br = 20; pam = 32. now u can set any pam.
                    test_web(device, 32, 20, '1', 'Slave')
                else:
                    device.open_cli()
                    device.move('m')
                    device.move('3')
                    device.move('baserate ', 20, ' ', 1, '\r')
                    device.move('master off ', 1, '\r')
                    device.move('ext on ', 1, '\r')
                    device.move('apply')

        logs.logger.info('Baserate 20 was set!\nWaiting 30 sec!')
        time.sleep(30)

        random_baserate_pull = []
        for i in range(10):
            random_baserate_pull.append(random.choice(baserate_pull_to_pam[pam]))
        logs.logger.warning(list(set(random_baserate_pull)))
        for random_baserate in list(set(random_baserate_pull)):

            list_of_threads = []
            for device in devices:
                if device.__class__.__name__ == 'WebAdapter':
                    if device == devices[0]:
                        thread = Thread(target=test_web, args=(device, pam, random_baserate, 1, 'Master'))
                    else:
                        thread = Thread(target=test_web, args=(device, pam, random_baserate, 1, 'Slave'))
                    list_of_threads.append(thread)
                elif device.__class__.__name__ == 'ComAdapter' or device.__class__.__name__ == 'TelnetAdapter' or device.__class__.__name__ == 'SshAdapter':  # we can do faster by adding device.move methods instead of test_cli()
                    if i == 0:
                        if device == devices[0]:
                            thread = Thread(target=test_cli, args=(device, pam, random_baserate, 1, 'Master'))
                        else:
                            thread = Thread(target=test_cli, args=(device, pam, random_baserate, 1, 'Slave'))
                        list_of_threads.append(thread)
                        i = 1
                    else:
                        if device == devices[0]:
                            thread = Thread(target=test_cli_in_configuration_menu,
                                            args=(device, pam, random_baserate, 1))
                        else:
                            thread = Thread(target=test_cli_in_configuration_menu,
                                            args=(device, pam, random_baserate, 1))
                        list_of_threads.append(thread)
                else:
                    logs.logger.error('Wrong Device Class!!')
                    break

            list_of_threads[0].start()
            list_of_threads[1].start()
            list_of_threads[0].join()
            list_of_threads[1].join()
            logs.logger.info('WAITING FOR DSL CONNECTION_______________________________________________')
            if devices[0].__class__.__name__ == 'WebAdapter':
                devices[0].reconnect()
                result = web_basement_moves.check_dsl_connection(devices[0])
                if result == '1':
                    logs.logger.warning(f'DSL connection established for pam:{pam} and baserate:{random_baserate}')
                elif result == '0':
                    logs.logger.error(f'no dsl connection for pam:{pam} and baserate:{random_baserate}')
                else:
                    logs.logger.error(f'check status fail ({result}) for pam:{pam} and baserate:{random_baserate}')

            elif devices[
                0].__class__.__name__ == 'ComAdapter' or device.__class__.__name__ == 'TelnetAdapter' or device.__class__.__name__ == 'SshAdapter':
                devices[0].reconnect()
                result = cli_basement_moves.check_status(devices[0])
                if result == '1':
                    logs.logger.warning(f'DSL connection established for pam:{pam} and baserate:{random_baserate}')
                elif result == '-':
                    logs.logger.error(f'no DSL connection for pam:{pam} and baserate:{random_baserate}')
                else:
                    logs.logger.error(f'check status fail ({result}) for pam:{pam} and baserate:{random_baserate}')
