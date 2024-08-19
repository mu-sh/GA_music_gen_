import torchaudio
from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write
from pydub import AudioSegment
import numpy as np

# Load the pretrained model
model = MusicGen.get_pretrained('facebook/musicgen-melody')
model.set_generation_params(duration=8)  # generate 8 seconds.

# Generate unconditional audio samples
wav_unconditional = model.generate_unconditional(4)  # generates 4 unconditional audio samples

# Generate audio samples based on descriptions
descriptions = ['breakcore', 'IDM', 'hyperpop']
wav_descriptions = model.generate(descriptions)  # generates 3 samples.

# Load melody and generate audio samples with chroma
melody, sr = torchaudio.load('assets//trimmed_audiofile.mp3')
wav_chroma = model.generate_with_chroma(descriptions, melody[None].expand(3, -1, -1), sr)

# Function to convert tensor to AudioSegment
def tensor_to_audiosegment(tensor, sample_rate):
    audio_array = tensor.cpu().numpy()
    audio_array = (audio_array * 32767).astype(np.int16)  # Convert to int16
    return AudioSegment(
        audio_array.tobytes(),
        frame_rate=sample_rate,
        sample_width=audio_array.dtype.itemsize,
        channels=1
    )

# Convert generated audio tensors to AudioSegment
audio_segments = []

# Process unconditional audio samples
for wav in wav_unconditional:
    audio_segments.append(tensor_to_audiosegment(wav, model.sample_rate))

# Process description-based audio samples
for wav in wav_descriptions:
    audio_segments.append(tensor_to_audiosegment(wav, model.sample_rate))

# Process chroma-based audio samples
for wav in wav_chroma:
    audio_segments.append(tensor_to_audiosegment(wav, model.sample_rate))

# Concatenate all audio segments
blended_audio = sum(audio_segments)

# Export the final blended audio
blended_audio.export("blended_output.wav", format="wav")