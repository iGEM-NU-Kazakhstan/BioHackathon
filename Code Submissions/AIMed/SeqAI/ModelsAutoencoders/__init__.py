import pandas as pd
from .DataPreprocessing import Preprocessing
from .ModelDetector import create_model, kmer, list_of_sequenses
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import tensorflow as tf

def prepare_data(dna_seq, enzyme):
    # Data preprocessing
    # Load data from csv
    data = pd.read_csv('SeqAI/data/classic_restrict.csv')

    # Read data
    dna_data = data['sequence'].to_list()
    length = 6

    # Define the enzyme work
    label_data = data[enzyme].to_list()

    # data preprocessing
    train_dna, test_dna = Preprocessing().TestTrain(dna_data, 70)
    train_label, test_label = Preprocessing().TestTrain(label_data, 70)

    train_dna = list_of_sequenses(train_dna, length)
    test_dna = list_of_sequenses(test_dna, length)

    tokenizer = Tokenizer(oov_token="<OOV>")

    tokenizer.fit_on_texts(train_dna)
    word_index = tokenizer.word_index

    sequences = tokenizer.texts_to_sequences(train_dna)

    padded = pad_sequences(sequences, padding="post")

    test_sequences = tokenizer.texts_to_sequences(test_dna)
    test_seq_final = pad_sequences(test_sequences, padding="post")

    y_zero = np.array(train_label)

    y_test = np.array(test_label)

    vocab_size = len(word_index)
    max_length = len(padded[0])

    dna_seq_kmered = kmer(dna_seq, length)
    dna_seq_sequences = tokenizer.texts_to_sequences(dna_seq_kmered)
    dna_seq_padded = pad_sequences(dna_seq_sequences, padding='post')
    dna_seq_final=dna_seq_padded[tf.newaxis, ...]

    return dna_seq_final

