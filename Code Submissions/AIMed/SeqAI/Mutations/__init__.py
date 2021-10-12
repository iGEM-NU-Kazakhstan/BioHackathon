from SeqAI.SeqProcessing import RestrictionDeterminer, ORF
import numpy as np
from Bio.Seq import Seq
from Bio import SeqIO
import random


class Mutation():
    def find_x_orf(self, x_point, dna_list):
        start = 0
        for i in dna_list[x_point:0:-1]:
            if i != 0:
                start += 1
            else:
                break
        start = x_point - start
        end = 0
        for i in dna_list[x_point:]:
            if i != 0:
                end += 1
            else:
                break
        end = x_point + end
        x_orf = [start, end]
        return x_orf

    def check_protein_is_true(self, dna_seq_changed, dna_seq_initial):
        prot_changed = Seq(dna_seq_changed).translate()
        prot_initial = Seq(dna_seq_initial).translate()
        if prot_initial == prot_changed and dna_seq_initial != dna_seq_changed:
            return True
        else:
            return False

    def random_mutation(self, lists, coordinate1, coordinate2):
        lists = list(lists)
        list_of_lists = []
        length = len(lists[coordinate1:coordinate2])
        for i in range(length):
            nucleotides = ['A', 'C', 'G', 'T']
            for z in range(3):
                x = random.randint(0, length - i)
                lists[coordinate1 + i:coordinate1 + i + x] = [random.choice(nucleotides) for i in range(x)]
                list_of_lists.append(''.join(lists))
        return list_of_lists

    def check_mutation(self, dna_seq_initial, coordinate1, coordinate2):
        lists = self.random_mutation(dna_seq_initial, coordinate1, coordinate2)
        true_mutation = [1 if self.check_protein_is_true(i, dna_seq_initial) else 0 for i in lists]
        true_mutation_list = []
        while sum(true_mutation) < 1:
            lists = self.random_mutation(dna_seq_initial, coordinate1, coordinate2)
            true_mutation = [1 if self.check_protein_is_true(i, dna_seq_initial) else 0 for i in lists]
        for i, z in zip(lists, true_mutation):
            if z != 0:
                true_mutation_list.append(i)
                true_mutation_list = list(dict.fromkeys(true_mutation_list))
        return true_mutation_list

    def find_x_point(self, array):
        x_point = []
        for x, i in zip(array, range(len(array))):
            if x > 1:
                x_point.append(i)
        z_point = [x_point[0]]
        for x, i in zip(x_point, range(len(x_point) - 1)):
            if x_point[i + 1] - 1 == x_point[i]:
                continue
            else:
                z_point.append(x_point[i + 1])

        return z_point

    def plotter(self, dna, new):
        z = []
        for i, k in zip(dna, new):
            if i == k:
                z.append('|')
            else:
                z.append('x')
        return ''.join(z)

    def plotter_change(self, list_of_results, initial_dna):
        true_seq = []
        z = []
        for i in list_of_results:
            c = 0
            for d, k in zip(i, initial_dna):
                if d != k:
                    c += 1
            z.append(c)
        z = np.argmax(np.array(z))
        true_seq = list_of_results[z]
        return true_seq

    def alter_restr(self, dna, site):
        orf_map = np.array(ORF().get_zeros_list(dna))
        restr = RestrictionDeterminer(site, dna).CreateMap()
        restricted_map = np.array([0 if i == '0' else 1 for i in restr])
        dna = list(dna)
        resulted_dna = list(dna)
        result = []
        condenced_array = np.array(orf_map + restricted_map)

        def one_x_point(dna, x_point, restricted_map_in_def):
            orf_coord = self.find_x_orf(x_point, orf_map)
            rest_coord = self.find_x_orf(x_point, restricted_map_in_def)

            if orf_coord[0] < rest_coord[0] and orf_coord[1] > rest_coord[1]:

                dna_to_alter = ''.join(dna[orf_coord[0]:orf_coord[1]])
                dna_to_alter = self.check_mutation(dna_to_alter, (rest_coord[0] - orf_coord[0] + 1),
                                              (rest_coord[1] - orf_coord[0]))
                for i in range(len(dna_to_alter)):
                    resulted_dna[orf_coord[0]:orf_coord[1]] = list(dna_to_alter[i])
                    result.append(''.join(resulted_dna))
            elif orf_coord[0] < rest_coord[0] and orf_coord[1] < rest_coord[1]:

                dna_to_alter = ''.join(dna[orf_coord[0]:orf_coord[1] + 3])
                dna_to_alter = self.check_mutation(dna_to_alter, (rest_coord[0] - orf_coord[0] + 1),
                                              (orf_coord[1] + 3 - orf_coord[0]))
                for i in range(len(dna_to_alter)):
                    resulted_dna[orf_coord[0]:orf_coord[1] + 3] = list(dna_to_alter[i])
                    result.append(''.join(resulted_dna))
            elif orf_coord[0] > rest_coord[0] and (orf_coord[1] > rest_coord[1] or orf_coord[1] < rest_coord[1]):

                dna_to_alter = ''.join(dna[rest_coord[0]:orf_coord[0]])
                dna_to_alter = self.random_mutation(dna_to_alter, 0, (orf_coord[0] - rest_coord[0]))
                for i in range(len(dna_to_alter)):
                    resulted_dna[rest_coord[0]:orf_coord[0]] = list(dna_to_alter[i])
                    result.append(''.join(resulted_dna))
            return result

        def check(dna_seq):
            result = dna_seq
            restr1 = RestrictionDeterminer(site, dna_seq).CreateMap()
            restricted_map1 = np.array([0 if i == '0' else 1 for i in restr1])
            condenced_array1 = np.array(orf_map + restricted_map1)
            if sum(restricted_map1) != 0:
                while sum(restricted_map1) != 0:
                    if max(condenced_array1) < 2:
                        result = self.random_mutation(dna_seq, np.argmax(restricted_map1), np.argmax(restricted_map1) + 1)
                        restr1 = RestrictionDeterminer(site, result).CreateMap()

                        restricted_map1 = np.array([0 if i == '0' else 1 for i in restr1])
                        condenced_array1 = np.array(orf_map + restricted_map1)
                    else:
                        results = one_x_point(dna_seq, np.argmax(condenced_array1), restricted_map1)
                        result = self.plotter_change(results, result)
                        restr1 = RestrictionDeterminer(site, result).CreateMap()

                        restricted_map1 = np.array([0 if i == '0' else 1 for i in restr1])
                        condenced_array1 = np.array(orf_map + restricted_map1)
            else:
                result = dna_seq
            return result

        argmaximum = max(condenced_array)
        if argmaximum > 1:
            x_point = self.find_x_point(condenced_array)
            if len(x_point) == 1:
                x_point = x_point[0]
                results = one_x_point(dna, x_point, restricted_map)
            else:
                results1 = [dna]
                for i in x_point:
                    results = one_x_point(results1[-1], i, restricted_map)
                    results1 += results
                results = self.plotter_change(results1, dna)
            final_result = check(results)
        else:
            final_result = check(dna)

        return final_result

    def alter_and_plot(self, dna, site):
        result=self.alter_restr(dna, site)
        orf = ORF().get_zeros(dna)
        orft = ''.join(['1' if i != '0' else '-' for i in orf])
        rest = RestrictionDeterminer(site, dna).CreateMap()
        restt = ''.join(['1' if i != '0' else '-' for i in rest])
        print(orft)
        print(result)
        print(self.plotter(dna, result))
        print(dna)
        print(restt)

    def alter_and_plot_to_tuple(self, dna, site):
        result=self.alter_restr(dna, site)
        orf = ORF().get_zeros(dna)
        orft = ''.join(['1' if i != '0' else '-' for i in orf])
        rest = RestrictionDeterminer(site, dna).CreateMap()
        restt = ''.join(['1' if i != '0' else '-' for i in rest])
        return orft, result, self.plotter(dna, result), dna, restt

