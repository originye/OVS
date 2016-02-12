from policy_update import *
from seq_trie import Seq, SeqTrie

# matching_fields_list = ['dl_vlan', 'metadata', 'in_port', 'dl_src', 'dl_dst', 'nw_src', 'nw_dst']
# #
# s= ["s1"]
# push(["s1"] + ["1234"] + ["metadata=1234,in_port=1,ip_src=10.10.10.10"])
# flow = pull(s)
# # flow1 = {'cid':'11','pid':'11','dl_vlan':'1111','in_port':'1','metadata':'0x111'}
# print flow
# x = Seq()
# seq_trie = policy_store_to_trie(x, flow)
# remove(["s1"] + ["1234"])
# push(["s1"] + ["1222"] + ["metadata=1234,in_port=2,ip_src=10.10.10.10"])
# flow1 = pull(s)
# print conflict_detection(seq_trie, flow1)
# x.update(flow1)
# print flow1
# print x.dl_dst
# seq = SeqTrie(x)
# print seq.metadata.get_value(u'0x111')
# # s= ["s1"]
# # flow = pull(s)
# # print flow
# # print flow['cid']
#print b

#compare_list = ['metadata', 'in_port', 'dl_src', 'dl_dst', 'nw_src', 'nw_dst']

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
    push(["s1"] + ["1234"] + ["metadata=1234,in_port=1,ip_src=10.10.10.10"])
    flow = pull(s)
    # flow1 = {'cid':'11','pid':'11','dl_vlan':'1111','in_port':'1','metadata':'0x111'}
    print flow
    x = Seq()
    seq_trie = policy_store_to_trie(x, flow)
    remove(["s1"] + ["1234"])
    push(["s1"] + ["1222"] + ["metadata=1234,in_port=2,ip_src=10.10.10.10"])
    flow1 = pull(s)
    print flow1
    print conflict_detection(seq_trie, flow1)


def policy_update_test(cid):
    s = ["s1"]
    clear_config(s)
    push(["s1"] + ["1234"] + ["metadata=1234,in_port=1,ip_src=10.10.10.10"])
    flow = pull(s)
    print flow
    policy_update(cid)



#conflict_test()
policy_update_test(12)
#print conflict_test() == True
# flow_dict = {}
# items = a.split(",")
# print items
# for item in items:
#     item = item.strip()
#     print item
#     if item == '':
#         continue
#     key, value = item.split("=")
#     flow_dict[key] = value
#
# print flow_dict



