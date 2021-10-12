import re
import sys
import argparse
import random
import os.path
from operator import itemgetter
from Bio.Seq import Seq
from Bio.Data import CodonTable

available_codon_tables = {'The Standard Code': 1,
 'The Vertebrate Mitochondrial Code': 2,
 'The Yeast Mitochondrial Code': 3,
 'The Mold, Protozoan, and Coelenterate Mitochondrial Code and the Mycoplasma/Spiroplasma Code': 4,
 'The Invertebrate Mitochondrial Code': 5,
 'The Ciliate, Dasycladacean and Hexamita Nuclear Code': 6,
 'The Echinoderm and Flatworm Mitochondrial Code': 9,
 'The Euplotid Nuclear Code': 10,
 'The Bacterial, Archaeal and Plant Plastid Code': 11,
 'The Alternative Yeast Nuclear Code': 12,
 'The Ascidian Mitochondrial Code': 13,
 'The Alternative Flatworm Mitochondrial Code': 14,
 'Chlorophycean Mitochondrial Code': 16,
 'Trematode Mitochondrial Code': 21,
 'Scenedesmus obliquus Mitochondrial Code': 22,
 'Thraustochytrium Mitochondrial Code': 23,
 'Rhabdopleuridae Mitochondrial Code': 24,
 'Candidate Division SR1 and Gracilibacteria Code': 25,
 'Pachysolen tannophilus Nuclear Code': 26,
 'Karyorelict Nuclear Code': 27,
 'Condylostoma Nuclear Code': 28,
 'Mesodinium Nuclear Code': 29,
 'Peritrich Nuclear Code': 30,
 'Blastocrithidia Nuclear Code': 31,
 'Cephalodiscidae Mitochondrial UAA-Tyr Code': 33}


def choose_codon_table(id_):
    table = CodonTable.unambiguous_dna_by_id[id_]
    return(table)


def read_fasta(path):
    seq = ''
    with open(path) as file:
        for line in file:
            if line.startswith('>'):
                continue
            else:
                seq += line.strip().upper()
    return seq


def read_restriction_enzymes_database(path):
    db = dict()
    with open(path) as file:
        for line in file:
            line = line.strip().split('\t')
            enzyme = line[0]
            site = re.sub('\(\d+\S\d+\)|\(-\d+\S-\d+\)|\(\d+\S-\d+\)|\(-\d+\S\d+\)', 
                          '', 
                          line[2])
            site = site.replace('^', '')
            db[enzyme] = site
    return db


def complement(seq):
    return(seq.replace('A', 't').replace('T', 'a').replace('C', 'g').replace('G', 'c').upper()[::-1])


def iupac(nucleotide):
    table = {
        'A': {'A'},
        'C': {'C'},
        'G': {'G'},
        'T': {'T'},
        'R': {'A', 'G'},
        'Y': {'C', 'T'},
        'S': {'G', 'C'},
        'W': {'A', 'T'},
        'K': {'G', 'T'},
        'M': {'A', 'C'},
        'B': {'C', 'G', 'T'},
        'D': {'A', 'G', 'T'},
        'H': {'A', 'C', 'T'},
        'V': {'A', 'C', 'G'},
        'N': {'A', 'C', 'G', 'T'}
    }
    return table[nucleotide]


def compare(seq1, seq2):
    for n1, n2 in zip(seq1, seq2):
        if len(iupac(n1) & iupac(n2)) > 0:
            continue
        else:
            return False
    return True
        

def find_pattern(seq, pattern):
    results = []
    length = len(pattern)
    for i in range(len(seq) - length + 1):
        s = seq[i:i + length]
        if compare(s, pattern):
            results.append((i, '+', s))
        elif compare(complement(s), pattern):
            results.append((i, '-', complement(s)))
        else:
            continue
    return results


def find_orfs_with_trans(seq, trans_table, min_protein_length):
    answer = []
    seq_len = len(seq)
    for strand, nuc in [(+1, seq), (-1, seq.reverse_complement())]:
        for frame in range(3):
            trans = nuc[frame:].translate(trans_table)
            trans_len = len(trans)
            aa_start = 0
            aa_end = 0
            while aa_start < trans_len:
                aa_end = trans.find("*", aa_start)
                if aa_end == -1:
                    aa_end = trans_len
                if aa_end - aa_start >= min_protein_length:
                    if strand == 1:
                        start = frame + aa_start * 3
                        end = min(seq_len, frame + aa_end * 3 + 3)
                    else:
                        start = seq_len - frame - aa_end * 3 - 3
                        end = seq_len - frame - aa_start * 3
                    answer.append((start, end, strand, trans[aa_start:aa_end]))
                aa_start = aa_end + 1
    answer.sort(key=itemgetter(0))
    return answer


def write_table(path, data):
    with open(path, 'w') as file:
        file.write('pos\tstrand\tsite\tregion\tcodone_pos\n')
        for line in data:
            file.write('\t'.join(map(str, line)) + '\n')
    pass


