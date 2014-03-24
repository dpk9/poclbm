
'''
Run guiminer for a certain time.
    argv[1] (int) = time to run guiminer for, in h:m:s format.
        (e.g. '2:15:30' runs for 2 h, 15 m, and 30 s)
    If argv[1] == 0 or is omitted, run guiminer until closed manually.

'''

import sys
import os
import signal
import time
import win32api

from subprocess import Popen, PIPE #, CREATE_NEW_CONSOLE
from time import sleep


# miner_path = 'C:\Program Files (x86)\guiminer'
miner_path = 'C:\Users\David\Documents\GitHub\poclbm'
miner_exe = 'poclbm.py jammastajew.lenovonvidia:asdf1234@api2.bitcoin.cz:8332 --device=0 --platform=1 --verbose -r 10'

os.chdir(miner_path)

miner_fullpath = 'python {}'.format(os.path.join(miner_path, miner_exe))
print '\n\nminer_fullpath:\n{}'.format(miner_fullpath)

if len(sys.argv) > 1:
    time_hms = sys.argv[1]
else:
    time_hms = '0:0:0'

if '--help' in sys.argv or '-h' in sys.argv:
    print __doc__
    quit()

try:
    [h, m, s] = time_hms.split(':')
except:
    raise ValueError('argv[1] should be `h:m:s`. Got {}'.format(time_hms))

try:
    h = int(h)
    m = int(m)
    s = int(s)
except:
    raise TypeError("h, m, and s should be <type 'int'>. Got: \nh: {}\nm: {}\ns: {}".format(type(h), type(m), type(s)))


time_s = s + (m*60) + (h*(60**2))

start_time = time.time()
exp_end_time = start_time+time_s

print '\n{}h : {}m : {}s\n'.format(h, m, s)
print 'Total time in s: {}'.format(time_s)
print 'Start time: {}'.format(time.ctime(start_time))
print 'End time  : {}'.format(time.ctime(exp_end_time))

ctrlc = False

try:
    print "Running guiminer:"
    print miner_exe
    miner_proc = Popen(miner_fullpath)

    print "setting powercfg to High Performance"
    os.system('powercfg -setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c') # High Performance
    

    if time_s == 0:
        pass
    else:
        sleep(time_s)
        miner_proc.kill()
except KeyboardInterrupt:
    sigint_end_time = time.time()
    time.sleep(1)
    print 'Expected end time: {}'.format(time.ctime(exp_end_time))
    print 'Actual end time:   {}'.format(time.ctime(sigint_end_time))
    print 'How early?         {}'.format(time.strftime('%H:%M:%S', time.gmtime(exp_end_time - sigint_end_time)))
    ctrlc = True
finally:
    print "it's done"
    if not ctrlc:
        print 'Ran for {}'.format(time.strftime('%H:%M:%S', time.gmtime(time.time() - start_time)))
    time.sleep(1)
    print "setting powercfg to Balanced"
    os.system('powercfg -setactive 381b4222-f694-41f0-9685-ff5bb260df2e') # Balanced




# def signal_handler(signal, frame):
#     print('You pressed Ctrl+C!')
