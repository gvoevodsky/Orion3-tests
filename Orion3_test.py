import subprocess
import Orion3com
import Orion3web
import Orion3telnet

# output = subprocess.check_output('ipconfig')


method_pull = ['web', 'com', 'telnet']
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

while True:
    test_method = input('Enter test method:')
    if test_method in method_pull:
        break
    else:
        print('Wrong method')

while True:
    pam = input('Enter pam:')
    if pam.isdigit():
        if int(pam) in pam_pull:
            break
        else:
            print('Wrong pam, possible options: 4,8,16,32,64,128')
    else:
        print('pam is not digit')

while True:
    baserate = input('Enter baserate:')
    if baserate.isdigit():
        if int(baserate) in baserate_pull_to_pam[int(pam)]:
            break
        else:
            print('with pam = ', pam, 'baserate should be in range', baserate_pull_to_pam[int(pam)][0], '-',
                  baserate_pull_to_pam[int(pam)][-1])
            print(baserate_pull_to_pam)
    else:
        print('baserate is not digit')

if __name__ == '__main__123':
    if test_method == 'web':
        Orion3web.test_first(int(pam), int(baserate)) # перенести прием аргументов в функии тестов в кажом модуле
    elif test_method == 'com':
        Orion3com.set_br(int(pam), int(baserate))  # доделать
    else:
        Orion3telnet.set_br(int(pam), int(baserate))

print(test_method, pam, baserate)
