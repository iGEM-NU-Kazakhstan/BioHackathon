from Bio import Entrez
import urllib
import re
import random

d_restriction_sites = {
    'EcoRI' : 'gaattc',
    'XbaI' : 'tctaga',
    'SpeI' : 'actagt',
    'PstI' : 'ctgcag',
    'NotI' : 'gcggccgc',
    'SapI' : 'gctcttc',
    'BasI' : 'ggtctc'
}

d_codon_substituants = {
    'ata':['att', 'atc'],
    'atg':[],
    'aca':['act', 'acc', 'acg'],
    'act':['aca', 'acc', 'acg'],
    'acc':['aca', 'act', 'acg'],
    'acg':['acc', 'aca', 'act'],
    'aac':['aat'],
    'aat':['aac'],
    'aaa':['aag'],
    'aag':['aaa'],
    'agc':['agt'],
    'agt':['agc'],
    'aga':['agg'],
    'agg':['aga'],
    'cta':['ctc', 'ctg', 'ctt'],
    'ctc':['cta', 'ctg', 'ctt'],
    'ctg':['cta', 'ctc', 'ctt'],
    'ctt':['cta', 'ctc', 'ctg'],
    'cca':['ccc', 'ccg', 'cct'],
    'ccc':['cca', 'ccg', 'cct'],
    'ccg':['cca', 'ccc', 'cct'],
    'cct':['cca', 'ccc', 'ccg'],
    'cac':['cat'],
    'cat':['cac'],
    'caa':['cag'],
    'cag':['caa'],
    'cga':['cgc', 'cgg', 'cgt'],
    'cgc':['cga', 'cgg', 'cgt'],
    'cgg':['cga', 'cgc', 'cgt'],
    'cgt':['cga', 'cgc', 'cgg'],
    'gta':['gtc', 'gtg', 'gtt'],
    'gtc':['gta', 'gtg', 'gtt'],
    'gtg':['gta', 'gtc', 'gtt'],
    'gtt':['gta', 'gtc', 'gtg'],
    'gca':['gcc', 'gcg', 'gct'],
    'gcc':['gca', 'gcg', 'gct'],
    'gcg':['gca', 'gcc', 'gct'],
    'gct':['gca', 'gcc', 'gcg'],
    'gac':['gat'],
    'gat':['gac'],
    'gaa':['gag'],
    'gag':['gaa'],
    'gga':['ggc', 'ggg', 'ggt'],
    'ggc':['gga', 'ggg', 'ggt'],
    'ggg':['gga', 'ggc', 'ggt'],
    'ggt':['gga', 'ggc', 'ggg'],
    'tca':['tcc', 'tcg', 'tct'],
    'tcc':['tca', 'tcg', 'tct'],
    'tcg':['tca', 'tcc', 'tct'],
    'tct':['tca', 'tcc', 'tcg'],
    'ttc':['ttt'],
    'ttt':['ttc'],
    'tta':['ttg'],
    'ttg':['tta'],
    'tac':['tat'],
    'tat':['tac'],
    'taa':['tag', 'tga'],
    'tag':['taa', 'tga'],
    'tga':['taa', 'tag'],
    'tgc':['tgt'],
    'tgt':['tgc'],
    'tgg':[]
}

def line_seperator(func):
    def decorate(*args, **kwargs):
        result = func(*args, **kwargs)
        print('===============================================================')
        return result
    return decorate

@line_seperator
def read_before_warning():
    print("\n****If you did not read the READ_BEFORE.txt file, Do it now.****\nIt has important information about using this program.\n")
    input('Press Enter to continue...\n')

@line_seperator
def internet_warning():
    print("\n\n****Make sure that you're connected to the internet****\n\n")

@line_seperator
def get_ID():
    acc_id = input('Enter your DNA sequence GenBank Access Number(Example: NG_059281):\n')
    return acc_id

@line_seperator
def DNA_or_not(d_info):
    if d_info['GBSeq_moltype'] == 'DNA':
        return True
    else:
        print(f"Your sequence must be a DNA, It is currently a {d_info['GBSeq_moltype']}!\n")
        return False

def send_request(ID):
    pass
    Entrez.email = "alivafa79@gmail.com"
    try:
        handle = Entrez.efetch(db="nuccore", id=ID, rettype="gb", retmode="xml")
    except urllib.error.HTTPError:
        return False
    results = Entrez.read(handle)
    return results[0]

@line_seperator
def send_request_check(d_info):
    if d_info == False:
        print("\n\n****Incorrect GenBank Access Number****\n\n")
        return False
    else:
        return True

