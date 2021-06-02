from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import torch

def run_trained_wav2vec2_model(audio_file, wake_word):
  processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")
  model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")

  input_values = processor(audio_file, sampling_rate=sample_rate, return_tensors="pt").input_values

  # INFERENCE

  # retrieve logits & take argmax
  logits = model(input_values).logits
  predicted_ids = torch.argmax(logits, dim=-1)

  # transcribe
  transcription = processor.decode(predicted_ids[0])

  contained_wake_word = wake_word in transcription.lower().split(' ')

  return contained_wake_word