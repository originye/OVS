import marisa_trie

keys = [u'ethernet src', u'ethernet dst', u'ip src', u'ip dst', u'ip src']
keys2 = [u'ethernet src', u'ethernet dst', u'ip src', u'ip dst', u'ip src']
values2 = ['(1,ee:13)', 'ff:12', '10.110.110.10', '112.112.11.11', '123.123.12.12']
#
#trie = marisa_trie.Trie([u'ethernet src', u'ethernet dst', u'ip src', u'ip dst'])
#
values = ['(1,ee:12)', 'ff:22', '10.10.10.10', '11.11.11.11', '12.12.12.12']
keys = keys + keys2
values = values + values2
#values = [(1, 2), (2, 1), (3, 3), (2, 1)]
#fmt = '@Hf'
#trie = marisa_trie.RecordTrie(fmt, zip(keys, values))
trie = marisa_trie.BytesTrie(zip(keys, values))


keys = [u'ethernet src', u'ethernet dst', u'ip src', u'ip dst', u'ip src']
values = [(1, 2), (2, 1), (3, 3), (2, 1)]
fmt = '@Hf'
trie = marisa_trie.RecordTrie(fmt, zip(keys, values))


keys = [u'ee:12', u'ff:aa'] # store all the ethernet src value
values_id = ['222', '3333'] # store all its policy id
ethernet_src_trie = marisa_trie.BytesTrie(zip(keys, values))
ethernet_src_trie.get_value(u'ee:12') # search if thsi ethernet and return its id, if not found ,return empty