@line_seperator
def correct_sequence(d_info):
    answer = None
    while answer not in ['y', 'n']:
        print(f'"{d_info["GBSeq_definition"]}"')
        answer = input('Is this what you are looking for?(y/n): ').lower()
        if answer == 'y':
            return True
        elif answer == 'n':
            return False

def contain_sequence(d_info):
    try:
        seq = d_info['GBSeq_sequence']
        return str(seq)
    except KeyError:
        return False

@line_seperator
def no_sequence_warning(ID):
    print(f"\n\n****{ID} GenBank page does not contain any DNA sequence.****\n                      Try another Access Number.\n\n")

def get_genes(d_info):
    gene_count = 0
    d_genes = dict()
    for feature in d_info['GBSeq_feature-table']:
        if feature['GBFeature_key'] == 'gene':
            gene_name = feature['GBFeature_quals'][0]['GBQualifier_value']
            gene_location = feature['GBFeature_location']
            d_genes.update({gene_name:[str(gene_location)]})
            gene_count += 1
    return gene_count, d_genes

@line_seperator
def choose_genes(gene_count, gene_dictionary):
    print(f'There is/are {gene_count} gene(s) in your dataset.\n')
    print('Write down the index of each gene to add it to your selected genes list.')
    print('For selecting multiple genes, add the index next to current indexes with 1 space distance.')
    print('Example: \n1 2 3')
    tf = False
    while not tf:
        print('\nPlease choose which of this genes you want to modify:')
        print('Index    Gene\n--------------')
        for i in range(gene_count):
            gene_name = list(gene_dictionary.keys())[i]
            i += 1
            print(f'  {i}   ->   {gene_name}')
        answer = input('\nSelect which index/indexes you want:\n')
        l_answer = answer.split()
        tf = True
        for i in range(len(l_answer)):
            try:
                l_answer[i] = int(l_answer[i])
            except ValueError: 
                tf = False

        if tf == False:
            continue

        l_answer = list(set(l_answer))
        if len(l_answer) > gene_count:
            tf = False

        if tf == False:
            continue

        for i in l_answer:
            if i < 1 or i > gene_count:
                tf = False
    
    selected_genes = [i-1 for i in sorted(l_answer)]
    return selected_genes

def get_CDS(d_info, genes_dictionary, choosed_genes):
    cds = ''
    for gene_i in choosed_genes:
        current_gene = list(genes_dictionary.keys())[gene_i]
        for feature in d_info['GBSeq_feature-table']:
            if feature['GBFeature_key'] == 'CDS' and feature['GBFeature_quals'][0]['GBQualifier_value'] == current_gene:
                cds = str(feature['GBFeature_location'])
                genes_dictionary[current_gene].append(cds)
                break
    l_delete = []
    for key, value in genes_dictionary.items():
        if len(value) < 2:
            l_delete.append(key)
    for i in l_delete:
        del genes_dictionary[i]
    return genes_dictionary

@line_seperator
def choose_restrictions(d_restriction_sites):
    tf = False
    while not tf:
        print('\n==============================================')
        print('\nBelow is the list of popular restriction sites.')
        print('Index    Restriction site\n--------------------')
        for i in range(len(d_restriction_sites.keys())):
            current_restriction = list(d_restriction_sites.keys())[i]
            restriction_name = current_restriction + '(' + d_restriction_sites[current_restriction] + ')'
            i += 1
            print(f'  {i}   ->   {restriction_name}')
        print("\nThere are 2 approaches:\n1 -> Use one or more of above restriction sites.\n2 -> Enter your own restriction site sequence(s).\n")
        approach = input("Which one do you prefer? Enter 1 to use our sequences or 2 to write down your own sequences:\n")
        if approach not in ['1', '2']:
            continue
        if approach == '1':
            print('\n==============================================')
            print('\nWrite down the index of each restriction site to add it to your selected restriction sites list.')
            print('For selecting multiple restriction sites, add the index next to current indexes with 1 space distance.')
            print('Example: \n1 2 3 4')
            print('\nPlease choose which of this restriction sites you want to use:')
            print('Index    Restriction site\n--------------------')
            for i in range(len(d_restriction_sites.keys())):
                current_restriction = list(d_restriction_sites.keys())[i]
                restriction_name = current_restriction + '(' + d_restriction_sites[current_restriction] + ')'
                i += 1
                print(f'  {i}   ->   {restriction_name}')
            answer = input('\nSelect which index/indexes you want:\n')
            l_answer = answer.split()
            tf = True
            for i in range(len(l_answer)):
                try:
                    l_answer[i] = int(l_answer[i])
                except ValueError: 
                    tf = False

            if tf == False:
                continue
            
            l_answer = list(set(l_answer))
            if len(l_answer) > len(d_restriction_sites.keys()):
                tf = False
            
            if tf == False:
                continue
                
            for i in l_answer:
                if i < 1 or i > len(d_restriction_sites.keys()):
                    tf = False
        elif approach == '2':
            print('\n==============================================')
            print('\nIf you have more than one sequence, Seperate each of them with *just a comma*.')
            print('Example:\nacgcgt,gtatac\n')
            res_seq = input('Write down your own restriction site(s):\n')
            tf = True
            res_seq = res_seq.split(',')
            for s in res_seq:
                for nuc in s:
                    if nuc.lower() not in ['a', 'c', 'g', 't']:
                        tf = False
                        break
                break

            if tf == False:
                continue
            
            for i_res in range(len(res_seq)):
                res_seq[i_res] = res_seq[i_res].lower()
    if approach == '1':
        ans = [list(d_restriction_sites.values())[i-1] for i in l_answer]
        return ans
    elif approach == '2':
        ans = res_seq
        return ans

