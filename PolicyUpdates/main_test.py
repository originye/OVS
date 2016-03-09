from policy_update import *
from seq_trie import Seq, SeqTrie
import multiprocessing as mp
from multiprocessing import Manager
import logging
import re
import time

logging.basicConfig(filename='failure_test.log',level=logging.DEBUG)


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
    process1 = mp.Process(target=inband_bundle, args=(s, '1', Q1, PID1, n,))
    processes.append(process1)
    process = mp.Process(target=upon_new_policy_test, args=(s, '1', Q1, PID1, n,))
    processes.append(process)
    process3 = mp.Process(target=inband_bundle, args=(s, '2', Q2, PID2, n,))
    processes.append(process3)
    process5 = mp.Process(target=upon_new_policy_test, args=(s, '2', Q2, PID2, n,))
    processes.append(process5)
    process6 = mp.Process(target=inband_bundle, args=(s, '3', Q3, PID3, n,))
    processes.append(process6)
    process8 = mp.Process(target=upon_new_policy_test, args=(s, '3', Q3, PID3, n,))
    processes.append(process8)
    process9 = mp.Process(target=inband_bundle, args=(s, '4', Q4, PID4, n,))
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


def synchronization_test_bundle():
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


def synchronization_baseline_test_bundle():
    s = ["1001"]
    s1 = ['1002']
    n = 500
    clear_config(s)
    clear_config(s1)
    processes = []
    t = time.time()
    logging.debug(str( ["START"] + [t]))
    process1 = mp.Process(target=inband_baseline_bundle, args=(s, '1', n,))
    processes.append(process1)
    process3 = mp.Process(target=inband_baseline_bundle, args=(s, '2', n,))
    processes.append(process3)
    process6 = mp.Process(target=inband_baseline_bundle, args=(s, '3', n,))
    processes.append(process6)
    process8 = mp.Process(target=inband_baseline_bundle, args=(s, '4', n,))
    processes.append(process8)
# Run processes

    for p in processes:
        p.start()
        print 'STARTING:', p, p.is_alive()
# Exit the completed processes
    for p in processes:
        p.join()
        print 'JOINED:', p, p.is_alive()

def conflict_unit_test():
    seq = Seq()
    seq_trie = SeqTrie(seq)
    i = 0
    t = 0
    while i <= 1000:
        flow_ = simulator_test()
        flow = parse_flow(flow_)
        i += 1
        pid = '%i' % i
        flow['dl_vlan'] = pid
        t1 = time.time()
        conflict_detection(seq_trie, flow)
        #print pid, flow
        seq_trie = policy_store_to_trie(seq, flow)
        t2 = time.time()
        t = t + t2 - t1
    t1 = time.time()
    t2 = time.time()
    t3 = t2 -t1
    print t,t3


def parse_flow(res):
    flow_dict = {}
    if "rejected" in res:
        return flow_dict
    items = res.split(",")
    for item in items:
        item = item.strip()
        if item == '' or item == 'ip':
            continue
        try:
            key, value = item.split("=")
        except ValueError:
            print "decoding error,", item
            print res
            continue
        if key in matching_fields_list:
            if " " in value:
                value, value1 = value.split(" ")
            if key == 'dl_vlan':
                cid, pid = value[1:2], value[2:4]
                flow_dict['cid'] = cid
                flow_dict['pid'] = pid
            flow_dict[key] = value
    return flow_dict


def conflict_system_test(n, conflict=False):
    s = ["1001"]
    s1 = ['1002']
    clear_config(s)
    clear_config(s1)

    manager1 = Manager()
    manager2 = Manager()
    manager3 = Manager()
    manager4 = Manager()

    Q1 = manager1.dict()
    failure1 = manager1.Value('i', 0)
    failed_list1 = manager1.list([])
    PID1 = manager1.list(['%02d' % i for i in xrange(1, 51)])
    Q2 = manager2.dict()
    failure2 = manager2.Value('i', 0)
    failed_list2 = manager2.list([])
    PID2 = manager2.list(['%02d' % i for i in xrange(1, 51)])
    Q3 = manager3.dict()
    failure3 = manager3.Value('i', 0)
    failed_list3 = manager3.list([])
    PID3 = manager3.list(['%02d' % i for i in xrange(1, 51)])
    Q4 = manager4.dict()
    failure4 = manager4.Value('i', 0)
    failed_list4 = manager4.list([])
    PID4 = manager4.list(['%02d' % i for i in xrange(1, 51)])
    t = time.time()
    logging.debug(str( ["START"] + [t]))
    processes = []
    process1 = mp.Process(target=policy_update_conflict_test, args=(s, '1', Q1, PID1, failure1, failed_list1, n, conflict, ))
    processes.append(process1)
    #process2 = mp.Process(target=controller_failure_detection, args=(s, '1', failure1, failed_list1,))
    #processes.append(process2)
    process = mp.Process(target=upon_new_policy_test, args=(s, '1', Q1, PID1, n, ))
    processes.append(process)
    process3 = mp.Process(target=policy_update_conflict_test, args=(s, '2', Q2, PID2, failure2, failed_list2, n, conflict, ))
    processes.append(process3)
    #process4 = mp.Process(target=controller_failure_detection, args=(s, '2', failure2, failed_list2,))
    #processes.append(process4)
    process5 = mp.Process(target=upon_new_policy_test, args=(s, '2', Q2, PID2, n, ))
    processes.append(process5)
    process6 = mp.Process(target=policy_update_conflict_test, args=(s, '3', Q3, PID3, failure3, failed_list3, n, conflict, ))
    processes.append(process6)
    #process4 = mp.Process(target=controller_failure_detection, args=(s, '2', failure2, failed_list2,))
    #processes.append(process4)
    process7 = mp.Process(target=upon_new_policy_test, args=(s, '3', Q3, PID3, n, ))
    processes.append(process7)

    process8 = mp.Process(target=policy_update_conflict_test, args=(s, '4', Q4, PID4, failure4, failed_list4, n, conflict, ))
    processes.append(process8)
    #process4 = mp.Process(target=controller_failure_detection, args=(s, '2', failure2, failed_list2,))
    #processes.append(process4)
    process9 = mp.Process(target=upon_new_policy_test, args=(s, '4', Q4, PID4, n, ))
    processes.append(process9)
