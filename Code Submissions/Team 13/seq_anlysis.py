from random import choice

bases = ["A", "T", "C", "G"]
RNA_base = ["A", "U", "C", "G"]

RNA_Codons = {
    # 'M' - START, '_' - STOP
    "GCU": "A", "GCC": "A", "GCA": "A", "GCG": "A",
    "UGU": "C", "UGC": "C",
    "GAU": "D", "GAC": "D",
    "GAA": "E", "GAG": "E",
    "UUU": "F", "UUC": "F",
    "GGU": "G", "GGC": "G", "GGA": "G", "GGG": "G",
    "CAU": "H", "CAC": "H",
    "AUA": "I", "AUU": "I", "AUC": "I",
    "AAA": "K", "AAG": "K",
    "UUA": "L", "UUG": "L", "CUU": "L", "CUC": "L", "CUA": "L", "CUG": "L",
    "AUG": "M",
    "AAU": "N", "AAC": "N",
    "CCU": "P", "CCC": "P", "CCA": "P", "CCG": "P",
    "CAA": "Q", "CAG": "Q",
    "CGU": "R", "CGC": "R", "CGA": "R", "CGG": "R", "AGA": "R", "AGG": "R",
    "UCU": "S", "UCC": "S", "UCA": "S", "UCG": "S", "AGU": "S", "AGC": "S",
    "ACU": "T", "ACC": "T", "ACA": "T", "ACG": "T",
    "GUU": "V", "GUC": "V", "GUA": "V", "GUG": "V",
    "UGG": "W",
    "UAU": "Y", "UAC": "Y",
    "UAA": "_", "UAG": "_", "UGA": "_"
}


def read_raw_file(file):
    """
    Reads a file containing the sequence(s)
    
    Parameter
    ---------
    file: string, name of the file, in the directory with text or fasta extention (.txt or .fasta)
    
    Returns
    ---------
    A list containing the content of the text file as string inside the list
    """
    # Open the file 
    text = open(file, "r")
    # Read it in a list
    text_read = text.readlines()
    text.close()
    return text_read


def check_nucleotide(seq_read):
    """
    Takes the list file containing sequence(s) in string format
    
    Parameter
    ---------
    seq_read: list, provided by the read_rwa_file function
    
    Returns
    ---------
    A list containing clean sequence(s) in form of string with no white space and junck 
    elements in reads
    """
    # Strip the potential white spaces around each read
    # Fill the potential white space inside the sequence
    # Turn each element to upper case
    # Skip the reads staring with '>' for potential fasta format files
    first = [x.strip().replace(" ", "").upper() for x in seq_read if x.startswith(">") == False]
    
    # Check if there is any irrelevant element in each single read
    # Elements should only be the ones in nuc list
    second = [[x.replace(y, "") for x in y if x in bases] for y in first]
    
    # Join the processed read in one sinle piece 
    third = ["".join(x) for x in second]
    return third[0]


def transcribe(DNAseq):
    """
    Transcribes the DNA sequence to RNA sequence 
    
    Parameter
    ---------
    DNAseq: String, sequence provided by check_nucleotide function

    Return
    ---------
    The transcribed RNA string
    """
    return DNAseq.replace("T", "U")


def de_transcribe(RNAseq):
    """
    De transcribes the RNA sequence to DNA sequence 
    
    Parameter
    ---------
    RNAseq: String, sequence provided by transcribe function

    Return
    ---------
    The de-transcribed DNA string
    """
    return RNAseq.replace("U", "T")


def gene_detector(seq):
    """
    Detects the gene in the sequence including starting and terminating codons
    
    Parameters
    ----------
    seq: String, sequence provided by check_nucleotide function
    
    Returns
    ----------
    A tuple containing the index of starting codon (int), the index of terminating codon (int) and
    the gene (str)
    """
    rna_seq = transcribe(seq)
    # Starting codon
    gene_start = "AUG"
    # Terminating codons
    gene_end = ["UAA", "UAG", "UGA"]
    
    # Finding which terminating codon is found first
    ending = sorted([(x, rna_seq.index(x)) for x in gene_end if x in rna_seq])[0][0]
    # Isolating gene from starting codon to the terminating codon from the whole_seq
    start_codon_index = rna_seq.index(gene_start.upper())
    term_codon_index = rna_seq.index(ending) + 3
    rna = rna_seq[start_codon_index: term_codon_index]
    
    return start_codon_index, term_codon_index, rna