def restriction_finder(restriction, tsequence):
    d_complementary = {
        'a':'t',
        'c':'g',
        'g':'c',
        't':'a'
    }
    c = len(restriction)
    r_restriction = ''.join([d_complementary[s] for s in restriction])[::-1]
    pattern = '(?=' + restriction + ')'
    res_indexes = [m.start() for m in re.finditer(pattern, tsequence)]
    if r_restriction != restriction:
        pattern = '(?=' + r_restriction + ')'
        r_res_indexes = [m.start() for m in re.finditer(pattern, tsequence)]
        indexes = (list(set(res_indexes + r_res_indexes)), c)
    else:
        indexes = (res_indexes, c)
    
    return indexes

def read_ranges(genes_dictionary):
    ngene_dictionary = {}
    for gene in genes_dictionary.keys():
        gene_range, CDS_range = genes_dictionary[gene][0], genes_dictionary[gene][1]
        if gene_range.startswith('complement'):
            ngene_range = gene_range[11:-1]
            if '<' in ngene_range:
                ngene_range = ngene_range.split('..')
                ngene_range = [0, int(ngene_range[1])-1]
            elif '>' in ngene_range:
                ngene_range = ngene_range.split('..')
                ngene_range = [int(ngene_range[0])-1, int(ngene_range[1][1:])-1]
            elif '>' not in ngene_range and '<' not in ngene_range:
                ngene_range = ngene_range.split('..')
                ngene_range = [int(ngene_range[0])-1, int(ngene_range[1])-1]
            if '>' in ngene_range and '<' in ngene_range:
                ngene_range = [0, int(ngene_range[1][1:])-1]
        elif gene_range[0].isdigit():
            ngene_range = gene_range.split('..')
            ngene_range = [int(ngene_range[0])-1, int(ngene_range[1])-1]


        if CDS_range[0].isdigit():
            nCDS_range = CDS_range.split('..')
            nCDS_range = [[int(nCDS_range[0])-1, int(nCDS_range[1])-1]]
        elif CDS_range.startswith('complement'):
            nCDS_range = CDS_range[11:-1]
            if '<' in nCDS_range:
                nCDS_range = nCDS_range.split('..')
                nCDS_range = [[0, int(nCDS_range[1])-1]]
            elif '>' in nCDS_range:
                nCDS_range = nCDS_range.split('..')
                nCDS_range = [[int(nCDS_range[0])-1, int(nCDS_range[1][1:])-1]]
            elif '>' not in nCDS_range and '<' not in nCDS_range:
                nCDS_range = nCDS_range.split('..')
                nCDS_range = [[int(nCDS_range[0])-1, int(nCDS_range[1])-1]]
            if '>' in nCDS_range and '<' in nCDS_range:
                nCDS_range = [[0, int(nCDS_range[1][1:])-1]]
        elif CDS_range.startswith('join'):
            nCDS_range = []
            nnCDS_range = CDS_range[5:-1]
            nnCDS_range = nnCDS_range.split(',')
            for r in nnCDS_range:
                if '<' in r:
                    r = r.split('..')
                    r = [0, int(r[1])-1]
                elif '>' in r:
                    r = r.split('..')
                    r = [int(r[0])-1, int(r[1][1:])-1]
                elif '>' not in r and '<' not in r:
                    r = r.split('..')
                    r = [int(r[0])-1, int(r[1])-1]
                if '>' in r and '<' in r:
                    r = [0, int(r[1][1:])-1]
                nCDS_range.append(r)
        ngene_dictionary.update({gene:[ngene_range, nCDS_range]})
    return ngene_dictionary
        