# Run processes
    t = time.time()
    logging.debug(str( ["START"] + [t]))
    for p in processes:
        p.start()
        print 'STARTING:', p, p.is_alive()

# Exit the completed processes
    for p in processes:
        p.join()
        print 'JOINED:', p, p.is_alive()


def controller_failure_unit_test():
    s = ["1001"]
    s1 = ["1002"]
    clear_config(s)
    clear_config(s1)
    manager1 = Manager()
    manager2 = Manager()
    failure1 = manager1.Value('i', 0)
    failed_list1 = manager1.list([])

    failure2 = manager2.Value('i', 0)
    failed_list2 = manager2.list([])
    processes = []
    process2 = mp.Process(target=controller_failure_detection, args=(s, '1', failure1, failed_list1,))
    processes.append(process2)
    process4 = mp.Process(target=controller_failure_detection, args=(s, '2', failure2, failed_list2,))
    processes.append(process4)
    for p in processes:
        p.start()
        print 'STARTING:', p, p.is_alive()
    r = random.randint(1, 10)
    time.sleep(r)
    print 'terminated'
    t1 = time.time()
    logging.debug(str( ["controller failed at:"] + [t1]))
    processes[0].terminate()
# Exit the completed processes
    for p in processes:
        p.join()
        print 'JOINED:', p, p.is_alive()


def controller_failure_system_test(n):
    s = ["1001"]
    s1 = ["1002"]
    clear_config(s)
    clear_config(s1)
    manager1 = Manager()
    manager2 = Manager()
    manager3 = Manager()
    manager4 = Manager()
    conflict = True
    Q1 = manager1.dict()
    failure1 = manager1.Value('i', 0)
    failed_list1 = manager1.list([])
    PID1 = manager1.list(['%02d' % i for i in xrange(1, 51)])
    Q2 = manager2.dict()
    failure2 = manager2.Value('i', 0)
    failed_list2 = manager2.list([])
    PID2 = manager2.list(['%02d' % i for i in xrange(1, 51)])
    Q3 = manager3.dict()
    failure3 = manager3.Value('i', 0)
    failed_list3 = manager3.list([])
    PID3 = manager3.list(['%02d' % i for i in xrange(1, 51)])
    Q4 = manager4.dict()
    failure4 = manager4.Value('i', 0)
    failed_list4 = manager4.list([])
    PID4 = manager4.list(['%02d' % i for i in xrange(1, 51)])
    processes = []
    process1 = mp.Process(target=policy_update_conflict_test, args=(s, '1', Q1, PID1, failure1, failed_list1, n, conflict, ))
    processes.append(process1)
    process2 = mp.Process(target=controller_failure_detection, args=(s, '1', failure1, failed_list1,))
    processes.append(process2)
    process = mp.Process(target=upon_new_policy_test, args=(s, '1', Q1, PID1, n, ))
    processes.append(process)
    process3 = mp.Process(target=policy_update_conflict_test, args=(s, '2', Q2, PID2, failure2, failed_list2, n, conflict, ))
    processes.append(process3)
    process4 = mp.Process(target=controller_failure_detection, args=(s, '2', failure2, failed_list2,))
    processes.append(process4)
    process5 = mp.Process(target=upon_new_policy_test, args=(s, '2', Q2, PID2, n, ))
    processes.append(process5)
    process6 = mp.Process(target=policy_update_conflict_test, args=(s, '3', Q3, PID3, failure3, failed_list3, n, conflict, ))
    processes.append(process6)
    process7 = mp.Process(target=controller_failure_detection, args=(s, '3', failure3, failed_list3,))
    processes.append(process7)
    process8 = mp.Process(target=upon_new_policy_test, args=(s, '3', Q3, PID3, n, ))
    processes.append(process8)
    process9 = mp.Process(target=policy_update_conflict_test, args=(s, '4', Q4, PID4, failure4, failed_list4, n, conflict, ))
    processes.append(process9)
    process10 = mp.Process(target=controller_failure_detection, args=(s, '4', failure4, failed_list4,))
    processes.append(process10)
    process11 = mp.Process(target=upon_new_policy_test, args=(s, '4', Q4, PID4, n, ))
    processes.append(process11)
# Run processes
# Run processes
# Run processes
    for p in processes:
        p.start()
        print 'STARTING:', p, p.is_alive()
    time.sleep(20)
    print 'terminated'
    processes[3].terminate()
    processes[4].terminate()
    processes[6].terminate()
    processes[7].terminate()
    print 'sleeping'
    time.sleep(1)
    processes[5].terminate()
    processes[8].terminate()
    print 'terminated 5'
    time.sleep(2)

    for p in processes:
        print 'TERMINATED:', p, p.is_alive()
# Exit the completed processes
    for p in processes:
        p.join()
        print 'JOINED:', p, p.is_alive()


if __name__ == '__main__':
    #synchronization_test()
    #synchronization_test_bundle()
    synchronization_baseline_test_bundle()
    #synchronization_baseline_test()
    #conflict_unit_test()
    #conflict_system_test(500, True)
    #controller_failure_unit_test()
    #controller_failure_system_test(1000)