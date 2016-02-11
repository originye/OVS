from policy_update import *
s= ["s1"]
flow = pull(s)
print bool(flow)
print flow['dl_vlan']
#print b



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