def read_table(path):
    container = []
    with open(path) as file:
        file.readline()
        for line in file:
            line = [i if not i.isnumeric() else int(i) for i in line.strip().split()]
            container.append(line)
    return container


def check_intersection(start, end, point):
    return start <= point and point <= end 


def annotate_restrict_sites(sites_table, orf):
    annotation = []
    for i in sites_table:
        for j in orf:
            start = j[0]
            end = j[1]
            region = 'in_noncoding_region'
            first_codone = i[0]
            if check_intersection(start, end, i[0]):
                for frame in range(3):
                    if (i[0] + frame - start) % 3 == 0:
                        first_codone = i[0] + frame
                region = 'in_coding_region'
                break
        annotation.append((i[0], i[1], i[2], region, first_codone))
    return annotation


def replace_codone(codone, table):
    table_decode = table.forward_table
    if not codone in table_decode:
        return [codone]
    aa = table_decode[codone]
    table = table.forward_table
    alternative = []
    for codone_, aa_ in table.items():
        if aa_ == aa and codone_ != codone:
            alternative.append(codone_)
    return alternative
     
    
def insert_silenced_mutation(site, pattern, table):
    output = ''
    for i in range(0, len(site), 3):
        codone = site[i:i+3]
        alternative = replace_codone(codone, table)
        if len(alternative) == 0:
            continue
        else:           
            for j in alternative:
                output = site[:i] + j + site[i+3:]
                if len(find_pattern(output, pattern)) > 0:
                    continue
                else:
                    return output
    if output == '':
        output = site
        print('Can`t create scilence mutation')
    return output
    

def change_nuc_in_site(seq, nuc, index):  
    return seq[:index] + nuc + seq[index+1:]


def insert_mutated_site_in_seq(seq, site, start, end):
    return seq[:start] + site + seq[end:]


def insert_random_mutation(site, pattern):
    nucleotides = {'A', 'C', 'G', 'T'}
    for index, nucleotide in enumerate(pattern):
        variance = nucleotides - iupac(nucleotide)
        if len(variance) != 0:
            random_nucleitide = random.choice(list(variance))
            mutated_site = change_nuc_in_site(site, random_nucleitide, index)
            break
        else:
            continue
    return mutated_site


def breake_choosen_sites(seq, pattern, annotation, codone_table):
    mutated_seq = str(seq)[:]
    for record in annotation:
        if record[3] == 'in_coding_region':
            if record[4] > record[0]:
                start = record[4] - 3
            else:
                start = record[4]
            for frame in range(3):
                if (len(record[2]) + frame) % 3 == 0:
                    tail = frame
                    break
            end = start + 3 + len(record[2]) + tail
            site = seq[start:end]
            silenced_mutated_site = insert_silenced_mutation(site, pattern, codone_table)
            mutated_seq = insert_mutated_site_in_seq(mutated_seq,
                                                 silenced_mutated_site,
                                                 start, end)
        else:
            start = record[4]
            end = start + len(record[2])
            site = seq[start:end]
            mutated_site = insert_random_mutation(site, pattern)
            mutated_seq = insert_mutated_site_in_seq(mutated_seq,
                                                     mutated_site,
                                                     start, end)
    return mutated_seq


def write_fasta(write_path, data):
    with open(write_path, 'w') as file:
        file.write('>\n')
        if len(data) > 70:
            for i in range(0, len(data), 70):
                file.write(f'{data[i:i+70]}\n')
        else:
            file.write(f'{data}\n')
    pass


