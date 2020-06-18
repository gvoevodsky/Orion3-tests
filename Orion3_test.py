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

while True:
    test_method = input('Enter test method:')
    if test_method in method_pull: break
    else: print('Wrong method')


pam = input('Enter pam:')
baserate = input('Enter baserate:')


