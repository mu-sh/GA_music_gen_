import os
import torchaudio
from tqdm import tqdm
from audiocraft.data.audio import audio_write
from audiocraft.models import MusicGen

# Load the pretrained model
model = MusicGen.get_pretrained('facebook/musicgen-melody')
model.set_generation_params(duration=8)  # generate 8 seconds.

def generate_chroma_for_snippets(snippets_dir, output_dir, descriptions):
    """
    Generates chroma-based audio samples for each snippet in a directory and saves them to the specified directory.

    Args:
        snippets_dir (str): Directory containing the audio snippets.
        output_dir (str): Directory where the chroma-based audio samples will be saved.
        descriptions (list): List of descriptions for generating chroma-based audio samples.
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Iterate over each snippet in the directory
    for snippet_file in tqdm(os.listdir(snippets_dir), desc="Generating chroma for snippets"):
        snippet_path = os.path.join(snippets_dir, snippet_file)
        
        # Load the snippet
        melody, sr = torchaudio.load(snippet_path)
        
        # Generate chroma-based audio samples
        wav_chroma = model.generate_with_chroma(descriptions, melody[None].expand(3, -1, -1), sr)
        
        # Save the generated chroma-based audio samples
        for i, wav in enumerate(wav_chroma):
            output_path = os.path.join(output_dir, f"{os.path.splitext(snippet_file)[0]}_chroma_{i+1}.wav")
            audio_write(output_path, wav, sr)



# Example usage
# snippets_dir = 'assets//snippets'
# output_dir = 'assets//chroma'
# descriptions = ['breakcore', 'IDM', 'hyperpop']
# generate_chroma_for_snippets(snippets_dir, output_dir, descriptions)            