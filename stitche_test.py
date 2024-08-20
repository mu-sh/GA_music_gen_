import torchaudio
from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write
from pydub import AudioSegment
import os
import numpy as np
import time
from tqdm import tqdm

# Load the pretrained model
model = MusicGen.get_pretrained('facebook/musicgen-melody')
model.set_generation_params(duration=8)  # generate 8 seconds.

# Start timer
start_time = time.time()

# Generate unconditional audio samples
wav_unconditional = model.generate_unconditional(4)  # generates 4 unconditional audio samples

# Generate audio samples based on descriptions
descriptions = ['breakcore', 'IDM', 'hyperpop']
wav_descriptions = model.generate(descriptions)  # generates 3 samples.


def split_audio_to_snippets(input_file, output_dir, snippet_duration=10):
    """
    Splits an audio file into 10-second snippets and saves them to the specified directory.

    Args:
        input_file (str): Path to the input audio file.
        output_dir (str): Directory where the snippets will be saved.
        snippet_duration (int): Duration of each snippet in seconds (default is 10 seconds).
    """
    # Load the audio file
    audio = AudioSegment.from_file(input_file)

    # Calculate the number of snippets
    snippet_duration_ms = snippet_duration * 1000  # Convert to milliseconds
    num_snippets = len(audio) // snippet_duration_ms

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Split and save the snippets
    for i in range(num_snippets):
        start_time = i * snippet_duration_ms
        end_time = start_time + snippet_duration_ms
        snippet = audio[start_time:end_time]
        snippet.export(os.path.join(output_dir, f"snippet_{i+1}.wav"), format="wav")

    # Handle the last snippet if it is shorter than the snippet duration
    if len(audio) % snippet_duration_ms != 0:
        start_time = num_snippets * snippet_duration_ms
        snippet = audio[start_time:]
        snippet.export(os.path.join(output_dir, f"snippet_{num_snippets+1}.wav"), format="wav")

# Example usage
input_file = 'assets//empty Brain.mp3'
output_dir = 'assets//snippets'
split_audio_to_snippets(input_file, output_dir)

# Directory containing the audio snippets
snippets_dir = 'assets//snippets'
output_dir = 'assets//chroma'
os.makedirs(output_dir, exist_ok=True)

# Descriptions for generating chroma-based audio samples
descriptions = ['breakcore', 'IDM', 'hyperpop']

# Iterate over each snippet in the directory
for snippet_file in tqdm(os.listdir(snippets_dir), desc="Processing snippets"):
    snippet_path = os.path.join(snippets_dir, snippet_file)
    
    # Load the snippet
    melody, sr = torchaudio.load(snippet_path)
    
    # Generate chroma-based audio samples
    wav_chroma = model.generate_with_chroma(descriptions, melody[None].expand(3, -1, -1), sr)
    
    # Save the generated chroma-based audio samples
    for i, wav in enumerate(wav_chroma):
        output_path = os.path.join(output_dir, f"{os.path.splitext(snippet_file)[0]}_chroma_{i+1}.wav")
        audio_write(output_path, wav, sr)

print("Chroma generation for all snippets completed.")

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


# Process chroma-based audio samples
for wav in tqdm(wav_chroma, desc="Processing chroma-based audio samples"):
    audio_segments.append(tensor_to_audiosegment(wav, model.sample_rate))

# Concatenate all audio segments
blended_audio = sum(audio_segments)

# Export the final blended audio
blended_audio.export("blended_output.wav", format="wav")

# End timer
end_time = time.time()
print(f"Total time taken: {end_time - start_time} seconds")