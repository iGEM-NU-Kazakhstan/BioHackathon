import pandas as pd
import tensorflow as tf

from tensorflow.keras import layers, losses

from DataPreprocessing import Preprocessing
from ModelEncoder import ChainAutoencoder

# Data preprocessing
# Load data from csv

data = pd.read_csv('../data/seq1.csv')

# Read data
dna_data = data['sequence'].to_list()
label_data = data['label'].to_list()

# Data preprocessing
train_dna, test_dna = Preprocessing().TestTrain(dna_data, 70)
train_label, test_label = Preprocessing().TestTrain(label_data, 70)

train_dna = Preprocessing().DNA_labeler(train_dna)
test_dna = Preprocessing().DNA_labeler(test_dna)
train_label = Preprocessing().Arrayer(train_label)
test_label = Preprocessing().Arrayer(test_label)

train_dna = train_dna[..., tf.newaxis]
test_dna = test_dna[..., tf.newaxis]
train_label = train_label[..., tf.newaxis]
test_label = test_label[..., tf.newaxis]

# Define the Model
autoencoder = ChainAutoencoder()

autoencoder.compile(optimizer='adam', loss=losses.MeanSquaredError())

# Train the Model
autoencoder.fit(train_dna, train_label,
                epochs=20,
                shuffle=True,
                validation_data=(test_dna, test_label))

# Save the model
autoencoder.save('../saved_models/ORFdetector')
