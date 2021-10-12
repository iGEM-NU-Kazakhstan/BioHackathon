import pandas as pd
import tensorflow as tf
import numpy as np
from tensorflow.keras import layers, losses

from DataPreprocessing import Preprocessing
from ModelDetector import create_model, kmer, list_of_sequenses
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Data preprocessing
# Load data from csv

data = pd.read_csv('../data/classic_restrict.csv')

# Read data
dna_data = data['sequence'].to_list()

# Define enzymes data
enzymes_name = ['ecoR1','Xba1','Spe1','Pst1','Not1','Sap1','Bsa1']


# Training and preprocessing loop
for i in enzymes_name:
    print('Enzyme: %s' % i)

    length = 6

    # Define the enzyme work
    label_data = data[i].to_list()

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

    # Define the model
    RestrictionDetector = create_model(vocab_size, max_length)

    learning_rate = 0.006
    RestrictionDetector.compile(loss='binary_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])

    num_epochs = 10
    history = RestrictionDetector.fit(padded, y_zero, epochs=num_epochs, validation_data=(test_seq_final, y_test))

    # Save the model
    RestrictionDetector.save(str('saved_models/Detector'+i))



