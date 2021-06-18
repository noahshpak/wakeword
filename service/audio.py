import tensorflow as tf
import tensorflow_io as tfio


def decode_audio(audio_binary):
    audio, sample_rate = tf.audio.decode_wav(audio_binary, desired_channels=1)
    audio = tfio.audio.resample(audio, tf.cast(sample_rate, tf.int64), 16000)
    return tf.squeeze(audio, axis=-1)


def get_spectrogram(waveform):
    # Padding for files with less than 16000 samples
    if tf.shape(waveform)[0] > 16000:
        waveform = waveform[:16000]
    zero_padding = tf.zeros([16000] - tf.shape(waveform), dtype=tf.float32)

    # Concatenate audio with padding so that all audio clips will be of the
    # same length
    waveform = tf.cast(waveform, tf.float32)
    equal_length = tf.concat([waveform, zero_padding], 0)
    spectrogram = tf.signal.stft(equal_length, frame_length=255, frame_step=128)

    spectrogram = tf.abs(spectrogram)
    spectrogram = tf.expand_dims(spectrogram, -1)
    return spectrogram
