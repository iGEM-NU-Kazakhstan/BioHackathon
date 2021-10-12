import tensorflow as tf
from tensorflow.keras import layers, losses
from tensorflow.keras.models import Model


class ChainAutoencoder(Model):
  def __init__(self):
    super(ChainAutoencoder, self).__init__()
    self.encoder = tf.keras.Sequential([
        layers.Input(shape=(500, 1)),
        layers.Conv1D(32, (3), activation='relu', padding='same', strides=2),
        layers.Conv1D(16, (3), activation='relu', padding='same', strides=2),
        layers.Conv1D(8, (3), activation='relu', padding='valid', strides=2)])

    self.decoder = tf.keras.Sequential([
        layers.Conv1DTranspose(8, kernel_size=3, strides=2, activation='relu', padding='valid'),
        layers.Conv1DTranspose(16, kernel_size=3, strides=2, activation='relu', padding='same'),
        layers.Conv1DTranspose(32, kernel_size=3, strides=2, activation='relu', padding='same'),
        layers.Conv1D(1, kernel_size=(3), activation='sigmoid', padding='same')])

  def call(self, x):
    encoded = self.encoder(x)
    decoded = self.decoder(encoded)
    return decoded
