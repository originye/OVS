import subprocess
import logging
import re
import time
from seq_trie import Seq, SeqTrie

last_pull = []
s = "s1"
Q = {}
PID = [1,2,3,4,5,6,7,8,9,10]
matching_fields_list = ['dl_vlan', 'metadata', 'in_port', 'dl_src', 'dl_dst', 'nw_src', 'nw_dst']
compare_list = ['metadata', 'in_port', 'dl_src', 'dl_dst', 'nw_src', 'nw_dst']


def policy_update(controller_id):
    seq_trie = SeqTrie()
    seq = Seq()
    while controller_failure_detection(): # return True if no controller failure
        while True:
            try:
                flow = pull(s)
                if not flow:
                    time.sleep(0.01)
                    continue
            except NameError:
                print "SwitchFailure"
                switch_failure_handler()
                raise
        if flow['cid'] == controller_id:
            if not conflict_detection(seq_trie, flow):
                p = getfromQ(flow['pid'])
                two_phase_update(p)
                remove(flow)
                seq_trie = policy_store_to_trie(seq, flow)
                free_pid(flow['pid'])
            else:
                remove(flow)


def free_pid(pid):
    del Q[pid]
    PID.append(pid)


def policy_store_to_trie(seq, flow):
    #TODO : store the installed policy in marisa_trie
    seq.update(flow)
    seq_trie = SeqTrie(seq)
    #print seq_trie.metadata.get_value(u'metadata')
    return seq_trie


def two_phase_update(policy):
    #TODO: first update internal then ingress
    return True


def getfromQ(pid):
    #TODO: get the policy with pid from Q
    try:
        policy = Q[pid]
    except KeyError:
        print "No such pid"
    return policy


def controller_failure_detection():
    return True


def switch_failure_handler():
    return True


# if detect conflict, return True
def conflict_detection(seq_trie, flow):
    #TODO: no conflict return True, otherwise return False
    none = True
    ANY = {'metadata':'ANY', 'in_port':'ANY', 'dl_src':'ANY', 'dl_dst':'ANY', 'nw_src':'ANY', 'nw_dst':'ANY'}
    pid = get_pid(seq_trie, compare_list[0], flow) + get_pid(seq_trie, compare_list[0], ANY)
    for i in xrange(1, len(compare_list)):
        pid2 = []
        if compare_list[i] in flow:
            none = False
            pid2 = get_pid(seq_trie, compare_list[i], flow)
        pid2 = pid2 + get_pid(seq_trie, compare_list[i], ANY)
        pid = set(pid).intersection(pid2)
    if none:
        return True
    else:
        if pid:
            return True
        else:
            return False


def get_pid(seq_trie, field, flow):
    if field == 'metadata':
        pid = seq_trie.metadata.get_value(unicode(flow[field]))
        return pid
    if field == 'in_port':
        pid = seq_trie.in_port.get_value(unicode(flow[field]))
        return pid
    if field == 'dl_src':
        pid = seq_trie.dl_src.get_value(unicode(flow[field]))
        return pid
    if field == 'dl_dst':
        pid = seq_trie.dl_dst.get_value(unicode(flow[field]))
        return pid
    if field == 'nw_src':
        pid = seq_trie.nw_src.get_value(unicode(flow[field]))
        return pid
    if field == 'nw_dst':
        pid = seq_trie.nw_dst.get_value(unicode(flow[field]))
        return pid


# ovs-ofctl remove switch id
def remove(flow):
    try:
        cmdline_args = ["ovs-ofctl"] + ["remove"] + flow + ["-O", "OpenFlow14"]
        #logging.debug(str( cmdline_args))
        p = subprocess.Popen(cmdline_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()
        res = [p.returncode, p.communicate()]
        #logging.debug(str( res))
        return res
        #return subprocess.check_output(cmdline_args, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError, e:
        logging.warning(str( e))
        #logging.warning(subprocess.Popen.communicate())
        return None


# pull a policy from switch return flow_dict={'metadata':'0x1123123','ip_src': '11.111.11.11'....}
def pull(switch):
    #flow = {'cid':0, 'pid': 0, 'policy': " "}
    try:
        cmdline_args = ["ovs-ofctl"] + ["pull"] + switch + ["-O", "OpenFlow14"]
        #logging.debug(str( cmdline_args))
        p = subprocess.Popen(cmdline_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()
        res = [p.returncode, p.communicate()]
        #logging.debug(str( res))
        res = res[1][0]
        #res = res[:-2]
        print res
        flow_dict = {}
        items = res.split(",")
        for item in items:
            item = item.strip()
            print item
            if item == '':
                continue
            key, value = item.split("=")
            if key in matching_fields_list:
                if " " in value:
                    value, value1 = value.split(" ")
                if key == 'dl_vlan':
                    cid, pid = value[0:2], value[2:4]
                    flow_dict['cid'] = cid
                    flow_dict['pid'] = pid
                flow_dict[key] = value
        return flow_dict
        #return subprocess.check_output(cmdline_args, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError, e:
        logging.warning(str( e))
        #logging.warning(subprocess.Popen.communicate())
        return None




# ovs-ofctl push switch id content, id= xxxx
def push(flow):
    try:
        cmdline_args = ["ovs-ofctl"] + ["push"] + flow + ["-O", "OpenFlow14"]
        #logging.debug(str( cmdline_args))
        p = subprocess.Popen(cmdline_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()
        res = [p.returncode, p.communicate()]
        #logging.debug(str( res))
        return res
        #return subprocess.check_output(cmdline_args, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError, e:
        logging.warning(str( e))
        #logging.warning(subprocess.Popen.communicate())
        return None