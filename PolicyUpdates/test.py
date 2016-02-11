from policy_update import *
from seq_trie import Seq, SeqTrie

# matching_fields_list = ['dl_vlan', 'metadata', 'in_port', 'dl_src', 'dl_dst', 'nw_src', 'nw_dst']
# #
# s= ["s1"]
# flow = pull(s)
# flow1 = {'cid':'11','pid':'11','dl_vlan':'1111','in_port':'1','metadata':'0x111'}
# x = Seq()
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
    seq_trie = policy_store_to_trie(seq, flow2)
    #seq.update(flow2)
    print seq.dl_vlan
    print conflict_detection(seq_trie, flow1)

conflict_test()

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



