import os
from pydub import AudioSegment
from tqdm import tqdm


def blend_audio_snippets(snippets_dir, output_file):
    """
    Blends all audio snippets in a directory together into a single audio file.

    Args:
        snippets_dir (str): Directory containing the audio snippets.
        output_file (str): Path to the output blended audio file.
    """
    # Ensure the output directory exists
    output_dir = os.path.dirname(output_file)
    os.makedirs(output_dir, exist_ok=True)

    # Convert generated audio tensors to AudioSegment
    audio_segments = []

    # Iterate over each snippet in the directory
    for snippet_file in tqdm(os.listdir(snippets_dir), desc="Blending audio snippets"):
        snippet_path = os.path.join(snippets_dir, snippet_file)
        
        # Load the snippet
        snippet = AudioSegment.from_file(snippet_path)
        audio_segments.append(snippet)

    # Concatenate all audio segments
    blended_audio = sum(audio_segments)

    # Export the final blended audio
    blended_audio.export(output_file, format="wav")

# Example usage
# snippets_dir = 'assets//snippets'
# output_file = 'assets//blended_output.wav'
# blend_audio_snippets(snippets_dir, output_file)    