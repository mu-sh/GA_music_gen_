import os
import random
import torchaudio
from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write
from pydub import AudioSegment
from tqdm import tqdm

# Load the pretrained model
model = MusicGen.get_pretrained('facebook/musicgen-melody')
model.set_generation_params(duration=8)  # generate 8 seconds.

def blend_audio_snippets(target_length, selected_segments, order, output_file):
    """
    Blends selected audio snippets together into a single audio file based on the specified order and target length.

    Args:
        target_length (float): Target track length in minutes (between 3.5 and 4.5 minutes).
        selected_segments (list): List of paths to the selected audio segments.
        order (list): List of indices representing the order in which to blend the segments.
        output_file (str): Path to the output blended audio file.
    """
    # Ensure the target length is within the specified range
    if not (3.5 <= target_length <= 4.5):
        raise ValueError("Target length must be between 3.5 and 4.5 minutes.")

    # Convert target length from minutes to milliseconds
    target_length_ms = target_length * 60 * 1000

    # Ensure the output directory exists
    output_dir = os.path.dirname(output_file)
    os.makedirs(output_dir, exist_ok=True)

    # Convert selected audio segments to AudioSegment and order them
    audio_segments = [AudioSegment.from_file(selected_segments[i]) for i in order]

    # Concatenate audio segments until the target length is reached
    blended_audio = AudioSegment.empty()
    current_length = 0

    for segment in tqdm(audio_segments, desc="Blending audio segments"):
        if current_length + len(segment) > target_length_ms:
            segment = segment[:target_length_ms - current_length]
        blended_audio += segment
        current_length += len(segment)
        if current_length >= target_length_ms:
            break

    # Export the final blended audio
    blended_audio.export(output_file, format="wav")

    # Return the fitness score (assuming a fitness function is defined)
    return fitness_function(output_file)

def fitness_function(output_file):
    """
    Dummy fitness function to score the blended audio.
    Replace this with your actual fitness function.

    Args:
        output_file (str): Path to the output blended audio file.

    Returns:
        float: Fitness score.
    """
    # Implement your fitness function here
    return random.random()

def genetic_algorithm(chroma_dir, output_dir, num_generations=10, population_size=10):
    """
    Genetic algorithm to optimize the blending of audio snippets.

    Args:
        chroma_dir (str): Directory containing the audio snippets.
        output_dir (str): Directory to save the output blended audio files.
        num_generations (int): Number of generations to run the algorithm.
        population_size (int): Number of individuals in the population.
    """
    # Load the snippets
    snippets = [os.path.join(chroma_dir, f) for f in os.listdir(chroma_dir)]

    # Initialize the population
    population = []
    for _ in range(population_size):
        target_length = random.uniform(3.5, 4.5)
        selected_segments = random.sample(snippets, len(snippets))
        order = list(range(len(selected_segments)))
        random.shuffle(order)
        population.append({
            'target_length': target_length,
            'selected_segments': selected_segments,
            'order': order
        })

    # Run the genetic algorithm
    for generation in range(num_generations):
        print(f"Generation {generation + 1}")

        # Evaluate the fitness of each individual
        for individual in population:
            output_file = os.path.join(output_dir, f"generation_{generation + 1}_individual_{population.index(individual) + 1}.wav")
            individual['fitness'] = blend_audio_snippets(
                individual['target_length'],
                individual['selected_segments'],
                individual['order'],
                output_file
            )

        # Sort the population by fitness
        population.sort(key=lambda x: x['fitness'], reverse=True)

        # Select the best individuals
        best_individuals = population[:2]

        # Create the next generation
        new_population = best_individuals.copy()
        while len(new_population) < population_size:
            parent1, parent2 = random.sample(best_individuals, 2)
            child = {
                'target_length': random.choice([parent1['target_length'], parent2['target_length']]),
                'selected_segments': random.choice([parent1['selected_segments'], parent2['selected_segments']]),
                'order': random.choice([parent1['order'], parent2['order']])
            }
            new_population.append(child)

        population = new_population

    # Save the best solutions
    for i, individual in enumerate(best_individuals):
        output_file = os.path.join(output_dir, f"best_solution_{i + 1}.wav")
        blend_audio_snippets(
            individual['target_length'],
            individual['selected_segments'],
            individual['order'],
            output_file
        )

# Example usage
#chroma_dir = 'assets//snippets'
#output_dir = 'assets//output'
#genetic_algorithm(chroma_dir, output_dir)