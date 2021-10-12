import numpy as np

class Preprocessing():
    def DNA_labeler(self, lists):
        translate = {'A' : 1, 'T' : 2, 'C' : 3, 'G' : 4, 'N': 0, 'K':0, 'M':0}
        new_array = [np.array([translate[nucleotide] for nucleotide in np.array(list(i))]).astype('float32') for i in lists]
        return np.array(new_array).astype('float32')


    def Arrayer(self, lists):
        new_array = [np.array(list(i)).astype('float32') for i in lists]
        return np.array(new_array)

    def TestTrain(self, lists, percent):
        train = lists[:int(len(lists) * percent/100)]
        test = lists[int(len(lists) * percent/100):]
        return np.array(train), np.array(test)