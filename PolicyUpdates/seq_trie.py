import marisa_trie


class Seq:
    dl_vlan = []
    metadata = []
    in_port = []
    dl_src = []
    dl_dst = []
    nw_src = []
    nw_dst = []
    matching_fields_list = ['dl_vlan', 'metadata', 'in_port', 'dl_src', 'dl_dst', 'nw_src', 'nw_dst']

    def __init__(self):
        print "hi"

    def update(self, flows):
        for flow in self.matching_fields_list:
            if flow in flows:
                if flow == 'dl_vlan':
                    self.dl_vlan.append(flows['dl_vlan'])
                if flow == 'metadata':
                    self.metadata.append(unicode(flows['metadata']))
                if flow == 'in_port':
                    self.in_port.append(unicode(flows['in_port']))
                if flow == 'dl_src':
                    self.dl_src.append(unicode(flows['dl_src']))
                if flow == 'dl_dst':
                    self.dl_dst.append(unicode(flows['dl_dst']))
                if flow == 'nw_src':
                    self.nw_src.append(unicode(flows['nw_src']))
                if flow == 'nw_dst':
                    self.nw_dst.append(unicode(flows['nw_dst']))
            else:
                if flow == 'metadata':
                    self.metadata.append(u'ANY')
                if flow == 'in_port':
                    self.in_port.append(u'ANY')
                if flow == 'dl_src':
                    self.dl_src.append(u'ANY')
                if flow == 'dl_dst':
                    self.dl_dst.append(u'ANY')
                if flow == 'nw_src':
                    self.nw_src.append(u'ANY')
                if flow == 'nw_dst':
                    self.nw_dst.append(u'ANY')


class SeqTrie:

    def __init__(self, seq):
        self.nw_dst = marisa_trie.BytesTrie(zip(seq.nw_dst, seq.dl_vlan))
        self.nw_src = marisa_trie.BytesTrie(zip(seq.nw_src, seq.dl_vlan))
        self.metadata = marisa_trie.BytesTrie(zip(seq.metadata, seq.dl_vlan))
        self.in_port = marisa_trie.BytesTrie(zip(seq.in_port, seq.dl_vlan))
        self.dl_dst = marisa_trie.BytesTrie(zip(seq.dl_dst, seq.dl_vlan))
        self.dl_src = marisa_trie.BytesTrie(zip(seq.dl_src, seq.dl_vlan))







