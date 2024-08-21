import os
from pydub import AudioSegment
from tqdm import tqdm

def split_audio_to_snippets(input_dir, output_dir, snippet_duration=10):
    """
    Splits all audio files in a directory into 10-second snippets and saves them to the specified directory.

    Args:
        input_dir (str): Directory containing the input audio files.
        output_dir (str): Directory where the snippets will be saved.
        snippet_duration (int): Duration of each snippet in seconds (default is 10 seconds).
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Iterate over each audio file in the input directory
    for audio_file in tqdm(os.listdir(input_dir), desc="Splitting audio files"):
        input_file = os.path.join(input_dir, audio_file)
        
        # Load the audio file
        audio = AudioSegment.from_file(input_file)

        # Calculate the number of snippets
        snippet_duration_ms = snippet_duration * 1000  # Convert to milliseconds
        num_snippets = len(audio) // snippet_duration_ms

        # Split and save the snippets
        for i in range(num_snippets):
            start_time = i * snippet_duration_ms
            end_time = start_time + snippet_duration_ms
            snippet = audio[start_time:end_time]
            snippet.export(os.path.join(output_dir, f"{os.path.splitext(audio_file)[0]}_snippet_{i+1}.wav"), format="wav")

        # Handle the last snippet if it is shorter than the snippet duration
        if len(audio) % snippet_duration_ms != 0:
            start_time = num_snippets * snippet_duration_ms
            snippet = audio[start_time:]
            snippet.export(os.path.join(output_dir, f"{os.path.splitext(audio_file)[0]}_snippet_{num_snippets+1}.wav"), format="wav")

# Example usage           
# input_dir = 'assets//audio'
# output_dir = 'assets//snippets'
# split_audio_to_snippets(input_dir, output_dir)            