def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subparser_name', help='Available commands:')
    
    parser_codon_tables = subparsers.add_parser('codon_tables', help='Return avalibale codon tables in STDOUT')
    
    parser_enzymes = subparsers.add_parser('enzymes', help='Return avalibale restriction enzymes in STDOUT')
    
    parser_find_sites = subparsers.add_parser('find_known_sites', help='Find sites in fasta file for given restriction enzyme')
    parser_find_sites.add_argument('fasta_path', action='store', help='path to FASTA file')
    parser_find_sites.add_argument('enzyme', action='store', help='name of Enzyme')
    parser_find_sites.add_argument('write_path', action='store', help='path to write results')
    parser_find_sites.add_argument('-c', '--codone', action='store', type=int, dest='codone',
                        required=False, default=1, help='The ID (1, 2, 3 etc.) of codone table choosen from [codon_tables] output, \
                        default=1 (The Standard Code)')
    parser_find_sites.add_argument('-m', '--min', action='store', type=int, dest='min',
                        required=False, default=75, help='Minimal length of protein for prediction ORF, default value = 75')

    
    parser_find_by_pattern = subparsers.add_parser('find_by_pattern', help='Find sites in fasta file for given restriction enzyme')
    parser_find_by_pattern.add_argument('fasta_path', action='store', help='path to FASTA file')
    parser_find_by_pattern.add_argument('pattern', action='store', help='Pattern of enzime site in IUPAC format. Example YCCGSS')
    parser_find_by_pattern.add_argument('write_path', action='store', help='path to write results')
    parser_find_by_pattern.add_argument('-c', '--codone', action='store', type=int, dest='codone',
                        required=False, default=1, help='The ID (1, 2, 3 etc.) of codone table choosen from [codon_tables] output, \
                        default=1 (The Standard Code)')
    parser_find_by_pattern.add_argument('-m', '--min', action='store', type=int, dest='min',
                        required=False, default=75, help='Minimal length of protein for prediction ORF, default value = 75')

    
    parser_remove_sites = subparsers.add_parser('remove_known_sites', help='Return modified FASTA')
    parser_remove_sites.add_argument('fasta_path', action='store', help='path to FASTA file')
    parser_remove_sites.add_argument('table_path', action='store', help='path to TSV file with targets')
    parser_remove_sites.add_argument('enzyme', action='store', help='name of Enzyme')
    parser_remove_sites.add_argument('write_path', action='store', help='path to write results')
    parser_remove_sites.add_argument('-c', '--codone', action='store', type=int, dest='codone',
                        required=False, default=1, help='The ID (1, 2, 3 etc.) of codone table choosen from [codon_tables] output, \
                        default=1 (The Standard Code)')

    parser_remove_by_pattern = subparsers.add_parser('remove_by_pattern', help='Return modified FASTA')
    parser_remove_by_pattern.add_argument('fasta_path', action='store', help='path to FASTA file')
    parser_remove_by_pattern.add_argument('table_path', action='store', help='path to TSV file with targets')
    parser_remove_by_pattern.add_argument('pattern', action='store', help='Pattern of enzime site in IUPAC format. Example YCCGSS')
    parser_remove_by_pattern.add_argument('write_path', action='store', help='path to write results')
    parser_remove_by_pattern.add_argument('-c', '--codone', action='store', type=int, dest='codone',
                        required=False, default=1, help='The ID (1, 2, 3 etc.) of codone table choosen from [codon_tables] output, \
                        default=1 (The Standard Code)')
                                        
                                        
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    return(parser.parse_args())


def main():
    args = parse_args()
    this_dir, this_filename = os.path.split(__file__)
    db_path = os.path.join(this_dir, "db", "restriction_enzymes_database.tsv")

    if args.subparser_name == 'codon_tables':
        keys = []
        for key, value in available_codon_tables.items():
            print(key, value)
    elif args.subparser_name == 'enzymes':
        db = read_restriction_enzymes_database(db_path)
        for i in db.items():
            print(' '.join(i))
    elif args.subparser_name == 'find_known_sites':
        fasta_path = args.fasta_path
        write_path = args.write_path
        enzyme = args.enzyme
        codon_id = args.codone
        min_protein_length = args.min
        
        seq = read_fasta(fasta_path)
        db = read_restriction_enzymes_database(db_path)
        pattern = db[enzyme]
        results = find_pattern(seq, pattern)
        
        codone_table = choose_codon_table(codon_id)
        orfs = find_orfs_with_trans(Seq(seq), codone_table, min_protein_length)
        annotated_results = annotate_restrict_sites(results, orfs)
        write_table(write_path, annotated_results)
        
    elif args.subparser_name == 'find_by_pattern':
        fasta_path = args.fasta_path
        write_path = args.write_path
        pattern = args.pattern.upper()
        codon_id = args.codone
        min_protein_length = args.min
        
        seq = read_fasta(fasta_path)
        db = read_restriction_enzymes_database(db_path)
        results = find_pattern(seq, pattern)
        codone_table = choose_codon_table(codon_id)
        orfs = find_orfs_with_trans(Seq(seq), codone_table, min_protein_length)
        annotated_results = annotate_restrict_sites(results, orfs)
        write_table(write_path, annotated_results)
        
    elif args.subparser_name == 'remove_known_sites':
        fasta_path = args.fasta_path
        table_path = args.table_path
        write_path = args.write_path
        enzyme = args.enzyme
        codon_id = args.codone
        
        annotated_results = read_table(table_path)
        seq = read_fasta(fasta_path)
        db = read_restriction_enzymes_database(db_path)
        pattern = db[enzyme]
        codone_table = choose_codon_table(codon_id)
        output = breake_choosen_sites(seq, pattern, annotated_results, codone_table)
        write_fasta(write_path, output)
        
    elif args.subparser_name == 'remove_by_pattern':
        fasta_path = args.fasta_path
        table_path = args.table_path
        write_path = args.write_path
        pattern = args.pattern.upper()
        codon_id = args.codone
        
        annotated_results = read_table(table_path)
        seq = read_fasta(fasta_path)
        db = read_restriction_enzymes_database(db_path)
        codone_table = choose_codon_table(codon_id)
        output = breake_choosen_sites(seq, pattern, annotated_results, codone_table)
        write_fasta(write_path, output)
    else:
        pass
    pass
    
    
if __name__ == "__main__":
    main()