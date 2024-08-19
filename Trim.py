from pydub import AudioSegment

# Load the audio file
audio = AudioSegment.from_file("assets\empty Brain.mp3")

# Define start and end times in milliseconds
start_time = 15000  # 10 seconds
end_time = 25000    # 20 seconds

# Trim the audio
trimmed_audio = audio[start_time:end_time]

# Export the trimmed audio to a new file
trimmed_audio.export("assets/trimmed_audiofile.mp3", format="mp3")