import subprocess
import logging
import re
import time

seq = []
last_pull = []
s = "s1"
Q = {}
PID = [1,2,3,4,5,6,7,8,9,10]
matching_fields_list = ['n_bytes', 'dl_vlan', 'metadata']


def policy_update(controller_id):
    while controller_failure_detection(): # return True if no controller failure
        while True:
            try:
                flow = pull(s)
                if not flow:
                    break
            except NameError:
                print "SwitchFailure"
                switch_failure_handler()
                raise
        if flow['cid'] == controller_id:
            if conflict_detection(seq, flow):
                p = getfromQ(flow['pid'])
                two_phase_update(p)
                remove(flow)
                policy_store(flow)
                free_pid(flow['pid'])
            else:
                remove(flow)


def free_pid(pid):
    del Q[pid]
    PID.append(pid)

def policy_store(flow):
    #TODO : store the installed policy in marisa_trie

    return True


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


def conflict_detection(seq, flow):
    #TODO: no conflict return True, otherwise return False
    return True

def remove(flow):
    #TODO: remove flow from switch s
    return True


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
                if key == 'dl_vlan':
                    value, value2 = value.split(" ")
                flow_dict[key] = value
        return flow_dict
        #return subprocess.check_output(cmdline_args, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError, e:
        logging.warning(str( e))
        #logging.warning(subprocess.Popen.communicate())
        return None

    # if flow == None:
    #     flow = " "
    #     raise NameError('SwitchFailure')
    # return flow


# ovs-ofctl push switch id content
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