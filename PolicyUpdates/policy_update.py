import subprocess
import logging
import re
import time, signal
import random
from seq_trie import Seq, SeqTrie
import multiprocessing as mp
from multiprocessing import Manager

last_pull = []
#s = ["s1"]
#PID = ['%02d' % i for i in xrange(1, 51)]  #['01','02',...]
matching_fields_list = ['dl_vlan', 'metadata', 'in_port', 'dl_src', 'dl_dst', 'nw_src', 'nw_dst']
compare_list = ['metadata', 'in_port', 'dl_src', 'dl_dst', 'nw_src', 'nw_dst']
backup_switch = ['s1', 's2', 's3', 's4', 's5']


# !! controller id  < 10, Q: store all the to-be-installed policies; failure: flag for controller failure
def policy_update(switch, controller_id, Q, PID, failure, failed_list):
    # cid = '%d' % controller_id
    cid = controller_id
    seq = Seq()
    seq_trie = SeqTrie(seq)
    while True:
        if isinstance(switch, type(Manager().list())):
            s = [switch[0]]
        else:
            s = switch
        if not failure.value:
            while True:
                try:
                    flow = pull(s)
                    if not flow:
                        time.sleep(1)
                        print "sleep", flow
                        continue
                    else:
                        break
                except NameError:
                    print "SwitchFailure"
                    s = switch_failure_handler(switch)
                    time.sleep(1)
                    continue
            if flow['cid'] == cid:
                if not conflict_detection(seq_trie, flow):
                    p = getfromQ(flow['pid'], Q)
                    #two_phase_update(p)
                    remove(s + [flow['dl_vlan']])
                    seq_trie = policy_store_to_trie(seq, flow)
                    free_pid(flow['pid'], Q, PID)
                else:
                    remove(s + [flow['dl_vlan']])
                    free_pid(flow['pid'], Q, PID)
                    print "!!removed! ", flow['dl_vlan']
        else:
            #print "main failed_list:", failed_list
            controller_failure_handler(cid, s, failed_list)
            time.sleep(2)


# return True if no controller failure
def controller_failure_detection(switch, cid, failure, failed_list):
    # TODO: heartbeat mechanisms and failure detection
    if isinstance(switch, type(Manager().list())):
        s = [switch[0]]
    else:
        s = switch
    controllers1 = controller_detector(s)
    while True:
        try:
            if isinstance(switch, type(Manager().list())):
                s = [switch[0]]
            else:
                s = switch
            heart_beat(s, cid)
            controllers2 = controller_detector(s)
            print controllers2
            if (set(controllers1).intersection(controllers2)) != set(controllers1):
                print "!!!!!!!!!!!!!!!!!failed controller detected,", cid
                print dump(s)
                for l in list(set(controllers1) - set(controllers2)):
                    failed_list.append(l)
                print "failed_list:", failed_list
                failure.value = 1
            else:
                failure.value = 0
                while len(failed_list):
                    failed_list.pop()
            controllers1 = controllers2
            time.sleep(2)
        except ValueError:
            print ValueError
            print "controller failure detection failed"


def upon_new_policy(switch, controller_id, Q, PID):
    # cid = '1%d' % controller_id
    cid = '1%s' % controller_id
    while True:
        if isinstance(switch, type(Manager().list())):
            s = [switch[0]]
        else:
            s = switch
        flow = simulator()
        pid = PID.pop(0)
        vlan = [cid + pid]
        Q[pid] = flow
        #print "new policy:", s
        push(s + vlan + [flow])
        time.sleep(5)


# simulator to generating new policy
def simulator():
    flow = policy_generator()
    return flow