def label_sites(seq, res_sites):
    """
    Analyzes the restriction site(s) against the RNA sequence and adds a label to the 
    restriction site(s) depending on which part of RNA sequences it binds to.
    
    Parameters
    ----------
    seq: String, sequence provided by check_nucleotide function
    res_sites: List, containing all the restriction sites provided by the user
    
    Returns
    ----------
    A tuple whose first element is a list with restrction sites with labels and second
    element is a dictionary of restriction sites that were not found in the sequence.
    """
    position = []
    # If restriction site is not in the sequence, it will be added to this dictionary
    report = {}
    # Translate DNA to RNA
    rna_seq = transcribe(seq)
    # Translate DNA restriction site(s) to RNA
    reses = list(map(transcribe, res_sites))
    
    # Making a list of RNA restriction site - length of the site... 
    # ... - starting point in the main sequence - ending point in the main sequence
    for res in reses:
        try:
            position.append([res, len(res), rna_seq.index(res), rna_seq.index(res) + len(res) - 1])
        # If the restriction site is not found, it will be added to the report dictionary
        except ValueError:
            report[res] = "This restriction site was not found."
            
    # Locating the position of the restriction site     
    for pos in position:
        # OUT-5: upstream of the starting codon (upstream of 5')
        if (pos[2] and pos[3]) < start:
            pos.append("Out-5")
        # OUT-3: downstream of the terminating codon (downstream of 3')
        elif (pos[2] and pos[3]) > end - 1:
            pos.append("Out-3")
        # Over-5: overlapping with the starting codon
        elif (pos[2] < start) and (start < pos[3] < end - 1):
            pos.append("Over-5")
        # Over-3: overlapping with the terminating codon
        elif (pos[2] < end - 1) and (pos[3] > end - 1):
            pos.append("Over-3")
        # Exon: restriction site is in the middle of the gene
        else:
            pos.append("Exon")
            
    return (position, report)


def exon_shuffler(seq, labeled_site):
    """
    Finds where the restriction site lies in the exon segment of the gene. Then change the
    codon with one its alternatives to change the sequence without changing the protein.
    
    Parameters
    ---------
    seq: String, sequence provided by check_nucleotide function
    labeled_site: String, restriction site sequence that lies across the exon segment of the gene.
    
    Returns
    ---------
    Modified exon part of the gene with alternative codons
    """
    
    sites = labeled_site
    start_codon_index, term_codon_index, gene = gene_detector(seq)
    # Find the index where restriction site starts
    rs_e = gene.find(sites[0])
    rs_l = len(sites[0]) - 1
    
    # Turning RNA sequence into codon triplets
    rna_triplet = [gene[i: i + 3] for i in range(0, len(gene), 3)]
    # Creating a list of the index numbers where the restriction site lies
    rest_site = [x for x in range(rs_e, rs_e + rs_l + 1)]

    pairs = []

    # Find with which codon triplets the restriction site aligns
    for nuc in rest_site:
        y = nuc / 3
        if y.is_integer() == True:
            pairs.append(int(y - 1))

        else:
            pairs.append(int(y))

    pairs = list(set(pairs))        
    
    for pair in pairs:
        triplet = rna_triplet[pair]
        value = RNA_Codons[triplet]
        # Detect the alternative codons for the codon triplet in the RNA sequence
        other_codons = [k for k, v in RNA_Codons.items() if v == value and k != triplet]
        # If there are more than one alternative, choose a triplet with random.choice
        final_codon = choice(other_codons)
        # Add the new alternative to the RNA codon triplet list
        rna_triplet.insert(pair, final_codon)
        # Remove the old codon triplet from the list
        rna_triplet.pop(pair + 1)
        
    # Join the triplets to reconstruct the RNA sequence
    final = "".join(rna_triplet)
    return final    
    
    
def sequence_modification(seq, res_sites):
    """
    Modifies the sequence according to the existing restriction site.
    
    Parameters
    ----------
    seq: String, DNA sequence provided by check_nucleotide function
    res_sites: List, containing all the restriction sites provided by the user
    
    Returns:
    ----------
    String, the modified sequence
    """   
    rna_seq = transcribe(seq)
    sites = label_sites(seq, res_sites)
    start_codon_index, term_codon_index, gene = gene_detector(seq)
    
    for pos in sites:
        # If the tag is "Out-5", just remove any sequence upstream of that site
        if pos[-1] == "Out-5":
            rna_seq = rna_seq[pos[-3]:]
        # If the tag is "Out-3", just remove any sequence downstream that site
        elif pos[-1] == "Out-3":
            rna_seq = rna_seq[: pos[-2] + 1]
        # If the tag is "Over-5", change the two nucleotides upstream of the starting codon
        elif pos[-1] == "Over-5":
            b1 = rna_seq[start_codon_index - 1]
            b1_rep_list = [x for x in RNA_base if x != b1]
            b1_replcaement = choice(b1_rep_list)
            b2 = rna_seq[start_codon_index - 2]
            b2_rep_list = [x for x in RNA_base if x != b2]
            b2_replacement = choice(b2_rep_list)
            rna_seq = rna_seq[:start_codon_index - 2] + b2_replacement + b1_replcaement + rna_seq[start_codon_index:]
        # If the tag is "Over-3", change the two nucleotides downstream of the terminating codon
        elif pos[-1] == "Over-3":
            b1 = rna_seq[term_codon_index]
            b1_rep_list = [x for x in RNA_base if x != b1]
            b1_replcaement = choice(b1_rep_list)
            b2 = rna_seq[term_codon_index + 1]
            b2_rep_list = [x for x in RNA_base if x != b2]
            b2_replacement = choice(b2_rep_list)
            rna_seq = rna_seq[:term_codon_index] + b1_replcaement + b2_replacement + rna_seq[term_codon_index + 2:]

        elif pos[-1] == "Exon":
            mod_gene = exon_shuffler(seq, pos)
            rna_seq = rna_seq[:start_codon_index] + mod_gene + rna_seq[term_codon_index + 3:]
            

        else:
            pass
        
        modified = de_transcribe(rna_seq)
        
    return modified