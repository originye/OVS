from policy_update import *
from seq_trie import Seq, SeqTrie
import multiprocessing as mp
from multiprocessing import Manager
import logging
import re
import time

logging.basicConfig(filename='test.log',level=logging.DEBUG)


def synchronization_test():
    s = ["1001"]
    s1 = ['1002']
    n = 500
    clear_config(s)
    clear_config(s1)
    manager1 = Manager()
    manager2 = Manager()
    manager3 = Manager()
    manager4 = Manager()
    t = time.time()
    logging.debug(str( ["START"] + [t]))
    Q1 = manager1.dict()
    PID1 = manager1.list(['%02d' % i for i in xrange(1, 51)])
    Q2 = manager2.dict()
    PID2 = manager2.list(['%02d' % i for i in xrange(1, 51)])
    Q3 = manager3.dict()
    PID3 = manager3.list(['%02d' % i for i in xrange(1, 51)])
    Q4 = manager4.dict()
    PID4 = manager4.list(['%02d' % i for i in xrange(1, 51)])
    processes = []
    process1 = mp.Process(target=inband, args=(s, '1', Q1, PID1, n,))
    processes.append(process1)
    process = mp.Process(target=upon_new_policy_test, args=(s, '1', Q1, PID1, n,))
    processes.append(process)
    process3 = mp.Process(target=inband, args=(s, '2', Q2, PID2, n,))
    processes.append(process3)
    process5 = mp.Process(target=upon_new_policy_test, args=(s, '2', Q2, PID2, n,))
    processes.append(process5)
    process6 = mp.Process(target=inband, args=(s, '3', Q3, PID3, n,))
    processes.append(process6)
    process8 = mp.Process(target=upon_new_policy_test, args=(s, '3', Q3, PID3, n,))
    processes.append(process8)
    process9 = mp.Process(target=inband, args=(s, '4', Q4, PID4, n,))
    processes.append(process9)
    process10 = mp.Process(target=upon_new_policy_test, args=(s, '4', Q4, PID4, n,))
    processes.append(process10)
# Run processes

    for p in processes:
        p.start()
        print 'STARTING:', p, p.is_alive()
# Exit the completed processes
    for p in processes:
        p.join()
        print 'JOINED:', p, p.is_alive()


def synchronization_baseline_test():
    s = ["1001"]
    s1 = ['1002']
    n = 500
    clear_config(s)
    clear_config(s1)
    processes = []
    t = time.time()
    logging.debug(str( ["START"] + [t]))
    process1 = mp.Process(target=inband_baseline, args=(s, '1', n,))
    processes.append(process1)
    process3 = mp.Process(target=inband_baseline, args=(s, '2', n,))
    processes.append(process3)
    process6 = mp.Process(target=inband_baseline, args=(s, '3', n,))
    processes.append(process6)
    process8 = mp.Process(target=inband_baseline, args=(s, '4', n,))
    processes.append(process8)
# Run processes

    for p in processes:
        p.start()
        print 'STARTING:', p, p.is_alive()
# Exit the completed processes
    for p in processes:
        p.join()
        print 'JOINED:', p, p.is_alive()

if __name__ == '__main__':
    synchronization_test()
   # synchronization_baseline_test()