def policy_generator():
    no = random.randint(1, len(compare_list))
    fields = random.sample(compare_list, no)
    flows = []
    dl_src_list = ['00:0A:E4:25:6B:B0','00:0A:E4:25:6B:A0','00:0A:E4:25:6B:C0','00:0A:E4:25:6B:D0']
    dl_dst_list = ['00:0A:E4:25:6B:BA','00:0A:E4:25:6B:AA','00:0A:E4:25:6B:CA','00:0A:E4:25:6B:DA']
    nw_src_list = ['10.10.10.10','11.11.11.11','12.12.12.12','13.13.13.13']
    nw_dst_list = ['20.20.20.20','21.21.21.21','22.22.22.22','23.23.23.23']
    for field in fields:
        if field == 'metadata':
            flows.append('metadata=0x11110000/0xffff0000')
        if field == 'in_port':
            flows.append('in_port=%d' % random.randint(1, 3))
        if field == 'dl_src':
            flows.append('dl_src=%s' % dl_src_list[random.randint(0, 3)])
        if field == 'dl_dst':
            flows.append('dl_dst=%s' % dl_dst_list[random.randint(0, 3)])
        if field == 'nw_src':
            flows.append('nw_src=%s' % nw_src_list[random.randint(0, 3)])
        if field == 'nw_dst':
            flows.append('nw_dst=%s' % nw_dst_list[random.randint(0, 3)])
    flow = 'dl_type=0x0800,' + flows[0]
    for f in flows[1:]:
        flow1 = flow + ','
        flow = flow1 + f
    return flow


def free_pid(pid, Q, PID):
    try:
        del Q[pid]
    except KeyError:
        print "Q error:", pid, Q
    PID.append(pid)
    return True


def policy_store_to_trie(seq, flow):
    seq.update(flow)
    seq_trie = SeqTrie(seq)
    #print seq_trie.metadata.get_value(u'metadata')
    return seq_trie


def two_phase_update(policy):
    # TODO: first update internal then ingress
    return True


def getfromQ(pid, Q):
    # TODO: get the policy with pid from Q
    policy = []
    try:
        policy = Q[pid]
    except KeyError:
        print "No such pid:", pid, Q
    return policy


def heart_beat(switch, cid):
    cid = '%s' % cid
    flow = switch + [cid]
    res = send_heart_beat(flow)
    if res[0]:
        print "heart beat failed"
        return False
    else:
        return True


def controller_detector(switch):
    flow = switch
    controllers = alive_controller(flow)
    #print "detector:", controllers
    return controllers


def switch_failure_handler(s):
    # TODO: handler switch failure and also how to detect switch failure
    backup_switch.remove(s[0])
    s.remove(s[0])
    s.append(backup_switch[0])
    print "switch failure handler:", s
    return [s[0]]


def controller_failure_handler(cid, s, failed_list):
    # TODO: handler switch failure and also how to detect switch failure
    print "controller failure!"
    res = lock([cid])
    if "Locked" in res:
        return None
    else:
        for c in failed_list:
            res = dump(s)
            vlan = get_vlan(res, c)
            print "vlan:", vlan
            for x in vlan:
                flow = s + [x]
                remove(flow)
            unlock([cid])
            return None


# if detect conflict, return True
def conflict_detection(seq_trie, flow):
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
            print "!!!!!!detected!"
            return True
        else:
            return False


def get_pid(seq_trie, field, flow):
    if field not in flow:
        flow[field] = 'ANY'
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


# ovs-ofctl heart-beat switch id
def send_heart_beat(flow):
    try:
        cmdline_args = ["ovs-ofctl"] + ["heart-beat"] + flow + ["-O", "OpenFlow14"]
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


