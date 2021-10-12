import re
from Bio import SeqIO
from itertools import takewhile

start_codons=['ATG', 'atg']
stop_codons=['TAA', 'TAG', 'TGA', 'taa', 'tag', 'tga']

def end_of_loop():
    raise StopIteration


class AIORFpreproc():

    def length(self, list, length, it):
        new_list = [i[:length] for i in list]
        for k in range(it):
            new_list += [i[length * (k + 1):length * (k + 2)] for i in list]
        return new_list

    def list_of_zeros(self, lists):
        list_of_seq = [ORF().get_zeros(i) for i in lists]
        return list_of_seq


class ORF():

    def kmer(self, sequense, k=3):
        seqlist = [sequense[i:i + k] for i in range(len(sequense) - k + 1)]
        return seqlist

    def kler(self, sequence, g, k=3):
        seqlist=''
        for i in range(g, len(sequence),k):
            if sequence[i:i+k] not in stop_codons:
                seqlist+=sequence[i:i+k]
            else:
                break
        return seqlist

    def findstart(self, seq):
        start=[i for i in range(len(seq)-3) if seq[i:i+3] in start_codons]
        return start

    def get_matrix(self, seq):
        start_pos = self.findstart(seq)
        if start_pos!=[]:
            start = start_pos[0]
            sequence='-'* (start) + self.kler(seq, start)
            if len(start_pos)>=2:
                for i in start_pos:
                    if i < len(sequence):
                        continue
                    else:
                        sequence+='-'* (i-len(sequence))+self.kler(seq, start)
            if len(sequence) < len(seq):
                sequence+='-'* (len(seq)-len(sequence))
            else:
                sequence=sequence[:len(seq)]
        else:
            sequence = '-'* len(seq)
        return sequence

    def get_zeros(self, list1):
        list_zeros = self.get_matrix(list1)
        new_seq = ['0' if i=='-' else '1' for i in list_zeros]
        new_seq = ''.join(new_seq)
        return new_seq

    def get_zeros_list(self, list1):
        list_zeros = self.get_matrix(list1)
        new_seq = [0 if i=='-' else 1 for i in list_zeros]
        return new_seq


class RestrictionDeterminer():

    def __init__(self, site, sequence):
        self.site = site
        self.sequence = sequence


    def kmer(self):
        seqlist = [self.sequence[i:i + len(self.site)] for i in range(len(self.sequence) - len(self.site) + 1)]
        seqlist += ['0' for i in range(len(self.site)-1)]
        return seqlist


    def CreateMap(self):
        sequence = self.kmer()
        new_seq = [1 if re.findall(self.site, i)!=[] else 0 for i in sequence]
        for i, k in zip(new_seq, range(len(new_seq))):
            if i != 1:
                continue
            elif i==1:
                for z in range(len(self.site)):
                    new_seq[k+z]='1'
        new_seq = [str(i) for i in new_seq]
        return ''.join(new_seq)

    def CreateLabel(self):
        sequence = self.kmer()
        if re.findall(self.site, self.sequence)!=[]:
            new_seq = 1
        else:
            new_seq = 0
        return new_seq


class Slicer():
    def __init__(self, seq):
        self.seq = seq

    def go(self):
        of_seq = int(len(self.seq)/500)
        new_seqs = [self.seq[i*500 : (i+1)*500] for i in range(of_seq)]
        new_seqs += [self.seq[of_seq*500:]+('0'*(500-int(len(self.seq)%500)))]
        return new_seqs




