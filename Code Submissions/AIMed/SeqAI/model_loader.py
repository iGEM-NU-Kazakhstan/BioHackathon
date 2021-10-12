import tensorflow as tf
import pandas as pd
from ModelsAutoencoders.DataPreprocessing import Preprocessing


model = tf.keras.models.load_model('saved_models/ORFdetector')
data = pd.read_csv('data/seq1.csv')
dna = data['sequence'].to_list()
label = data['label'].to_list()

seq = Preprocessing().DNA_labeler(dna[1])
label1 = label[1]

seq = seq[tf.newaxis, ..., tf.newaxis]

coder = model.encoder(seq).numpy()
decoder = model.decoder(coder).numpy()

decoder=decoder.reshape((500))


def translator(lists, treshold):
    new_list=['1' if i>treshold else '0' for i in lists]
    return new_list


a=''.join(translator(decoder, 0.5))

print(a)
print(label1)


def comparer(list1, list2):
    z=0
    for i, k in zip(list1, list2):
        if i==k:
            z+=1
    percent = z/len(list1)
    return percent


print(comparer(a, label1))


def measure(listA, listB):
    TP = 0
    TF = 0
    FP = 0
    FN = 0

    for i in range(len(listA)):
        if listB[i] == listA[i] == '1':
           TP += 1
        if listB[i] == listA[i] == '0':
           TF += 1
        if listB[i] == '0' and listA[i] == '1':
           FP += 1
        if listB[i] == '1' and listA[i] == '0':
           FN += 1

    # Recall or true positive rate
    TPR = TP / (TP + FN)

    # Precision or positive predictive value
    PPV = TP / (TP + FP)

    return TP, FP, TF, FN, TPR, PPV


print(measure(a, label1))