# ovs-ofctl check-alive-controller switch
def alive_controller(flow):
    try:
        cmdline_args = ["ovs-ofctl"] + ["check-alive-controller"] + flow + ["-O", "OpenFlow14"]
        #logging.debug(str( cmdline_args))
        p = subprocess.Popen(cmdline_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()
        res = [p.returncode, p.communicate()]
        #logging.debug(str( res))
        res = res[1][0]
        print "alive:", res
        if len(res) > 0:
            controllers = res.split(" ")
            controllers.remove("\n")
        else:
            controllers = []
        #print "controllers:", controllers
        return controllers
        #return subprocess.check_output(cmdline_args, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError, e:
        logging.warning(str( e))
        #logging.warning(subprocess.Popen.communicate())
        return None


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


# pull a policy from switch return
# flow_dict={'pid':'11','cid':'23','dl_vlan':'2311',metadata':'0x1123123','ip_src': '11.111.11.11'....}
def pull(switch):
    #flow = {'cid':0, 'pid': 0, 'policy': " "}
    try:
        cmdline_args = ["ovs-ofctl"] + ["pull"] + switch + ["-O", "OpenFlow14"]
        #logging.debug(str( cmdline_args))
        p = subprocess.Popen(cmdline_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()
        res1 = [p.returncode, p.communicate()]
        if res1[0]:
            raise NameError("switch failed")
        #logging.debug(str( res))
        res = res1[1][0]
        #res = res[:-2]
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
        # return subprocess.check_output(cmdline_args, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError, e:
        logging.warning(str( e))
        # logging.warning(subprocess.Popen.communicate())
        return None


# ovs-ofctl push switch id content, id= xxxx
def push(flow):
    try:
        cmdline_args = ["ovs-ofctl"] + ["push"] + flow + ["-O", "OpenFlow14"]
        # logging.debug(str( cmdline_args))
        p = subprocess.Popen(cmdline_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()
        res = [p.returncode, p.communicate()]
        # logging.debug(str( res))
        return res
        # return subprocess.check_output(cmdline_args, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError, e:
        logging.warning(str( e))
        # logging.warning(subprocess.Popen.communicate())
        return None


# clear configuration
def clear_config(switch):
    try:
        cmdline_args = ["ovs-ofctl"] + ["del-flows"] + switch + ["-O", "OpenFlow14"]
        # logging.debug(str( cmdline_args))
        p = subprocess.Popen(cmdline_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()
        res = [p.returncode, p.communicate()]
        # logging.debug(str( res))
        return res
        # return subprocess.check_output(cmdline_args, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError, e:
        logging.warning(str( e))
        # logging.warning(subprocess.Popen.communicate())
        return None


# ovs-ofctl lock switch controller_id
def lock(flow):
    try:
        cmdline_args = ["ovs-ofctl"] + ["lock"] + flow + ["-O", "OpenFlow14"]
        # logging.debug(str( cmdline_args))
        p = subprocess.Popen(cmdline_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()
        res = [p.returncode, p.communicate()]
        # logging.debug(str( res))
        return res[1][0]
        # return subprocess.check_output(cmdline_args, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError, e:
        logging.warning(str( e))
        # logging.warning(subprocess.Popen.communicate())
        return None


# ovs-ofctl unlock switch controller_id
def unlock(flow):
    try:
        cmdline_args = ["ovs-ofctl"] + ["unlock"] + flow + ["-O", "OpenFlow14"]
        # logging.debug(str( cmdline_args))
        p = subprocess.Popen(cmdline_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()
        res = [p.returncode, p.communicate()]
        # logging.debug(str( res))
        return res[1][0]
        # return subprocess.check_output(cmdline_args, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError, e:
        logging.warning(str( e))
        # logging.warning(subprocess.Popen.communicate())
        return None


# dump all the policies on the switch
def dump(switch):
    try:
        cmdline_args = ["ovs-ofctl"] + ["dump-flows"] + switch + ["table=246"] + ["-O", "OpenFlow14"]
        # logging.debug(str( cmdline_args))
        p = subprocess.Popen(cmdline_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()
        res = [p.returncode, p.communicate()]
        # logging.debug(str( res))
        return res[1][0]
        # return subprocess.check_output(cmdline_args, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError, e:
        logging.warning(str( e))
        # logging.warning(subprocess.Popen.communicate())
        return None


def get_vlan(res, cid):
        vlan = []
        flows = res.split("\n")[1:]
        for flow in flows:
            items = flow.split(",")
            for item in items:
                item = item.strip()
                if item == '':
                    continue
                if "dl_vlan" in item:
                    if "action" in item:
                        item, action = item.split(" ")
                    key, value = item.split("=")
                    if value[1:2] == cid:
                        vlan.append(value)
        return vlan