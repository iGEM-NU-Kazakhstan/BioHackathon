import tensorflow as tf


def create_model(vocab_size, max_length):
    model = tf.keras.Sequential([
        tf.keras.layers.Embedding(vocab_size, 16, input_length=max_length),
        tf.keras.layers.Conv1D(32, 5, activation='relu'),
        tf.keras.layers.MaxPool1D((2)),
        tf.keras.layers.Conv1D(16, 5, activation='relu'),
        tf.keras.layers.MaxPool1D((2)),
        tf.keras.layers.GlobalMaxPooling1D(),
        tf.keras.layers.Dense(72, activation='relu'),
        tf.keras.layers.Dropout(.5),
        tf.keras.layers.Dense(1, activation="sigmoid")
    ])

    return model


def kmer(sequense, klen):
    seqlist = ' '.join([sequense[i:i+klen] for i in range(len(sequense)-klen+1)])
    return seqlist


def list_of_sequenses(list, klen):
    list_of_seq = [kmer(i, klen) for i in list]
    return list_of_seq