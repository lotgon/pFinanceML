import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras import layers
class Alphabet(Model):
    def __init__(self, window_size):
        super(Alphabet, self).__init__()
        self.encoder = tf.keras.Sequential([
            tf.keras.layers.Input(shape=(window_size, 1)),
            layers.Conv1D(2, 9, activation='relu', padding='same', strides=1),
            layers.MaxPool1D(2, strides=2, padding='valid'),
            layers.Conv1D(4, 9, activation='relu', padding='same', strides=1),
            layers.MaxPool1D(2, strides=2, padding='valid'),
            layers.Conv1D(8, 9, activation='relu', padding='same', strides=1),
            layers.MaxPool1D(2, strides=2, padding='valid'),
            layers.Conv1D(16, 9, activation='relu', padding='same', strides=1),
            layers.MaxPool1D(2, strides=2, padding='valid'),
            layers.Conv1D(32, 9, activation='relu', padding='same', strides=1),
            layers.MaxPool1D(2, strides=2, padding='valid'),
            layers.Flatten()
            ,layers.Dense(54)
        ])
        latent_shape = self.encoder.layers[-2].input_shape
        print(latent_shape)
        self.decoder = tf.keras.Sequential([
            layers.Input(shape=54),
            layers.Dense(latent_shape[1]*latent_shape[2], activation='relu'),
            layers.Reshape(latent_shape[1:]),
            layers.UpSampling1D(2),
            layers.Conv1DTranspose(32, kernel_size=9, strides=1, activation='relu', padding='same'),
            layers.UpSampling1D(2),
            layers.Conv1DTranspose(16, kernel_size=9, strides=1, activation='relu', padding='same'),
            layers.UpSampling1D(2),
            layers.Conv1DTranspose(8, kernel_size=9, strides=1, activation='relu', padding='same'),
            layers.UpSampling1D(2),
            layers.Conv1DTranspose(4, kernel_size=9, strides=1, activation='relu', padding='same'),
            layers.UpSampling1D(2),
            layers.Conv1DTranspose(2, kernel_size=9, strides=1, activation='relu', padding='same'),
            layers.Conv1D(1, 3, activation='sigmoid', padding='same')
        ])

    def call(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded

class AlphabetMulti(Model):
    def __init__(self, window_size):
        super(AlphabetMulti, self).__init__()
        self.nne1 = tf.keras.Sequential([
            layers.Input(shape=(window_size, 1)),
            layers.Conv1D(2, 9, activation='relu', padding='same', strides=1),
            #layers.BatchNormalization(),
            layers.MaxPool1D(2, strides=2, padding='valid'),
            layers.Conv1D(4, 9, activation='relu', padding='same', strides=1),
            #layers.BatchNormalization(),
            layers.MaxPool1D(2, strides=2, padding='valid'),
            layers.Conv1D(8, 9, activation='relu', padding='same', strides=1),
            #layers.BatchNormalization(),
            layers.MaxPool1D(2, strides=2, padding='valid'),
            layers.Conv1D(16, 9, activation='relu', padding='same', strides=1),
            #layers.BatchNormalization(),
            layers.MaxPool1D(2, strides=2, padding='valid'),
            layers.Conv1D(32, 9, activation='relu', padding='same', strides=1),
            #layers.BatchNormalization(),
            layers.MaxPool1D(2, strides=2, padding='valid')
        ])
        nne1_outputshape = self.nne1.layers[-1].output_shape
        print(nne1_outputshape)

        self.encoder1 = tf.keras.Sequential([
            layers.Input(shape=nne1_outputshape[1:]),
            layers.Flatten(),
            layers.Dense(100, activation="tanh")
            ,layers.Lambda(lambda x: tf.sign(x))
        ])

        # self.nne2 = tf.keras.Sequential([
        #     layers.Input(shape=nne1_outputshape[1:]),
        #     layers.Conv1D(32, 9, activation='relu', padding='same', strides=1),
        #     layers.MaxPool1D(2, strides=2, padding='valid'),
        #     layers.Conv1D(64, 9, activation='relu', padding='same', strides=1),
        #     layers.MaxPool1D(2, strides=2, padding='valid')
        # ])
        #
        # nne2_outputshape = self.nne2.layers[-1].output_shape
        # print(nne2_outputshape)
        #
        # self.encoder2 = tf.keras.Sequential([
        #     layers.Input(shape=nne2_outputshape[1:]),
        #     layers.Flatten(),
        #     layers.Dense(1024, activation='relu'),
        #     layers.Dense(100, activation='relu'),
        #     layers.Dense(10, activation='sigmoid')
        # ])

        self.decoder1 = tf.keras.Sequential([
            layers.Input(shape=100),
            #layers.Lambda(lambda x: -tf.math.log(1. / x - 1.)),
            #layers.Dense(nne1_outputshape[1]*nne1_outputshape[2]/4, activation='relu'),
            layers.Dense(nne1_outputshape[1]*nne1_outputshape[2], activation='relu'),
            layers.Reshape(nne1_outputshape[1:])
        ])
        self.nnd1 = tf.keras.Sequential([
            layers.UpSampling1D(2),
            #layers.BatchNormalization(),
            layers.Conv1DTranspose(32, kernel_size=9, strides=1, activation='relu', padding='same'),
            layers.UpSampling1D(2),
            #layers.BatchNormalization(),
            layers.Conv1DTranspose(16, kernel_size=9, strides=1, activation='relu', padding='same'),
            layers.UpSampling1D(2),
            #layers.BatchNormalization(),
            layers.Conv1DTranspose(8, kernel_size=9, strides=1, activation='relu', padding='same'),
            layers.UpSampling1D(2),
            #layers.BatchNormalization(),
            layers.Conv1DTranspose(4, kernel_size=9, strides=1, activation='relu', padding='same'),
            layers.UpSampling1D(2),
            #layers.BatchNormalization(),
            layers.Conv1DTranspose(2, kernel_size=9, strides=1, activation='relu', padding='same'),
            layers.Conv1D(1, 3, activation='sigmoid', padding='same', name='nnd1')
            ,layers.Flatten()
        ])
        # self.nnd1_ = tf.keras.Sequential([
        #     layers.UpSampling1D(2),
        #     layers.Conv1DTranspose(32, kernel_size=9, strides=1, activation='relu', padding='same'),
        #     layers.UpSampling1D(2),
        #     layers.Conv1DTranspose(16, kernel_size=9, strides=1, activation='relu', padding='same'),
        #     layers.UpSampling1D(2),
        #     layers.Conv1DTranspose(8, kernel_size=9, strides=1, activation='relu', padding='same'),
        #     layers.UpSampling1D(2),
        #     layers.Conv1DTranspose(4, kernel_size=9, strides=1, activation='relu', padding='same'),
        #     layers.UpSampling1D(2),
        #     layers.Conv1DTranspose(2, kernel_size=9, strides=1, activation='relu', padding='same'),
        #     layers.Conv1D(1, 3, activation = 'sigmoid', padding = 'same', name = 'nnd1_')
        # ])
        # self.decoder2 = tf.keras.Sequential([
        #     layers.Input(shape=10),
        #     layers.Dense(100, activation='relu'),
        #     layers.Dense(1024, activation='relu'),
        #     layers.Dense(nne2_outputshape[1]*nne2_outputshape[2], activation='relu'),
        #     layers.Reshape(nne2_outputshape[1:])
        # ])
        # self.nnd2 = tf.keras.Sequential([
        #     layers.UpSampling1D(2),
        #     layers.Conv1DTranspose(64, kernel_size=9, strides=1, activation='relu', padding='same'),
        #     layers.UpSampling1D(2),
        #     layers.Conv1DTranspose(32, kernel_size=9, strides=1, activation='relu', padding='same')
        # ])

    def call(self, x):
        nne1_result = self.nne1(x)
        encoded1 = self.encoder1(nne1_result)
        decoded1 = self.decoder1(encoded1)
        decoded2 = self.nnd1(decoded1)

        #nne2_result = self.nne2(nne1_result)
        #encoded2 = self.encoder2(nne2_result)

        #decoded2 = self.decoder2(encoded2)
        #decoded2 = self.nnd2(decoded2)
        #decoded2 = self.nnd1_(decoded2)

        return decoded2


class AlphabetTest(Model):
    def __init__(self, window_size):
        super(AlphabetTest, self).__init__()
        self.nne1 = tf.keras.Sequential([
            layers.Input(shape=(window_size)),
            layers.Flatten(),
            layers.Dense(100, activation='relu')
        ])
        self.encoder1 = tf.keras.Sequential([
            layers.Dense(100, activation='sigmoid')
        ])
        self.decoder1 = tf.keras.Sequential([
            layers.Input(shape=100),
            layers.Dense(100, activation='relu')
        ])
        self.nnd1 = tf.keras.Sequential([
            layers.Dense(window_size, activation='relu'),
            layers.Reshape((window_size, 1))
        ])

    def call(self, x):
        nne1_result = self.nne1(x)
        encoded1 = self.encoder1(nne1_result)
        decoded1 = self.decoder1(encoded1)
        decoded1 = self.nnd1(decoded1)

        #nne2_result = self.nne2(nne1_result)
        #encoded2 = self.encoder2(nne2_result)

        #decoded2 = self.decoder2(encoded2)
        #decoded2 = self.nnd2(decoded2)
        #decoded2 = self.nnd1_(decoded2)

        return decoded1