def in_CDS(genes_dictionary, l_restriction_places):
    l_all_cds_ranges = []
    for key, value in genes_dictionary.items():
        for v in value[1]:
            l_all_cds_ranges.append(v)
    
    l_in_cds = []
    for i in l_restriction_places:
        place = i[0]
        lenght = i[1]
        for j in place:
            for m in range(j, j+lenght):
                for pair in l_all_cds_ranges:
                    if m <= pair[1]  and m >= pair[0]:
                        l_in_cds.append((j, m - j, pair[0]))
                        break
                break
    return l_in_cds
                
def in_CDS_hide(d_codon_substituants, tsequence, resplace, lenght, m, d):
    l_sequnces = []
    for i in range(resplace, resplace+lenght):
        if (i - d) % 3 == 2:
            l_sequnces.append((tsequence[i-2:i+1], i-2))
    ncodon = None
    for codon in l_sequnces:

        if len(d_codon_substituants[codon[0]]) == 0:
            continue
        else:
            ncodon = (random.choice(d_codon_substituants[codon[0]]), codon[1])
            break
    if ncodon == None:
        return 'not possible'
    else:
        tsequence = tsequence[:ncodon[1]] + ncodon[0] + tsequence[ncodon[1]+3:]
        return tsequence

def stop_or_not(l_restriction_places):
    tf = True
    for t in l_restriction_places:
        if len(t[0]) != 0:
            tf = False
            break
    return tf

def ask_output_name():
    print('===============================================================')
    print('Enter your output file name:')
    print('For example if you enter "hidden_sequence" , your output file will be "hidden_sequence.txt"')
    answer = input('Output file name:\n')
    return answer
    

read_before_warning()

if __name__ == '__main__':
    internet_warning()
    while True:
        access_number = get_ID()
        d_informations = send_request(access_number)
        if not send_request_check(d_informations):
            continue
        if not DNA_or_not(d_informations):
            continue
        if not correct_sequence(d_informations):
            continue
        seq = contain_sequence(d_informations)
        if not seq:
            no_sequence_warning(access_number)
            continue
        gene_count, genes_dictionary = get_genes(d_informations)
        if gene_count == 0:
            print("Your DNA sequence has no Gene!\n")
            continue
        if gene_count != 0:
            choosed_genes = choose_genes(gene_count, genes_dictionary)
            genes_dictionary = get_CDS(d_informations, genes_dictionary, choosed_genes)
        restrictions = choose_restrictions(d_restriction_sites)
        break
    genes_dictionary = read_ranges(genes_dictionary)
    while True:
        l_restriction_places = []
        for res in restrictions:
            restriction_places = restriction_finder(res, seq)
            l_restriction_places.append(restriction_places)
        if stop_or_not(l_restriction_places):
            break
        l_in_CDS = in_CDS(genes_dictionary,l_restriction_places)
        l_all_in_CDS = [i[0] for i in l_in_CDS]
        for res_places in l_restriction_places:
            for res_place in res_places[0]:
                if res_place not in l_all_in_CDS:
                    l_nucleotide = ['a', 'c', 'g', 't']
                    n = res_place + random.randint(0, res_places[1] - 1)
                    l_nucleotide.remove(seq[n])
                    seq = seq[:n] + random.choice(l_nucleotide) + seq[n+1:]
                else:
                    for incdses in l_in_CDS:
                        if incdses[0] == res_place:
                            m = incdses[1]
                            d = incdses[2]
                            break
                    seq = in_CDS_hide(d_codon_substituants, seq, incdses[0], res_places[1], m, d)
                    if seq == 'not possible':
                        print('There is a tie. Hiding process failed!')
                        exit()
    outname = ask_output_name() + '.txt'
    with open(outname, 'w') as f:
        for g,r in genes_dictionary.items():
            res_sites = 'Chosen restriction sites: ' + str(restrictions) + '\n'
            final_sequence = 'DNA sequence:\n' + seq[r[0][0] : r[0][1] + 1]
            f.write(head)
            f.write(res_sites)
            f.write(final_sequence)
            f.write('\n===============================================================================\n')
