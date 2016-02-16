from policy_update import *
from seq_trie import Seq, SeqTrie
import multiprocessing as mp
from multiprocessing import  Manager


def conflict_test():
    seq = Seq()
    flow1 = {'cid':'11','pid':'11','dl_vlan':'1111','in_port':'1','metadata':'0x111'}
    flow2 = {'cid':'12','pid':'12','dl_vlan':'1212','in_port':'1','metadata':'0x111','dl_src':'ee:ee:ee:ee'}
    #seq.update(flow1)
    seq_trie = policy_store_to_trie(seq, flow1)
    #seq.update(flow2)
    print seq.dl_vlan
    print conflict_detection(seq_trie, flow2)

    s = ["s1"]
    clear_config(s)
    push(["s1"] + ["1234"] + ["metadata=1234,in_port=1,nw_src=10.10.10.10"])
    flow = pull(s)
    # flow1 = {'cid':'11','pid':'11','dl_vlan':'1111','in_port':'1','metadata':'0x111'}
    print flow
    x = Seq()
    seq_trie = policy_store_to_trie(x, flow)
    remove(["s1"] + ["1234"])
    push(["s1"] + ["1222"] + ["metadata=1234,in_port=2,nw_src=10.10.10.10"])
    flow1 = pull(s)
    print flow1
    print conflict_detection(seq_trie, flow1)


def policy_update_test(cid):
    s = ["s1"]
    clear_config(s)
    push(["s1"] + ["1234"] + ["metadata=1234,in_port=1,nw_src=10.10.10.10"])
    flow = pull(s)
    print flow
    policy_update(cid)


def simulator_test(cid):
    s = ["s1"]
    clear_config(s)
    try:
        upon_new_policy(cid)
    except KeyboardInterrupt:
        flow = pull(s)
        print "flow: %s" % flow


def heartbeat_test():
    s = ["s1"]
    heart_beat(s, 1)
    heart_beat(s, 2)
    controller_detector(s)


def main_test():
    s = ["s1"]
    #clear_config(s)
    manager = Manager()

    Q = manager.dict()
    failure = manager.Value('i', 0)
    failed_list = manager.list()
    processes=[]
    process1 = mp.Process(target=policy_update, args=(s, '1', Q, failure, failed_list,))
    processes.append(process1)
    process2 = mp.Process(target=controller_failure_detection, args=(s, '1', failure, failed_list,))
    processes.append(process2)
    process = mp.Process(target=upon_new_policy, args=(s, '1', Q,))
    processes.append(process)
# Run processes
    for p in processes:
        p.start()
        print p, p.is_alive(), p.name
# Exit the completed processes
    for p in processes:
        p.join()

#conflict_test()
#policy_update_test(12)
#simulator_test(1)
# try:
#     main_test()
# except ValueError:
#     print pull(['s1'])

# manager = Manager()
#
# failure = manager.list()
# failure.append("s")
# print failure
#
# lock(["s1"]+["1"])
# res = lock(["s1"]+["2"])
# print "Locked" in res[1][0]
# print "Locked" in res
res = dump(['s1'])
print res
vlan = get_vlan(res, "1")
print vlan
for i in vlan:
    flow = ['s1'] + [i]
    remove(flow)