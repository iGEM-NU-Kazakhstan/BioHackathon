"""
Welcome to SeqAI system!

It's brand new program to detect sites of restrictions
and ORFs in given DNA chain.

In SeqAI.ModelAutoencoders you can access to DL models,
which is realised in our code

In SeqAI.Mutations you will find algorithms of mutagene-
sis and checking of mutated DNA.

In SeqAI.SeqProcessing you can see algorithms to prepare
and check input data.

Base functions of hiding restriction sites are given in
SeqAI python folder.

Good luck!
"""
# from Bio import SeqIO
# from SeqAI import DetectRestriction

'''Choose your DNA string'''
# dna_seq=

'''Or upload it from .fasta (or another) file'''
# seq_list=[str(seq_record.seq) for seq_record in SeqIO.parse("file_name.fasta", "fasta")]

'''Choose the site of restriction or just use the name of enzyme'''
'''SeqAI can recognize restriction sites of 1028 enzymes, in case
enzyme isn't in our database, you can easily input your own restriction site'''

# restriction_site=
# or
# enzyme =

'''Hide chosen restriction sites harmless to ORFs' of your DNA'''
# hide RS by restriction site's sequence
# DetectRestriction().detect(dna_seq, site = restriction_site)

# hide RS by enzyme name
# DetectRestriction().detect(dna_seq, enzyme = enzyme)

'''Or use for loop to hide restriction sites in multiple sequences'''
# for i in seq_list:
#     DetectRestriction().detect(dna_seq, site = restriction_site)

'''If you want to save the result of RS hide use another function:'''
# alter_results = DetectRestriction().detect(dna_seq, enzyme = enzyme)
# or
# alter_results = DetectRestriction().detect(dna_seq, site = restriction_site)



