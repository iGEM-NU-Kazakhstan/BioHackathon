from main import dp
import re
import sys
import argparse
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

### ЭТИ ФУНКЦИИ НУЖНО УДАЛИТЬ В КОНЦЕ
def seq(x):
    return("1 sequence, 2 sequence, 3 sequence")
def orf(x):
    return("agtagGTAGGcggatGTAGGgtccat")
def sites(x):
    return('final sequence')


def write_file(seq, codon_table):
    result = []
    for row in find_orfs_with_trans(seq, codon_table):
        result.append(str(row[0]) + ' ' + str(row[1]) + ' ' + str(row[2]) + ' ' + str(len(str(row[3]))) + ' ' + str(row[3]))
    with open('ORFs.txt', 'w') as file:
        file.write('All ORFs that I found:\nFormat: index, index of first nucleotide, index of last nucleotide, DNA(+/-), length, sequence\n\n')
        for i in range(len(result)):
            file.write(str(i+1) + '. ' + result[i] + '\n')


def choose_codon_table(codon_id):
    table = CodonTable.unambiguous_dna_by_id[int(codon_id)]
    return (table)


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
    return (seq.replace('A', 't').replace('T', 'a').replace('C', 'g').replace('G', 'c').upper()[::-1])


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
            results.append((i+1, '+', s))
        elif compare(complement(s), pattern):
            results.append((i+1, '-', complement(s)))
        else:
            continue
    return results


def find_orfs_with_trans(seq, trans_table, min_protein_length=75):
    seq = Seq(seq)
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
                print(j)
                for frame in range(3):
                    if (i[0] + frame - start) % 3 == 0:
                        first_codone = i[0] + frame
                region = 'in_coding_region'
                break
        annotation.append((i[0], i[1], i[2], region, first_codone))
    return annotation


def replace_codone(codone, table):
    table_decode = table.forward_table
    aa = table_decode[codone]
    table = table.forward_table
    alternative = []
    for codone_, aa_ in table.items():
        if aa_ == aa and codone_ != codone:
            alternative.append(codone_)
    return alternative


def insert_scilent_mutation(site, pattern, table):
    output = ''
    print(site)
    for i in range(0, len(site), 3):
        codone = site[i:i + 3]
        print(codone)
        alternative = replace_codone(codone, table)
        if len(alternative) == 0:
            continue
        else:
            output = codone + site[i:i + 3]
            if find_pattern(output, pattern):
                continue
    if output == '':
        output = site
        print('Can`t create scilence mutation')
    return output


def change_nuc_in_site(seq, nuc, index):
    return seq[:index] + nuc + seq[index + 1:]


def insert_murated_site_in_seq(seq, site, start, end):
    return seq[:start] + site + seq[end + 1:]


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
            end = start + (len(record[2]) + 3) + tail
            site = seq[start:end]
            scilent_mutated_site = insert_scilent_mutation(site, pattern, codone_table)
            mutated_seq = insert_murated_site_in_seq(mutated_seq,
                                                     scilent_mutated_site,
                                                     start, end)
        else:
            start = record[4]
            end = start + len(record[2])
            site = seq[start:end]
            mutated_site = insert_random_mutation(site, pattern)
            mutated_seq = insert_murated_site_in_seq(mutated_seq,
                                                     mutated_site,
                                                     start, end)
    return mutated_seq


def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subparser_name', help='Available commands:')

    parser_codon_tables = subparsers.add_parser('codon_tables', help='Return avalibale codon tables in STDOUT')

    parser_enzymes = subparsers.add_parser('enzymes', help='Return avalibale restriction enzymes in STDOUT')

    parser_find_sites = subparsers.add_parser('find_known_sites',
                                              help='Find sites in fasta file for given restriction enzyme')
    parser_find_sites.add_argument('fasta_path', action='store', help='path to FASTA file')
    parser_find_sites.add_argument('enzyme', action='store', help='name of Enzyme')
    parser_find_sites.add_argument('write_path', action='store', help='path to write results')

    parser_remove_sites = subparsers.add_parser('remove_sites', help='Return modified FASTA')
    parser_remove_sites.add_argument('fasta_path', action='store', help='path to FASTA file')
    parser_remove_sites.add_argument('table_path', action='store', help='path to TSV file with targets')
    parser_remove_sites.add_argument('enzyme', action='store', help='name of Enzyme')
    parser_remove_sites.add_argument('write_path', action='store', help='path to write results')

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    return (parser.parse_args())