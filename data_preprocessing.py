from config.data_preprocessing_spec import PREPROCESSING_SPEC

from audiomentations import Compose, AddGaussianNoise, TimeStretch, PitchShift, PolarityInversion
import numpy as np

from scipy import signal

SAMPLING_RATE = 16000

def apply_data_augmentation(augmentation_spec, decoded_list):
  augmentation_list = []

  if 'white_noise' in augmentation_spec:
    augmentation_list.append(AddGaussianNoise(min_amplitude=0.001, max_amplitude=0.01, p=0.5))
  
  if 'time_stretch' in augmentation_spec:
    augmentation_list.append(TimeStretch(min_rate=0.8, max_rate=1.25, p=0.5))
  
  if 'pitch_shift' in augmentation_spec:
    augmentation_list.append(PitchShift(min_semitones=-7, max_semitones=7, p=0.5))
  
  if 'polarity_inversion' in augmentation_spec:
    augmentation_list.append(PolarityInversion(p=0.5))
  
  augmented_samples = np.array([Compose(augmentation_list)(samples=sample, sample_rate=SAMPLING_RATE) for sample in decoded_list])
  return augmented_samples

def preprocess_audio_files(spec_name, decoded_list):
    augmentation_spec = PREPROCESSING_SPEC[spec_name]

    augmented_samples = apply_data_augmentation(augmentation_spec, decoded_list)

    spectogram_list = np.array([
        signal.spectrogram(sample, SAMPLING_RATE)[2] for sample in augmented_samples
    ])

    return spectogram_list

